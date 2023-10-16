# coding=utf-8
"""
@Modify Time :2023/6/11 11:28    
@Author      :tao.chen 
"""


import json
import re
import random
import time
from collections import namedtuple
import openai
from tornado import gen, web
from jinja2 import Template
from sqlalchemy.engine.base import Engine
from sqlalchemy import inspect
from jupyter_client.jsonutil import json_default
from jupyter_client import find_connection_file
from jupyter_client.blocking import BlockingKernelClient
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from snb_plugin.sql.execute_sql import __smartnotebook_getengine_by_conn_id as smartnotebook_getengine_by_conn_id
from snb_plugin.utils.snb_uuid import uuid1
from snb_node.base.Interceptor import interceptor


record_path = "/home/.config/chat_record.txt"
# record_path = "/Users/taochen/SmartNotebook/snb/chat_record.txt"

prompt_template = namedtuple("prompt_template", ["python", "sql"])(
    python={
        "generate": "{{prompt}}，只输出python代码",
        "fix": "Python代码如下：\n{{content}}\n上述python代码报错{{prompt}},修复上述代码报错问题，输出修复后的python代码",
        "edit": "Python代码如下：\n{{content}}\n操作：{{prompt}}，只输出python代码\n修改后的python代码：",
        "explain": "Python代码如下：\n{{content}}\n操作：添加注释来解释上述python代码",
    },
    sql={
        "generate": "{{prompt}}，以MarkDown形式输出SQL语句\n",
        "fix": "SQl语句如下：\n{{content}}\n上述SQL语句报错{{prompt}}，修复以上SQL语句\n以MarkDown形式输出修复后的SQL语句",
        "edit": "SQl语句如下：\n{{content}}\n操作：针对上述SQL按要求进行修改，要求是：{{prompt}}，以MarkDown形式输出修改后的SQL语句\n修改后的SQL语句：",
        "explain": "SQl语句如下：\n{{content}}\n操作：添加注释来解释上述SQL语句",
    },
)


class create_client:
    """
    连接kernel，获取上下文，需要kernel
    kernel - "/root/.local/share/jupyter/runtime/kernel-{kernel_uid}.json"
    """

    def __init__(self, kernel):
        self.kernel = kernel

    def __enter__(self):
        # 找到连接文件路径
        connection_file = find_connection_file(
            # kernel_name="/root/.local/share/jupyter/runtime/kernel-debf0b32-2676-41ff-8cdd-d2f8b7a04ba1.json"
            filename=self.kernel
        )
        # 创建内核客户端并连接到内核
        self.kernel_client = BlockingKernelClient(connection_file=connection_file)
        self.kernel_client.load_connection_file()
        self.kernel_client.start_channels()
        return self

    def get_msg(self, execute_code):
        # 执行代码并获取结果
        # code_to_execute = """print('aaa')"""
        msg_id = self.kernel_client.execute(execute_code)
        # 获取结果
        outputs = []
        while True:
            try:
                msg = self.kernel_client.get_iopub_msg(timeout=1)  # 设置适当的超时时间
                if msg["parent_header"]["msg_id"] != msg_id:
                    continue
                msg_type = msg["header"]["msg_type"]
                content = msg["content"]
                if msg_type == "stream" and content["name"] == "stdout":
                    output_text = content["text"]
                    outputs.append(output_text)
                elif msg_type == "execute_result":
                    result = content["data"]["text/plain"]
                    outputs.append(result)
                elif msg_type == "error":
                    error_message = content["evalue"]
                    outputs.append(f"Error: {error_message}")
            except Exception as e:
                break
        return outputs

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 关闭内核客户端
        self.kernel_client.stop_channels()


