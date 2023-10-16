import json
import os

import requests
from concurrent.futures import ThreadPoolExecutor
from tornado import gen, web
from jupyter_client.jsonutil import json_default
import time
import re
import snb_plugin.utils.snb_RSA as snb_rsa

from snb_node.base.Interceptor import interceptor
from snb_node.config.Config import SNB_SERVER_URL,config,pem,workspace_uid

from tornado.concurrent import run_on_executor

file_list_url="/api/snb_native/notebook_file/list/%s/%s?page=1&pageSize=100"
file_down_url="/api/snb_native/notebook_file/download/%s/%s"
home=""

class TestHandler(web.RequestHandler):
    def is_folder_empty(self, file_path):
        files = os.listdir(file_path)
        return len(files) == 0

    @gen.coroutine
    @interceptor
    def get(self, ws_uid) -> {"GRADE": ["BASIC"], "ROLE": ["ADMIN", "EDITOR", "VIEWER"]}:
        header = self.request.headers
        info = {
            "user_ws_role": header.get("user_ws_role"),
            "snb_user_grade": header.get("snb_user_grade")
        }

        res = {"code": 200, "msg": "托尔斯泰", "data": info}
        self.finish(json.dumps(res, default=json_default))

class permission_config_Handler(web.RequestHandler):

    @gen.coroutine
    def get(self):
        print(1)
        res = {"code": 200, "msg": "内容查询成功", "data": self.application.permission_config}
        self.finish(json.dumps(res, default=json_default))

class FileHandler(web.RequestHandler):

    def is_folder_empty(self, file_path):
        files = os.listdir(file_path)
        return len(files) == 0

    @gen.coroutine
    @interceptor
    def delete(self, ws_uid) -> {"GRADE": ["BASIC", "PRO", "ENT"], "ROLE": ["ADMIN", "EDITOR"]}:
        try:
            body = self.request.body.strip().decode('utf-8')
            json_body = json.loads(body)
            file_path = json_body["file_path"]
            type = json_body["type"]
            if type == 'folder':
                if os.path.isdir(file_path):
                    if self.is_folder_empty(file_path):
                        os.rmdir(file_path)
                        res = {"code": 200, "msg": "文件夹删除成功", "data": []}
                        self.finish(json.dumps(res, default=json_default))
                    else:
                        res = {"code": 400, "msg": "当前文件夹不为空", "data": []}
                        self.finish(json.dumps(res, default=json_default))
                else:
                    res = {"code": 400, "msg": "非法路径", "data": [file_path]}
                    self.finish(json.dumps(res, default=json_default))
            elif type == 'file':
                if file_path:
                    os.remove(file_path)
                    res = {"code": 200, "msg": "文件删除成功", "data": []}
                    self.finish(json.dumps(res, default=json_default))
            else:
                res = {"code": 400, "msg": "无效类型", "data": [type]}
                self.finish(json.dumps(res, default=json_default))
        except Exception as e:
            res = {"code": 400, "msg": "删除失败", "data": [f"文件 '{file_path}' 删除失败: {e.strerror}"]}
            self.finish(json.dumps(res, default=json_default))

class WsFileSyncNodeHandler(web.RequestHandler):
    @gen.coroutine
    @interceptor
    def get(self, ws_uid) -> {"GRADE": ["BASIC", "PRO", "ENT"], "ROLE": ["ADMIN", "EDITOR"]}:
        try:
            dest_file = self.get_argument('path', '')
            if os.path.exists(dest_file):
                res = {"code": 200, "msg": "该文件存在", "data": [dest_file]}
            else:
                res = {"code": 200, "msg": "该文件不存在", "data": {}}
            self.finish(json.dumps(res, default=json_default))
        except Exception as e:
            res = {"code": 400, "msg": "查询失败", "data": [e]}
            self.finish(json.dumps(res, default=json_default))

    @interceptor
    def post(self, ws_uid) -> {"GRADE": ["BASIC", "PRO", "ENT"], "ROLE": ["ADMIN", "EDITOR"]}:
        try:
            cookie = self.request.headers['Cookie']
            params = json.loads(self.request.body)
            uid = params.get("uid")
            file_path = params.get("file_path")
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            url = ''.join([SNB_SERVER_URL, file_down_url]) % (ws_uid, uid)
            sign_str = snb_rsa.sign(file_down_url % (ws_uid, uid), pem)
            header = {"Cookie": cookie, "sign": sign_str, "workspaceUid": workspace_uid}
            conn_info = requests.get(url, headers=header)
            with open(home + file_path, 'wb') as fp:
                fp.write(conn_info.content)
            res = {"code": 200, "msg": "同步成功", "data": {}}
            self.finish(json.dumps(res, default=json_default))
        except Exception as e:
            res = {"code": 400, "msg": "同步失败", "data":{}}
            self.finish(json.dumps(res, default=json_default))


