# -*- coding: utf-8 -*-
"""
@Time    : 2022/09/15
@Author  : wangxinyi
"""
import json
import time

from revChatGPT.V1 import Chatbot
from tornado import gen, web
from jupyter_client.jsonutil import json_default
import openai
import datetime
from snb_plugin.utils.snb_uuid import uuid1
import markdown
from concurrent.futures import ThreadPoolExecutor

from sshtunnel import SSHTunnelForwarder

from snb_plugin.jinjasql import JinjaSql
from tornado.concurrent import run_on_executor

from snb_node.base.Interceptor import interceptor

# ssh_host = "174.137.58.98"  # 堡垒机ip地址或主机名
# ssh_port = 29199  # 堡垒机连接mysql服务器的端口号，一般都是22，必须是数字
# ssh_user = "root"  # 这是你在堡垒机上的用户名
# ssh_password = "jHL3w3m5Fxag"  # 这是你在堡垒机上的用户密码
# mysql_host = "127.0.0.1"  # 这是你mysql服务器的主机名或ip地址
# mysql_port = 3128  # 这是你mysql服务器上的端口，3306，mysql就是3306，必须是数字
# server = SSHTunnelForwarder(
#     ssh_address_or_host=(ssh_host, ssh_port),
#     ssh_username=ssh_user,
#     ssh_password=ssh_password,
#     remote_bind_address=(mysql_host, mysql_port),
#     local_bind_address=("0.0.0.0", 63333),
# )
# try:
#     # server.start()
#     pass
# except Exception as e:
#     print(e)

ssh_host = "139.196.49.140"  # 堡垒机ip地址或主机名
ssh_port = 1022  # 堡垒机连接mysql服务器的端口号，一般都是22，必须是数字
ssh_user = "root"  # 这是你在堡垒机上的用户名
ssh_password = "!dJHqnIq8AYw"  # 这是你在堡垒机上的用户密码
mysql_host = "rm-uf6k8l12ozqc2sjtq.mysql.rds.aliyuncs.com"  # 这是你mysql服务器的主机名或ip地址
mysql_port = 3306  # 这是你mysql服务器上的端口，3306，mysql就是3306，必须是数字
server = SSHTunnelForwarder(
    ssh_address_or_host=(ssh_host, ssh_port),
    ssh_username=ssh_user,
    ssh_password=ssh_password,
    remote_bind_address=(mysql_host, mysql_port),
    local_bind_address=("0.0.0.0", 63333),
)
try:
    server.start()
    # print(123)
    pass
except Exception as e:
    print(e)

_SNB_chatGPT_INFO = {}


class GPTAPIHandler(web.RequestHandler):
    # @web.authenticated
    @gen.coroutine
    def post(self):
        try:
            body = self.request.body.strip().decode("utf-8")
            json_body = json.loads(body)
            prompt_content = json_body["content"]
            conversation_id = json_body.get("conversation_id")
            if conversation_id is None or conversation_id == "":
                conversation_id = uuid1()
            msg_info = _SNB_chatGPT_INFO.get(conversation_id)
            if msg_info:
                pass
            else:
                msg_info = []

            msg_info.append({"role": "user", "content": prompt_content})

            openai.api_key = "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"
            openai.proxy = "http://127.0.0.1:63333"
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=msg_info)

            print(response["choices"][0]["message"]["role"])
            print(response["usage"]["total_tokens"])

            msg_info.append({"role": "assistant", "content": response["choices"][0]["message"]["content"]})
            _SNB_chatGPT_INFO[conversation_id] = msg_info

            res_str = {
                "conversation_id": conversation_id,
                "message": {
                    "requst_message": {
                        "id": response["id"],
                        "author": {"role": "user", "name": "WXY"},
                        "create_time": datetime.datetime.fromtimestamp(response["created"]).strftime(
                            "%Y-%m-%d %H:%M:%S.%f"
                        ),
                        "content": {"content_type": "text", "parts": [prompt_content]},
                    },
                    "response_message": [
                        {
                            "id": response["id"],
                            "author": {"role": "assistant", "name": "chatGPT"},
                            "create_time": datetime.datetime.fromtimestamp(response["created"]).strftime(
                                "%Y-%m-%d %H:%M:%S.%f"
                            ),
                            "content": {
                                "content_type": "text",
                                "parts": [response["choices"][0]["message"]["content"]],
                            },
                            "html_content": {
                                "content_type": "html",
                                "parts": [
                                    markdown.markdown(
                                        response["choices"][0]["message"]["content"],
                                        extensions=["snb_plugin.snb_aigc.snb_fenced_code:FencedCodeExtension"],
                                    )
                                ],  # extensions=['fenced_code']    )]
                            },
                        }
                    ],
                },
            }
            res = {"code": 200, "msg": "成功", "data": res_str}
            self.finish(json.dumps(res, default=json_default))
        except Exception as e:
            res = {"code": 400, "msg": "失败:" + str(e), "data": []}
            self.finish(json.dumps(res, default=json_default))


