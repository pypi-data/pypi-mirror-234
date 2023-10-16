"""Tornado handlers for the terminal emulator."""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import json
import logging
import signal

from tornado import web
import terminado
import _signal

from snb_node.base.Interceptor import interceptor
from snb_node.tools.tz import utcnow
from snb_node.base.handlers import IPythonHandler
from snb_node.base.zmqhandlers import WebSocketMixin


class TerminalHandler(IPythonHandler):
    """Render the terminal interface."""
    @web.authenticated
    def get(self, term_name):
        self.write(
            self.render_template(
                'terminal.html',
                ws_path=f"terminals/websocket/{term_name}",
            )
        )


class NamedTerminalHandler(IPythonHandler):
    """Creates and renders a named terminal interface."""
    @web.authenticated
    def get(self):
        model = self.terminal_manager.create()
        term_name = model['name']
        new_path = self.request.path.replace("terminals/new", "terminals/" + term_name)
        self.redirect(new_path)


class NewTerminalHandler(IPythonHandler):
    """Creates and renders a terminal interface using the named argument."""
    @web.authenticated
    def get(self, term_name):
        if term_name == 'new':
            raise web.HTTPError(400, "Terminal name 'new' is reserved.")
        new_path = self.request.path.replace(f"new/{term_name}", term_name)
        if term_name in self.terminal_manager.terminals:
            self.set_header('Location', new_path)
            self.set_status(302)
            self.finish(json.dumps(self.terminal_manager.get_terminal_model(term_name)))
            return

        self.terminal_manager.create_with_name(term_name)
        self.redirect(new_path)


class TermSocket(WebSocketMixin, IPythonHandler, terminado.TermSocket):


    def origin_check(self):
        """Terminado adds redundant origin_check

        Tornado already calls check_origin, so don't do anything here.
        """
        return True

    @interceptor
    def get(self, *args, **kwargs) -> {"GRADE": ["BASIC", "PRO", "ENT"], "ROLE": ["ADMIN", "EDITOR"]}:
        args = args[1:]
        if not self.get_current_user():
            raise web.HTTPError(403)
        if not args[0] in self.term_manager.terminals:
            self.term_manager.create_with_name(args[0])
            #raise web.HTTPError(404)
        self.term_name=args[0]
        return super().get(*args, **kwargs)

    def on_message(self, message):
        logging.error("message："+message)
        super().on_message(message)
        self._update_activity()

    def write_message(self, message, binary=False):
        if self.ws_connection is not None:
            super().write_message(message, binary=binary)
            self._update_activity()

    def _update_activity(self):
        self.application.settings['terminal_last_activity'] = utcnow()
        # terminal may not be around on deletion/cull
        if self.term_name in self.term_manager.terminals:
            self.term_manager.terminals[self.term_name].last_activity = utcnow()

    def on_close(self):

        # if self.term_name in self.term_manager.terminals:
        #     logging.info("终端还没有被关闭")
        #     self.term_manager.terminals[self.term_name].send("exit;")
        #     output = self.term_manager.terminals[self.term_name].read()
        #     logging.error("读取到到命令执行" + str(output))
        # else:
        #     logging.info("终端已经被关闭")
        # self.term_manager.terminals[self.term_name].kill()
        # self.session.send(stream, msg)
        # this_term.kill()
        '''if self.term_name in self.term_manager.terminals:
            logging.error("终端还在")
            ## self.term_manager.terminals[self.term_name].kill(signal.SIGKILL)
        else:
            logging.error("终端不在了")


        logging.error("检测是否会调用on_close\n"+str(self.term_name))
        print("TermSocket on_close")'''
        logging.info("我进来了")
        #super().on_message('''["stdin", "exit \r"]''')
        #self.term_manager.terminals.pop(self.term_name)
        if self.term_name in self.term_manager.terminals:
            self.term_manager.terminals[self.term_name].terminate(force=True)
            self.term_manager.terminals.pop(self.term_name)
        logging.info("终端不在了")