class FileSyncHandler(web.RequestHandler):

    def downloadFile(self,folder_uid, cookie, ws_uid):
        url = ''.join([SNB_SERVER_URL, file_list_url]) % (ws_uid, folder_uid)
        sign_str = snb_rsa.sign(file_list_url % (ws_uid, folder_uid), pem)
        header = {"Cookie": cookie, "sign": sign_str, "workspaceUid": workspace_uid}
        conn_info = requests.get(url, headers=header)
        print(conn_info.text)
        print(url)
        resp = conn_info.json()
        if resp["code"] == 200:
            for d in resp['data']['data']:
                if d['type'] == 'file':
                    url = ''.join([SNB_SERVER_URL, file_down_url]) % (ws_uid, d['uid'])
                    sign_str = snb_rsa.sign(file_down_url % (ws_uid, d['uid']), pem)
                    header = {"Cookie": cookie, "sign": sign_str, "workspaceUid": workspace_uid}
                    conn_info = requests.get(url, headers=header)
                    with open(home + d['file_path'], 'wb') as fp:
                        fp.write(conn_info.content)
                    print(d['name'])
                if d['type'] == 'folder':
                    dir_path = home + d['file_path']
                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)
                    self.downloadFile(d['uid'], cookie, ws_uid)
                    print(d['name'])
        else :
            raise Exception('server 500 错误')


    # @web.authenticated
    @gen.coroutine
    @interceptor
    def get(self,ws_uid) -> {"GRADE": ["BASIC", "PRO", "ENT"], "ROLE": ["ADMIN", "EDITOR"]}:
        try:
            cookie = self.request.headers['Cookie']
            self.downloadFile('',cookie,ws_uid)
            res = {"code": 200, "msg": "文件同步成功", "data": []}
            self.finish(json.dumps(res, default=json_default))
        except Exception as e :
            res = {"code": 400, "msg": "File Sync 失败", "data": [e]}
            self.finish(json.dumps(res, default=json_default))

class nodeStatHandler(web.RequestHandler):
    executor = ThreadPoolExecutor(4)

    @run_on_executor
    def getNodeStat(self):
        with open('/sys/fs/cgroup/memory/memory.limit_in_bytes', 'r') as fp:
            mem = fp.readline()
        mem = int(mem)
        with open('/proc/meminfo', 'r') as fp:
            py_mem = fp.readline()
        phy_mem = re.sub(r"[a-zA-Z :]", "", py_mem)
        phy_mem = int(phy_mem) * 1024
        memory = round(min(mem, phy_mem) / (1024 * 1024 * 1024), 2)

        with open('/sys/fs/cgroup/memory/memory.usage_in_bytes', 'r') as fp:
            usa_mem = fp.readline()
        memory_usage = round(int(usa_mem) / (1024 * 1024 * 1024), 2)

        with open('/sys/fs/cgroup/cpu/cpu.shares', 'r') as fp:
            cpu = fp.readline()
        cpu_core = round(int(cpu) / (1024))

        with open('/sys/fs/cgroup/cpu/cpuacct.usage', 'r') as fp:
            cpu_time_start = fp.readline()
        time.sleep(1)
        with open('/sys/fs/cgroup/cpu/cpuacct.usage', 'r') as fp:
            cpu_time_end = fp.readline()
        cpu_usage_per = round((int(cpu_time_end) - int(cpu_time_start)) / (10 ** 9) * 100, 2)

        return {"memory": memory, "memory_usage": memory_usage, "cpu_core": cpu_core, "cpu_usage_per": cpu_usage_per}


    # @web.authenticated
    @gen.coroutine
    @interceptor
    def get(self, ws_uid, env_uid) -> {"GRADE": ["BASIC", "PRO", "ENT"], "ROLE": ["ADMIN", "EDITOR"]}:
        try:
            res=yield self.getNodeStat()
            res = {"code": 200, "msg": "获取Node 信息成功", "data": [res]}
            self.finish(json.dumps(res, default=json_default))
        except Exception as e :
            res = {"code": 400, "msg": "node stat 失败", "data": []}
            self.finish(json.dumps(res, default=json_default))


_ws_uid_regex = r"(?P<ws_uid>.*)"
_ws_env_id_regex = r"(?P<env_uid>.*)"
_ws_uid = r"(?P<ws_uid>[^/]+)"
default_handlers = [
    (fr"/api/snb/node/notebook_file/sync/{_ws_uid_regex}", FileSyncHandler),
    (fr"/api/snb/node/file/sync/{_ws_uid_regex}", WsFileSyncNodeHandler),
    (fr"/api/snb/node/nodeStatInfo/{_ws_uid}/{_ws_env_id_regex}", nodeStatHandler),
    (fr"/api/snb/node/file/{_ws_uid_regex}", FileHandler),
    (fr"/api/snb/node/test/{_ws_uid_regex}", TestHandler),
    (fr"/api/node/permission_config/test", permission_config_Handler)

]