class ChatGPTV2DemoHandler(web.RequestHandler):
    executor = ThreadPoolExecutor(4)

    @gen.coroutine
    # @interceptor
    def post(self, ws_uid) -> {"GRADE": ["BASIC", "PRO", "ENT"], "ROLE": ["ADMIN", "EDITOR"]}:
        try:
            body = self.request.body.strip().decode("utf-8")
            self.json_body = json.loads(body)
            conversation_id = self.json_body.get("conversation_id")
            if conversation_id is None or conversation_id == "":
                # conversation_id = "1234"
                conversation_id = uuid1()

            """
            # 获取参数，判断generate,fix,explain,edit,代码类型sql，python
            prompt, content = json_body["prompt"], json_body["content"]
            kernel_id = json_body["kernelId"]
            gpt_type = json_body.get("type", "generate").lower()
            code_type = json_body.get("code_type", "python").lower()
            db_uid = json_body.get("dbId")
            """

            # explain，fix时prompt允许为空
            if self.json_body["type"] not in ("explain", "fix") and self.json_body["prompt"].strip() in ("", None):
                raise Exception("prompt参数为空")

            prompt = yield self.prompt_engineer(
                code_type=self.json_body["code_type"],
                db_type=self.json_body.get("db_type"),
            )

            # if self.json_body["code_type"] == "python":
            #     response = yield self.run_model(
            #         prompt=prompt,
            #         sql=False if self.json_body["code_type"] == "python" else True,
            #         explain=False if self.json_body["type"] != "explain" else True,
            #     )
            # else:
            #     # sql demo写死
            #     response = yield self.get_demo_response(prompt)
            response = yield self.run_model(
                prompt=prompt,
                sql=False if self.json_body["code_type"] == "python" else True,
                explain=False if self.json_body["type"] != "explain" else True,
            )

            # 响应中取出结果,去掉开头和结尾的换行符
            # res_msg = response["choices"][0]["text"].lstrip()
            res_msg = response["choices"][0]["message"]["content"].lstrip()

            matches = (
                re.findall(
                    rf"```[^\n]+\n(.*?)```",
                    res_msg,
                    re.DOTALL,
                )
                if self.json_body["type"] not in ("explain",)
                else []
            )

            # 记录
            yield self.record(prompt=prompt, response=res_msg)
            res_str = {"conversation_id": conversation_id, "message": res_msg if matches == [] else "\n".join(matches)}
            res = {"code": 200, "msg": "成功", "data": res_str}
            self.finish(json.dumps(res, default=json_default))
        except Exception as e:
            print(e)
            res = {"code": 400, "msg": "失败:" + str(e), "data": []}
            self.finish(json.dumps(res, default=json_default))

    @run_on_executor
    def get_demo_response(self, prompt):
        """
        拼接后的prompt计算编辑距离返回对应的response
        Args:
            prompt : 拼接后的prompt
        Returns:

        """

        # 计算编辑距离
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

        with open("snb_node/chatgptv2/chatDemo.json", mode="rt", encoding="utf8") as chat_demo:
            demo_data = json.loads(chat_demo.read())
        min_v = 25
        min_o = demo_data.get("chat_messages")[0]
        for msg in demo_data.get("chat_messages"):
            dd = edit_distance(msg["requests"], prompt)
            if min_v > dd:
                min_v = dd
                min_o = msg
        time.sleep(random.randint(1, 3))
        return min_o["response"]

    @run_on_executor
    def run_model(self, prompt, **kwargs):
        """
        调用微软云code-davinci-002模型
        Args:
            prompt: prompt
        Return:
            {
                "id": "cmpl-4kGh7iXtjW4lc9eGhff6Hp8C7btdQ",
                "object": "text_completion",
                "created": 1646932609,
                "model": "ada",
                "choices": [
                    {
                        "text": ", a dark line crossed",
                        "index": 0,
                        "logprobs": null,
                        "finish_reason": "length"
                    }
                ]
            }
        """
        # azure openaiapi
        openai.api_type = "azure"
        openai.api_base = "https://smartnotebook.openai.azure.com/"
        openai.api_version = "2023-03-15-preview"
        openai.api_key = "937aa41b8916473693d737617bac0a6f"

        # 模型参数
        model_params = {
            "engine": "gpt35",
            "prompt": prompt,
            "temperature": 0.1,
            "max_tokens": 256,
            "top_p": 1,
            "frequency_penalty": 1,
            "presence_penalty": 0.3,
            "stop": None if kwargs.get("explain")
            # else ['"""', "'''", "#"]
            else ["#", "<|im_sep|>"] if not kwargs.get("sql") else [";", "/*", "<|im_sep|>"],
        }

        # 调用模型 gpt35 0315
        # response = openai.Completion.create(**model_params)

        # 调用模型 gpt35 0613
        response = openai.ChatCompletion.create(
            # engine="gpt0613",
            engine="gpt35",
            messages=[
                {"role": "system", "content": "You are an code AI assistant that helps people write code"},
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.1,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=1,
            presence_penalty=0.3,
            stop=None,
        )
        return response

    @run_on_executor
    def prompt_engineer(self, code_type: str, *args, **kwargs):
        """
        根据代码类型和数据源类型拼接prompt
        Args:
            code_type : 代码类型 python| sql
            kwargs : db_type数据源类型，默认为None，code_type为sql时必传
        Returns:
            返回对应拼接的prompt
        """
        prompt = self.json_body["prompt"]
        variable_in_prompt = re.findall(r"\{\{(.*?)\}\}", prompt)

        if not variable_in_prompt:
            prompt = Template(getattr(prompt_template, self.json_body["code_type"])[self.json_body["type"]]).render(
                prompt=prompt, content=self.json_body.get("content", "")
            )
            return prompt + "\n"

        if code_type == "python":
            kernel_id = self.json_body.get("kernelId")
            df_info, is_dataframe = self.get_dataframe_columns(
                kernel_id=kernel_id, variable_in_prompt=variable_in_prompt
            )

            variable_dic = {
                var: var if not is_dataframe.get(var) else f"{var}(列名：{df_info[var]['name']})".strip()
                for var in variable_in_prompt
            }

        else:
            conn_uid = self.json_body.get("dbId")
            db_type = kwargs.get("db_type")

            # {{table_name}} 位置提到prompt最前面，并把原来的替换
            for i in zip(re.findall(r"(\{\{.*?\}\})", prompt), variable_in_prompt):
                prompt = f"{i[0]}," + prompt.replace(*i)

            if db_type == "dfsql":
                kernel_id = self.json_body.get("kernelId")
                df_info, is_dataframe = self.get_dataframe_columns(
                    kernel_id=kernel_id, variable_in_prompt=variable_in_prompt
                )
                variable_dic = {
                    var: "" if not is_dataframe.get(var) else f"有一张表{var}，字段名：{df_info[var]['name']}"
                    for var in variable_in_prompt
                }
            else:
                column_info, in_database = self.get_table_columns(
                    conn_uid=conn_uid, variable_in_prompt=variable_in_prompt
                )
                # 将返回的表结构以prompt进行拼装
                # 返回prompt中对应变量的替换字典
                variable_dic = {
                    var: ""
                    if not in_database.get(var)
                    else f"有一张表{var}，字段名：{column_info[var]['name']}，字段注释：{column_info[var]['comment']}"
                    for var in variable_in_prompt
                }

        prompt = Template(getattr(prompt_template, self.json_body["code_type"])[self.json_body["type"]]).render(
            prompt=Template(prompt).render(**variable_dic), content=self.json_body.get("content", "")
        )
        return prompt + "\n"

    @staticmethod
    def get_table_columns(conn_uid: str, *args, **kwargs):
        """
        数据库连接根据表名获取列
        Args:
            conn_uid: 数据库连接uid
        Returns:
            prompt中变量的字典
        """
        engine = smartnotebook_getengine_by_conn_id(conn_uid, {})
        insp = inspect(engine)
        variable_in_prompt = kwargs.get("variable_in_prompt", [])
        column_info = dict()

        in_database = {var: True if var in insp.get_table_names() else False for var in variable_in_prompt}
        # 解析prompt中的变量
        column_info = {
            var: var
            if not in_database.get(var)
            else {
                key: [col[key] if key != "type" else str(col[key]) for col in insp.get_columns(var)]
                for key in ["name", "comment", "type"]
            }
            for var in variable_in_prompt
        }

        return column_info, in_database

    @staticmethod
    def get_dataframe_columns(kernel_id: str, *args, **kwargs):
        """
        使用jinja2替换输入的prompt
        Args:
            kernel_id : notebook kernel id
        Return:
            prompt中变量的字典
        """
        variable_in_prompt = kwargs.get("variable_in_prompt")
        # 从prompt中提取变量，从kernel中取变量值
        kernel_id = f"/root/.local/share/jupyter/runtime/kernel-{kernel_id}.json"
        with create_client(kernel_id) as client:
            variable_in_kernel = json.loads(client.get_msg("print(_snb_var_list())")[0])
            is_dataframe = {i["varName"]: i["varType"] == "DataFrame" for i in variable_in_kernel}

            df_info = {
                var: var
                if not is_dataframe.get(var)
                else {key: client.get_msg(f"print(list({var}.columns))")[0].strip() for key in ["name"]}
                for var in variable_in_prompt
            }
        return df_info, is_dataframe

    @run_on_executor
    def record(self, prompt, response):
        """记录prompt和response"""

        # print("prompt:\n", prompt)
        # print("response:\n", response)
        with open(record_path, mode="at", encoding="utf-8") as record_file:
            record_file.write(str({"prompt": prompt, "response": response}) + "\n")


_conn_uid_regex = r"(?P<conn_uid>.*)"
_ws_uid = r"(?P<ws_uid>[^/]+)"
default_handlers = [
    (rf"/api/snb/node/aigc/chatgptv2/{_ws_uid}", ChatGPTV2DemoHandler),
]
