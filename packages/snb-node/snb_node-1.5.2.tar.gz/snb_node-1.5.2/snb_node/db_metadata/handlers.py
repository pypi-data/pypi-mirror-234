# -*- coding: utf-8 -*-
"""
@Time    : 2022/09/15
@Author  : wangxinyi
"""

import json
import traceback
from concurrent.futures import ThreadPoolExecutor

from tornado import gen, web
from jupyter_client.jsonutil import json_default
from snb_plugin.sql.execute_sql import __smartnotebook_getengine_by_conn_id as smartnotebook_getengine_by_conn_id, \
    __connect_test as connect_test, __connect_neo4j_test as connect_neo4j_test ,__connect_mongodb_test as connect_mongodb_test
from snb_plugin.sql.execute_sql import __smartnotebook_engine_list as smartnotebook_engine_list
from sqlalchemy import inspect
import time

from tornado.concurrent import run_on_executor

from snb_node.base.Interceptor import interceptor
from  sqlalchemy.engine.base import Engine

_metaCache={}

def execute_sql_query(engine, sql_query, tag):
    # 执行 SQL 查询
    with engine.connect() as connection:
        result = connection.execute(sql_query)
        db_s = []
        # 获取查询结果
        if tag:
          for row in result:
            db_s.append(row[0])
          return db_s

class DBmetaDataHandler(web.RequestHandler):
    executor = ThreadPoolExecutor(4)
    # @web.authenticated
    @gen.coroutine
    @interceptor
    def get(self, ws_uid, conn_uid) -> {"GRADE": ["BASIC", "PRO", "ENT"], "ROLE": ["ADMIN", "EDITOR"]}:

        try:
            curr_time = time.time()
            refresh = self.get_argument('refresh', '0')
            if refresh=='1' or _metaCache.get(conn_uid) == None or _metaCache.get(conn_uid)['timeout_time'] < curr_time:
                smartnotebook_engine_list.pop(conn_uid, '')
                schema_obj = yield self.getMeatDate(conn_uid)

                res = {"code": 200, "msg": "DB metadata success", "data": schema_obj, "timeout_time": curr_time + 600 }
                _metaCache[conn_uid] = res
            else:
                res = _metaCache.get(conn_uid)
            self.finish(json.dumps(res, default=json_default))
        except Exception as e :
            log = traceback.format_exc()
            print(log)
            res = {"code": 400, "msg": "链接失败", "data": []}
            self.finish(json.dumps(res, default=json_default))

    @run_on_executor
    def getMeatDate(self, conn_uid):
        """
        {
            "name": "privince_gps",
            "type": "table",
            "columns": [
                            {
                        "name": "province",
                        "type": "VARCHAR(35) COLLATE \"utf8_bin\"",
                        "default": "None",
                        "comment": "None",
                        "nullable": "False"
                    },
                ]
        }
        """
        engine = smartnotebook_getengine_by_conn_id(conn_uid, {})
        if engine.__ds_type__ == 'mindsdb':
            dataBases = execute_sql_query(engine, "show  DATABASES;", True)
            schema_obj = []
            for base in dataBases:
                execute_sql_query(engine, "use " + base + ";", False)
                tables = execute_sql_query(engine, "show tables;", True)
                cs_c = []
                for table in tables:
                    cc = {"name": table, "type": "table"}
                    cs_c.append(cc)
                schema_obj.append({'name': base, 'type': 'table', 'columns': cs_c})
            return schema_obj
        elif engine.__ds_type__ == 'mongodb':
            collection_names =engine.list_collection_names()
            # 打印集合列表
            schema_obj = []
            for collection_name in collection_names:
                schema_obj.append({'name': collection_name, 'type': 'table', 'columns': []})
            return schema_obj
        elif isinstance(engine,Engine):
            insp = inspect(engine)
            schema_obj = []
            for tb_name in insp.get_table_names():
                cs = insp.get_columns(tb_name)
                cs_c = []
                for c in cs:
                    cc = {}
                    for k in c:
                        cc[k] = str(c[k])
                    cs_c.append(cc)
                schema_obj.append({'name': tb_name, 'type': 'table', 'columns': cs_c})
            return schema_obj
        else:
            node_info = {"name": "NodeLabels", "type": "table", "columns": []}
            query_graph = engine.execute_query("call db.labels()", database_=engine.default_db)
            for rec in query_graph.records:
                node_info['columns'].append(
                    {"name": rec['label'], "type": "", "default": "", "comment": "", "nullable": ""})

            r_info = {"name": "RelationshipType", "type": "table", "columns": []}
            query_graph = engine.execute_query("""call db.relationshipTypes()""", database_=engine.default_db)
            for rec in query_graph.records:
                r_info['columns'].append(
                    {"name": rec['relationshipType'], "type": "", "default": "", "comment": "", "nullable": ""})

            return  [node_info, r_info]

class DBTestHandler(web.RequestHandler):
    executor = ThreadPoolExecutor(4)

    # @web.authenticated
    @gen.coroutine
    @interceptor
    def post(self, ws_uid) -> {"GRADE": ["BASIC", "PRO", "ENT"], "ROLE": ["ADMIN", "EDITOR"]}:
        try:
            body = self.request.body.strip().decode('utf-8')
            json_body = json.loads(body)
            res_str = yield self.connect_test(json_body)
            res = {"code": 200, "msg": res_str, "data": []}
            self.finish(json.dumps(res, default=json_default))
        except Exception as e :
            res = {"code": 400, "msg": "DB Test:"+str(e), "data": []}
            self.finish(json.dumps(res, default=json_default))

    @run_on_executor
    def connect_test(self, json_body):
        if json_body["ds_type"] == "neo4j":
            return connect_neo4j_test(json_body)
        elif json_body["ds_type"]=="mongodb":
            return connect_mongodb_test(json_body)
        else:
            return connect_test(json_body)

_conn_uid_regex = r"(?P<conn_uid>.*)"
_ws_uid = r"(?P<ws_uid>[^/]+)"
default_handlers = [
    (fr"/api/snb/node/db_metadata/{_ws_uid}/{_conn_uid_regex}", DBmetaDataHandler),
    (fr"/api/snb/node/db_test/{_ws_uid}", DBTestHandler),
]
