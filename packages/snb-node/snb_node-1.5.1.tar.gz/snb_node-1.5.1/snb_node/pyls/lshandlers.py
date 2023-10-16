import subprocess
import threading
import json

import tornado
from tornado import ioloop, process, web, websocket, gen
from pylsp_jsonrpc import streams


class LanguageServerWebSocketHandler(tornado.websocket.WebSocketHandler):
    writer = None

    def check_origin(self, origin):
        return True

    #@gen.coroutine
    def get(self):
        return super(LanguageServerWebSocketHandler, self).get()
        #await super(LanguageServerWebSocketHandler, self).get()


    def open(self, *args, **kwargs):
        self.proc = process.Subprocess(
            #['python' ,'/snb_node/pyls__main.py', '-v'],  # 具体的LSP实现进程，如 'pyls -v'、'ccls --init={"index": {"onChange": true}}'等
            ['python', 'c:/smartnotebook/snb_node/pyls__main.py', '-v'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
        self.writer = streams.JsonRpcStreamWriter(self.proc.stdin)

        def consume():
            ioloop.IOLoop()
            reader = streams.JsonRpcStreamReader(self.proc.stdout)
            reader.listen(lambda msg: self.write_message(json.dumps(msg)))

        self.thread = threading.Thread(target=consume)
        self.thread.daemon = True
        self.thread.start()

    def on_message(self, message):
        self.writer.write(json.loads(message))

    def on_close(self):
        if self.writer:
            self.writer.close()
            self.writer = None
        if self.proc:
            self.proc.uninitialize()
        if self.thread.is_alive():
            print("on_close self.thread.is_alive is true")





default_handlers = [
    (fr"/api/snb/node/pylsws", LanguageServerWebSocketHandler)
]
