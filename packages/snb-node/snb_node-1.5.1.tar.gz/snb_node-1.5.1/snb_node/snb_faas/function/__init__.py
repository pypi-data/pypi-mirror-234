#  wangixnyi
# 2022-10-28
import functools
import tornado
import tornado.web
from jupyter_client.jsonutil import json_default

from snb_node.snb_faas.function import _function_registry
from ..DbInfo import con
import pandas as pd
import os
import yaml, json
import inspect
from ...config.Config import SNB_SERVER_URL, config
import re

envir_uid = config.get('workspace', 'envir_uid')


MAX_CONTENT_LENGTH = 10 * 1024 * 1024

class Snb_FaaS_Handler(tornado.web.RequestHandler):


    SUPPORTED_METHODS = ['GET', 'POST', 'CONNECT','DELETE','PUT']

    def initialize(self, snb_function):
        self.snb_function = snb_function

    def compute_etag(self):
        return None  # disable tornado Etag

    #@snb_authenticated
    async def get(self):
        errorJson = ""
        p_fun = inspect.getfullargspec(self.snb_function)
        body_json = json.loads(self.request.body)
        args_list = p_fun.args
        re_list = []
        defaults_v = p_fun.defaults
        for x in p_fun.args:
            x_type = p_fun.annotations.get(x, str)
            r_index = args_list.index(x)
            is_defult = False
            default_v = None
            if defaults_v:
                if r_index >= len(args_list) - len(defaults_v):
                    is_defult = True
                    default_v = defaults_v[r_index - len(args_list) + len(defaults_v)]
            # print(x_type==int,is_defult,default_v,x_type)

            if x in body_json or is_defult == True:
                if x in body_json:
                    val = body_json[x]
                else:
                    val = default_v
                if x_type == str:
                    if is_defult:
                        re_list.append("%s='%s'" % (x, val))
                    else:
                        re_list.append("'%s'" % val)
                else:
                    if is_defult:
                        re_list.append("%s=%s" % (x, val))
                    else:
                        re_list.append("%s" % val)
            else:
                data = {"code": "400"}
                '''if str(args_list) in body_json or len(body_json) > 0:
                    date["error"] = "参数不对"
                    return self.write(json.dumps(date, ensure_ascii=False))'''
                data["error"] = "参数不全"
                return self.write(json.dumps(data, ensure_ascii=False))
        fun_str = "%s(%s)" % ('self.snb_function', ','.join(re_list))
        obj = eval(fun_str)
        data = {"code": "200"}
        if obj is not None:
            data["data"] = obj
            self.write(json.dumps(data, default=json_default))

    #@snb_authenticated
    async def post(self):
        return await self.get()

    #@snb_authenticated
    async def put(self):
        return await self.get()

    #@snb_authenticated
    async def delete(self):
        return await self.get()