_chatbot = None


class ChatGPTHandler(web.RequestHandler):
    # @web.authenticated
    @gen.coroutine
    def post(self):
        try:
            body = self.request.body.strip().decode("utf-8")
            json_body = json.loads(body)
            prompt_content = json_body["content"]
            conversation_id = json_body.get("conversation_id")
            global _chatbot
            if _chatbot is None:
                _chatbot = Chatbot(
                    config={
                        "email": "wangxinyi@smartnotebook.tech",
                        "password": "wxyyouopenAI@SNB123890",
                        "proxy": "http://127.0.0.1:63333",
                    }
                )
            if conversation_id and conversation_id != "":
                for data in _chatbot.ask(prompt_content, conversation_id=conversation_id):
                    response = data["message"]
            else:
                for data in _chatbot.ask(prompt_content):
                    response = data["message"]
                    conversation_id = data["conversation_id"]

            print("conversation_id:", conversation_id)
            print("response message:", response)
            html_str = markdown.markdown(
                response, extensions=["snb_plugin.snb_aigc.snb_fenced_code:FencedCodeExtension"]
            )
            # html_str="dd"
            print(html_str)

            res_str = {
                "conversation_id": conversation_id,
                "message": {
                    "requst_message": {
                        "id": data["parent_id"],
                        "author": {"role": "user", "name": "WXY"},
                        "create_time": datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()).strftime(
                            "%Y-%m-%d %H:%M:%S.%f"
                        ),
                        "content": {"content_type": "text", "parts": [prompt_content]},
                    },
                    "response_message": [
                        {
                            "id": data["parent_id"],
                            "author": {"role": "assistant", "name": "chatGPT"},
                            "create_time": datetime.datetime.fromtimestamp(
                                datetime.datetime.now().timestamp()
                            ).strftime("%Y-%m-%d %H:%M:%S.%f"),
                            "content": {"content_type": "text", "parts": [response]},
                            "html_content": {
                                "content_type": "html",
                                "parts": [html_str],  # extensions=['fenced_code']    )]
                            },
                        }
                    ],
                },
            }
            res = {"code": 200, "msg": "成功", "data": res_str}
            self.finish(json.dumps(res, default=json_default))
        except Exception as e:
            print(e)
            res = {"code": 400, "msg": "失败:" + str(e), "data": []}
            self.finish(json.dumps(res, default=json_default))


import json
import random


def edit_distance(str1, str2):
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]


