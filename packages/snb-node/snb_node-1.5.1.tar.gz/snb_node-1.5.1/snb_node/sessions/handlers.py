# -*- coding: utf-8 -*-
"""
@Time    : 2022/7/27
@Author  : hao.wu
"""
import json

from tornado import gen, web
from jupyter_client.jsonutil import json_default
from jupyter_client.kernelspec import NoSuchKernel

from snb_node.base.handlers import APIHandler
from snb_node.base.Interceptor import interceptor
from snb_node.tools.utils import maybe_future, url_path_join


class SessionRootHandler(APIHandler):
    # @web.authenticated
    @gen.coroutine
    def get(self, ws_uid):
        """
        desc: 返回正在运行的 sessions 列表
        :return: list of running sessions
        """
        sm = self.session_manager
        sessions = yield maybe_future(sm.list_sessions())
        res = {"code": 200, "msg": "success", "data": sessions}
        self.finish(json.dumps(res, default=json_default))

    # @web.authenticated
    @interceptor
    @gen.coroutine
    def post(self, ws_uid) -> {"GRADE": ["BASIC", "PRO", "ENT"], "ROLE": ["ADMIN", "EDITOR", "VIEWER"]}:
        """
        desc: 如果指定的会话不存在，创建一个新的 session
        :return:
        """
        sm = self.session_manager

        model = self.get_json_body()
        if model is None:
            raise web.HTTPError(400, "No JSON data provided")

        if "notebook" in model and "path" in model["notebook"]:
            self.log.warning("Sessions API changed, see updated swagger docs")
            model["path"] = model["notebook"]["path"]
            model["type"] = "notebook"

        try:
            path = model["path"]
        except KeyError as e:
            raise web.HTTPError(400, "Missing field in JSON data: path") from e

        try:
            mtype = model["type"]
        except KeyError as e:
            raise web.HTTPError(400, "Missing field in JSON data: type") from e

        name = model.get("name", None)
        kernel = model.get("kernel", {})
        kernel_name = kernel.get("name", None)
        kernel_id = kernel.get("id", None)

        if not kernel_id and not kernel_name:
            self.log.debug("No kernel specified, using default kernel")
            kernel_name = None

        exists = yield maybe_future(sm.session_exists(path=path))
        if exists:
            model = yield maybe_future(sm.get_session(path=path))
        else:
            try:
                model = yield maybe_future(
                    sm.create_session(path=path, kernel_name=kernel_name, kernel_id=kernel_id, name=name, type=mtype)
                )
            except NoSuchKernel:
                msg = f"The '{kernel_name}' kernel is not available. 请联系管理员进行修复或安装 '{kernel_name}' kernel."
                status_msg = f"{kernel_name} kernel not found！"
                self.log.warning(f"Kernel not found: {kernel_name}")
                self.set_status(200)
                #self.finish(json.dumps(dict(message=msg, short_message=status_msg)))
                self.finish(json.dumps({'code': 200, 'data': [], 'msg': msg}))
                return

        location = url_path_join(self.base_url, "api", "sessions", model["id"])
        self.set_header("Location", location)
        self.set_status(200)
        res = {"code": 200, "msg": "success", "data": model}
        self.finish(json.dumps(res, default=json_default))


class SessionHandler(APIHandler):
    @interceptor
    @web.authenticated
    @gen.coroutine
    def get(self, ws_uid, session_id) -> {"GRADE": ["BASIC", "PRO", "ENT"], "ROLE": ["ADMIN", "EDITOR"]}:
        """
        desc: 返回单个 session 的信息
        :param session_id:
        :return:
        """
        # Returns the JSON model for a single session
        sm = self.session_manager
        model = yield maybe_future(sm.get_session(session_id=session_id))
        self.finish(json.dumps(model, default=json_default))

    @web.authenticated
    @gen.coroutine
    def patch(self, session_id):
        """Patch updates sessions:

        - 路径更新，会话以跟踪重命名的路径
        - kernel.name 使用给定的内核规范启动一个新内核
        """
        sm = self.session_manager
        km = self.kernel_manager
        model = self.get_json_body()
        if model is None:
            raise web.HTTPError(400, "No JSON data provided")

        # get the previous session model
        before = yield maybe_future(sm.get_session(session_id=session_id))

        changes = {}
        if "notebook" in model and "path" in model["notebook"]:
            self.log.warning("Sessions API changed, see updated swagger docs")
            model["path"] = model["notebook"]["path"]
            model["type"] = "notebook"
        if "path" in model:
            changes["path"] = model["path"]
        if "name" in model:
            changes["name"] = model["name"]
        if "type" in model:
            changes["type"] = model["type"]
        if "kernel" in model:
            # Kernel id takes precedence over name.
            if model["kernel"].get("id") is not None:
                kernel_id = model["kernel"]["id"]
                if kernel_id not in km:
                    raise web.HTTPError(400, f"No such kernel: {kernel_id}")
                changes["kernel_id"] = kernel_id
            elif model["kernel"].get("name") is not None:
                kernel_name = model["kernel"]["name"]
                kernel_id = yield sm.start_kernel_for_session(
                    session_id, kernel_name=kernel_name, name=before["name"], path=before["path"], type=before["type"]
                )
                changes["kernel_id"] = kernel_id

        yield maybe_future(sm.update_session(session_id, **changes))
        model = yield maybe_future(sm.get_session(session_id=session_id))

        if model["kernel"]["id"] != before["kernel"]["id"]:
            # kernel_id changed because we got a new kernel
            # shutdown the old one
            yield maybe_future(km.shutdown_kernel(before["kernel"]["id"]))
        self.finish(json.dumps(model, default=json_default))

    @interceptor
    @web.authenticated
    @gen.coroutine
    def delete(self, ws_uid, session_id) -> {"GRADE": ["BASIC", "PRO", "ENT"], "ROLE": ["ADMIN", "EDITOR"]}:
        """
        desc: 根据 session_id 删除 session
        :param session_id:
        :return:
        """
        sm = self.session_manager
        try:
            yield maybe_future(sm.delete_session(session_id))
        except KeyError as e:
            # the kernel was deleted but the session wasn't!
            raise web.HTTPError(410, "Kernel deleted before session") from e
        self.set_status(200)
        self.finish(json.dumps({"msg": "成功", "code": 200, "data": []}, default=json_default))


# -----------------------------------------------------------------------------
# URL to handler mappings
# -----------------------------------------------------------------------------

_session_id_regex = r"(?P<session_id>\w+-\w+-\w+-\w+-\w+)"
_ws_uid = r"(?P<ws_uid>[^/]+)"
default_handlers = [
    (rf"/api/snb/node/sessions/{_ws_uid}/{_session_id_regex}", SessionHandler),
    (rf"/api/snb/node/sessions/{_ws_uid}", SessionRootHandler),
]