class Snb_Help_Handler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ['GET', 'POST', 'CONNECT','DELETE','PUT']

    def initialize(self, snb_function, snb_function_doc, path):
        self.snb_function = snb_function
        self.path = path
        self.snb_function_doc = snb_function_doc

    def compute_etag(self):
        return None  # disable tornado Etag

    #@snb_authenticated
    async def get(self):
        path_ = self.path + "?envir_uid=" + envir_uid
        defult_json_head = {"swagger": "2.0",
                            "info": {"title": "SmartNotebook API", "description": "Swagger API definition",
                                     "version": "1.0"}, "basePath": "/", "schemes": ["http"], "definitions": {},
                            "parameters": {},
                            "paths": {"/api/snb/node/faas/Service/" + path_ + "": {
                                "post": {"tags": [self.snb_function.__name__], "summary": "", "description": "",
                                         "produces": ["application/json"],
                                         "parameters": [{"in": "body", "name": "body", "description": "post data",
                                                         "required": True, "schema": {
                                                 "type": "object", "properties": {}
                                             }}],
                                         "responses": {"200": {"description": "请求成功", "schema": {"type": "object",
                                                                                                 "properties": {
                                                                                                     "code": {
                                                                                                         "type": "integer",
                                                                                                         "default": 200},
                                                                                                     "msg": {
                                                                                                         "type": "string",
                                                                                                         "default": ""},
                                                                                                     "data": {"properties":None,"type":"object"}}}},
                                                       "400": {"description": "请求失败", "schema": {"type": "object",
                                                                                                 "properties": {
                                                                                                     "code": {
                                                                                                         "type": "integer",
                                                                                                         "default": 400},
                                                                                                     "msg": {
                                                                                                         "type": "string",
                                                                                                         "default": "参数异常"}}}}}
                                         }}}}
        #如果是空 则说明是默认 python 0527
        if self.snb_function_doc:
            _doc = self.snb_function_doc

            json_object = json.loads(_doc)

            input_json = json_object.get("input")
            output_json = json_object.get("output")
            start = _doc.find("input=")
            end = _doc.find("output=")
            if input_json:
                defult_json_head["paths"]["/api/snb/node/faas/Service/" + path_ + ""]["post"]["parameters"][0][
                    "schema"][
                    "properties"] = json.loads(json.dumps(input_json, ensure_ascii=False))
            if output_json:
                defult_json_head["paths"]["/api/snb/node/faas/Service/" + path_ + ""]["post"]["responses"]["200"]["schema"][
                    "properties"]["data"]["properties"] = json.loads(json.dumps(output_json, ensure_ascii=False))
            self.write(json.dumps(defult_json_head, ensure_ascii=False))
        else:
            p_fun = inspect.getfullargspec(self.snb_function)
            args_list = p_fun.args
            defaults_v = p_fun.defaults
            argsJson = {}
            # defaults_v 是空则没有默认值
            for x in p_fun.args:
                x_type = p_fun.annotations.get(x, str)
                r_index = args_list.index(x)
                is_defult = False
                default_v = None
                types = 'str int bool list dict'
                if defaults_v:
                    if r_index >= len(args_list) - len(defaults_v):
                        is_defult = True
                        default_v = defaults_v[r_index - len(args_list) + len(defaults_v)]

                if isinstance(x_type, type):
                    _type = x_type.__name__
                    if _type in types:
                        type_ = ""
                        if x_type == str:
                            type_ = "String"
                        elif x_type == int:
                            type_ = "int"
                        elif x_type == bool:
                            type_ = "bool"
                        elif x_type == list:
                            type_ = "list"
                        elif x_type == dict:
                            type_ = "dict"
                        if is_defult:
                            argsJson[x] = {
                                "type": type_,
                                "default": default_v
                            }
                        else:
                            argsJson[x] = {
                                "type": type_,
                                "default": None
                            }
                else:
                    print(str(p_fun.annotations[x]))


            defult_json_head["paths"]["/api/snb/node/faas/Service/" + path_ + ""]["post"]["parameters"][0]["schema"][
                "properties"] = json.loads(json.dumps(argsJson, ensure_ascii=False))
            self.write(json.dumps(defult_json_head, ensure_ascii=False))
    #@snb_authenticated
    async def post(self):
        return await self.get()

    #@snb_authenticated
    async def put(self):
        return await self.get()

    #@snb_authenticated
    async def delete(self):
        return await self.get()

def create_FaaS(app,source=None, temp_dir="/home/.config/functions-framework/"):
    source_modules=[]
    for src in source:
        module=src.get("module")
        file_tmp=temp_dir+module+".py"
        with open(file_tmp,"w",encoding="utf8") as sp:
            sp.write(src.get("code_str"))
        source_module, spec = _function_registry.load_function_module(file_tmp)
        source_modules.append({"source_module":source_module,"spec":spec,"module":module,"file_tmp":file_tmp})
        # Handle log severity backwards compatibility
    for sm in source_modules:
        try:
            sm["spec"].loader.exec_module(sm["source_module"])
            sm["function"] = _function_registry.get_user_function(sm["file_tmp"], sm["source_module"])
            app.add_handlers(r".*", [
                tornado.web.url(r"/api/snb/node/faas/Service/"+sm["module"], Snb_FaaS_Handler,kwargs=dict(snb_function=sm["function"]['HTTP'])),
                tornado.web.url(r"/api/snb/node/faas/Service/"+sm["module"]+"/help", Snb_Help_Handler,kwargs=dict(snb_function=sm["function"]['HTTP'], snb_function_doc=sm["function"]['HTTP'].__doc__,
                                                                                                                  path=sm["module"]))
            ])
        except Exception as e:
            print(e)

def init_SNB_FAAS(app):
    data = pd.read_sql("SELECT * FROM tb_snb_faas_data where status=1 ORDER BY create_time desc", con)
    source = data.to_dict(orient='records')
    temp_dir = "/home/.config/functions-framework/"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    create_FaaS(app,source, temp_dir=temp_dir)
