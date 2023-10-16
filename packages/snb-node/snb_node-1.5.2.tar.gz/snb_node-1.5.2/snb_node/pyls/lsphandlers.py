import subprocess
import threading
import json

import tornado
from tornado import ioloop, process, web, websocket, gen
from pylsp_jsonrpc import streams
from pylsp.python_lsp import PythonLSPServer



class LanguageServerWebSocketHandler(tornado.websocket.WebSocketHandler):
    pylsp_handler = None

    def check_origin(self, origin):
        return True

    #@gen.coroutine
    def get(self, ws_uid):
        return super(LanguageServerWebSocketHandler, self).get()
        #await super(LanguageServerWebSocketHandler, self).get()


    def open(self, *args, **kwargs):

        def send_message(message):
            try:
                payload = json.dumps(message, ensure_ascii=False)
                self.write_message(payload)
            except Exception as e:  # pylint: disable=broad-except
                print("Failed to write message %s, %s", message, str(e))

        self.pylsp_handler = PythonLSPServer(rx=None, tx=None, consumer=send_message,check_parent_process=False)
        self.pylsp_handler.start()


    def on_message(self, message):
        msg = tornado.escape.json_decode(message)
        self.pylsp_handler.consume(msg)


    def on_close(self):
        if self.pylsp_handler:
            #self.pylsp_handler.close()
            self.pylsp_handler = None


_ws_uid = r"(?P<ws_uid>[^/]+)"
default_handlers = [
    (fr"/api/snb/node/pylsws/{_ws_uid}", LanguageServerWebSocketHandler)
]
