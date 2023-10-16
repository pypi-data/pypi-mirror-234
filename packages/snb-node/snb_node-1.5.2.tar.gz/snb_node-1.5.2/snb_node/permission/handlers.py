import json
from tornado import gen, web
from jupyter_client.jsonutil import json_default

class permission_config_Handler(web.RequestHandler):

    @gen.coroutine
    def get(self):
        print(1)
        res = {"code": 200, "msg": "内容查询成功", "data": self.application.permission_config}
        self.finish(json.dumps(res, default=json_default))

default_handlers = [
    (fr"/api/node/permission_config", permission_config_Handler)
]