class ChatGPTDemoHandler(web.RequestHandler):
    executor = ThreadPoolExecutor(4)

    @gen.coroutine
    @interceptor
    def post(self, ws_uid) -> {"GRADE": ["BASIC", "PRO", "ENT"], "ROLE": ["ADMIN", "EDITOR"]}:
        try:
            body = self.request.body.strip().decode("utf-8")
            json_body = json.loads(body)
            prompt_content = json_body["content"]
            conversation_id = json_body.get("conversation_id")
            if conversation_id is None or conversation_id == "":
                conversation_id = uuid1()

            with open("snb_node/chatgptapi/chatGptdemo01.json", "r", encoding="utf8") as fp:
                obj_all = json.load(fp)
            yield self.sleep()

            min_v = 10
            min_o = obj_all.get("chat_messages")[0]
            for msg in obj_all.get("chat_messages"):
                dd = edit_distance(msg["requst_message"]["content"]["parts"][0], prompt_content)
                if min_v > dd:
                    min_v = dd
                    min_o = msg

            res_str = {"conversation_id": conversation_id, "message": min_o}
            res = {"code": 200, "msg": "成功", "data": res_str}
            self.finish(json.dumps(res, default=json_default))
        except Exception as e:
            print(e)
            res = {"code": 400, "msg": "失败:" + str(e), "data": []}
            self.finish(json.dumps(res, default=json_default))

    @run_on_executor
    def sleep(self):
        time.sleep(0.0 + random.randint(2, 5))


from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
import os

os.environ["OPENAI_API_KEY"] = "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"
# openai.api_key = "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"

_langchain_agent = None


class langChainHandler(web.RequestHandler):
    # @web.authenticated
    @gen.coroutine
    def post(self, ws_uid):
        try:
            body = self.request.body.strip().decode("utf-8")
            json_body = json.loads(body)
            prompt_content = json_body["content"]
            conversation_id = json_body.get("conversation_id")
            global _langchain_agent
            if _langchain_agent is None:
                _langchain_agent = create_csv_agent(OpenAI(temperature=0), "/home/gdpData.csv", verbose=False)

            openai.proxy = "http://127.0.0.1:63333"
            response = _langchain_agent.run(prompt_content)

            if conversation_id and conversation_id != "":
                pass
            else:
                conversation_id = uuid1()

            print("conversation_id:", conversation_id)
            print("response message:", response)
            html_str = markdown.markdown(
                response, extensions=["snb_plugin.snb_aigc.snb_fenced_code:FencedCodeExtension"]
            )
            # html_str="dd"
            print(html_str)

            res_str = {
                "conversation_id": conversation_id,
                "message": {
                    "requst_message": {
                        "id": uuid1(),
                        "author": {"role": "user", "name": "WXY"},
                        "create_time": datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()).strftime(
                            "%Y-%m-%d %H:%M:%S.%f"
                        ),
                        "content": {"content_type": "text", "parts": [prompt_content]},
                    },
                    "response_message": [
                        {
                            "id": uuid1(),
                            "author": {"role": "assistant", "name": "chatGPT"},
                            "create_time": datetime.datetime.fromtimestamp(
                                datetime.datetime.now().timestamp()
                            ).strftime("%Y-%m-%d %H:%M:%S.%f"),
                            "content": {"content_type": "text", "parts": [response]},
                            "html_content": {
                                "content_type": "html",
                                "parts": [html_str],  # extensions=['fenced_code']    )]
                            },
                        }
                    ],
                },
            }
            res = {"code": 200, "msg": "成功", "data": res_str}
            self.finish(json.dumps(res, default=json_default))
        except Exception as e:
            print(e)
            res = {"code": 400, "msg": "失败:" + str(e), "data": []}
            self.finish(json.dumps(res, default=json_default))


_conn_uid_regex = r"(?P<conn_uid>.*)"
_ws_uid = r"(?P<ws_uid>[^/]+)"
default_handlers = [
    # (fr"/api/snb/node/aigc/chatgpt/{_ws_uid}", langChainHandler),
    (rf"/api/snb/node/aigc/chatgpt/{_ws_uid}", ChatGPTDemoHandler),
    # (fr"/api/snb/node/aigc/chatgpt", ChatGPTHandler),
]
