import json

from tornado import gen, web
from snb_node.base.handlers import APIHandler
from jupyter_client.jsonutil import json_default

class HeartBeatHandler(APIHandler):

    @gen.coroutine
    def get(self):
        """
        desc: 返回正在运行的 sessions 列表
        :return: list of running sessions
        """

        res = {"code": 200, "msg": "success", "data": ""}
        self.finish(json.dumps(res, default=json_default))

default_handlers = [
    (fr"/api/snb/node/heartbeat", HeartBeatHandler)
]
