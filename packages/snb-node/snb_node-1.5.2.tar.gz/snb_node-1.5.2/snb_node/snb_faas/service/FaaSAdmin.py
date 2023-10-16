#  wangixnyi
# 2022-10-28
import json
from tornado import gen, web
import pandas as pd
import uuid
import time
from ..DbInfo import con
from ..function import init_SNB_FAAS
from ...base.Interceptor import interceptor
from ...config.Config import SNB_SERVER_URL, config
import re
import ast

envir_uid = config.get('workspace', 'envir_uid')

def is_json_valid(json_string):
    try:
        # 尝试解析 JSON 字符串为 Python 对象
        json_object = json.loads(json_string)
        return True
    except json.JSONDecodeError as e:
        # JSON 解析错误，表示 JSON 字符串不合规
        print("JSON 解析错误:", e)
        return False

def has_type_keyword(json_object):
    if isinstance(json_object, dict):
        if "type" in json_object:
            return True
        for value in json_object.values():
            if has_type_keyword(value):
                return True
    elif isinstance(json_object, list):
        for item in json_object:
            if has_type_keyword(item):
                return True
    return False

def extract_http_content(code_str):
    # 解析代码，生成语法树
    tree = ast.parse(code_str)

    # 查找所有函数定义
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.returns and node.returns.value.upper() == 'HTTP':
                # 获取函数的注释部分
                if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Str):
                    comment = node.body[0].value.s.strip()
                    return comment
    return None


class ListHandler(web.RequestHandler):

    @interceptor
    def get(self, ws_uid) -> {"GRADE": ["BASIC", "PRO", "ENT"], "ROLE": ["ADMIN","EDITOR","VIEWER"]}:
        try:
            ws_uid = self.get_argument('ws_uid', '')
            data=pd.read_sql("SELECT * FROM tb_snb_faas_data where ws_uid = '"+ws_uid+"' ORDER BY create_time desc",con)
            data["url"] = SNB_SERVER_URL + "/api/snb/node/faas/Service/" + data["module"]+"?envir_uid="+envir_uid
            data["url_help"] = SNB_SERVER_URL + "/api/snb/node/faas/Service/" + data["module"]+"/help?envir_uid="+envir_uid
            #res=data.to_json(orient='records', force_ascii=False)
            res=data.to_dict(orient='records')
            self.finish(json.dumps({"code":200,"msg":"查询成功!","data":res}))
        except Exception as e:
            print(e)
            self.finish(json.dumps({"code": 200, "msg": "查询成功!", "data": []}))



class CRUDHandler(web.RequestHandler):

    def get(self, ws_uid, faas_uid):
        try:
            data = pd.read_sql("SELECT * FROM tb_snb_faas_data where id = '"+faas_uid+"'", con)
            data["url"] = SNB_SERVER_URL + "/api/snb/node/faas/Service/" + data["module"]+"?envir_uid="+envir_uid
            # res=data.to_json(orient='records', force_ascii=False)
            res = data.to_dict(orient='records')
            self.finish(json.dumps({"code": 200, "msg": "查询成功!", "data": res}))
        except Exception as e:
            print(e)
            self.finish(json.dumps({"code": 200, "msg": "查询成功!", "data": []}))

    @interceptor
    def post(self, ws_uid, faas_uid) -> {"GRADE": ["BASIC", "PRO", "ENT"], "ROLE": ["ADMIN", "EDITOR"]}:
        params = json.loads(self.request.body)
        m=re.findall(r"__MODULE_NAME__[ ]*=[ ]*\"([^\"]+)\"", params["code_str"], re.S)

        if params["code_str"]:
            code_json = params["code_str"]
            http_content = extract_http_content(code_json)
            if http_content:
                if is_json_valid(http_content):
                    data = json.loads(http_content)
                    help_json = json.dumps(data, indent=2)
                    json_object = json.loads(help_json)
                    input_value = json_object.get("input")
                    if not has_type_keyword(input_value):
                        self.finish(json.dumps({"code": 400, "msg": "input 缺少 type 类型", "data": []}))
                else:
                    self.finish(json.dumps({"code": 400, "msg": "json 格式不正确", "data": []}))
                    return
        if len(m)>0:
            params["module"]=re.sub(r"\s+", "", m[0])
            pattern = r'^[a-zA-Z0-9_]+$'
            if re.match(pattern, params["module"]) and len(params["module"]) < 64:
                sql = "insert into tb_snb_faas_data(id,module,code_str,status,create_time,nb_uid,nb_name,cell_uid,ws_uid) values(?,?,?,?,datetime('now'),?,?,?,?)"
                try:
                    cur = con.cursor()
                    cur.execute(sql, (str(uuid.uuid1()),params["module"],params["code_str"],params["status"],params["nb_uid"],params["nb_name"],params["cell_uid"],params["ws_uid"]))  # 执行一条数据的插入
                    con.commit()  # 提交事务，不提交只会执行语句，但没有数据插入
                    print('插入一条数据成功')
                    init_SNB_FAAS(self.application)
                    self.finish(json.dumps({"code": 200, "msg": "增加成功！", "data": {"url": SNB_SERVER_URL + "api/snb/node/faas/Service/" + params["module"]+"/help?envir_uid="+envir_uid}}))
                except Exception as e:
                    if 'UNIQUE constraint failed: tb_snb_faas_data.module' == e.args[0]:
                        self.finish(json.dumps({"code": 400, "msg": m[0]+":__MODULE_NAME__ 已存在", "data": []}))
                    else:
                        print(e)
                        con.rollback()  # 插入失败时回滚
                        print('插入数据失败')
                        self.finish(json.dumps({"code": 400, "msg": str(e), "data":[]}))
                finally:
                    cur.close()  # 关闭游标
            else:
                self.finish(json.dumps({"code": 400, "msg": "__MODULE_NAME__ 长度只允许低于64且只能允许字母数字下划线", "data": []}))
        else:
            self.finish(json.dumps({"code": 400, "msg": "__MODULE_NAME__ 不存在！", "data": []}))

    @interceptor
    def delete(self, ws_uid, faas_uid) -> {"GRADE": ["BASIC", "PRO", "ENT"], "ROLE": ["ADMIN", "EDITOR"]}:
        params = json.loads(self.request.body)
        sql = "delete from tb_snb_faas_data where id = ? and ws_uid=?"
        try:
            cur = con.cursor()
            cur.execute(sql, [params["id"], params["ws_uid"]])  # 执行一条数据的插入
            con.commit()  # 提交事务，不提交只会执行语句，但没有数据插入
        except Exception as e:
            print(e)
            con.rollback()  # 插入失败时回滚
        finally:
            cur.close()  # 关闭游标

        #init_SNB_FAAS(self.application)
        application_copy_list = self.application.default_router.rules.copy()
        for rule in application_copy_list:
            copy_list = rule.target.rules.copy()
            for ru in copy_list:
                if hasattr(ru,"regex"):
                    if ru.regex.pattern == '/api/snb/node/faas/Service/'+params["module"]+'$':
                        rule.target.rules.pop(rule.target.rules.index(ru))
                    if ru.regex.pattern == '/api/snb/node/faas/Service/'+params["module"]+'/help$':
                        rule.target.rules.pop(rule.target.rules.index(ru))
            if len(rule.target.rules) == 0:
                self.application.default_router.rules.pop(self.application.default_router.rules.index(rule))
        #print(dir(self.application))
        self.finish(json.dumps({"code":200,"msg": "删除成功！","data":[]}))

_faas_uid_regex = r"(?P<faas_uid>.*)"
_ws_uid = r"(?P<ws_uid>.*)"
default_handlers = [
    (fr"/api/snb/node/faas/list/{_ws_uid}", ListHandler),
    (fr"/api/snb/node/faas/admin/{_ws_uid}/{_faas_uid_regex}", CRUDHandler),
]
