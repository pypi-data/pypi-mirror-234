import json
import traceback

from apscheduler.triggers.cron import CronTrigger
from tornado import gen, web
from jupyter_client.jsonutil import json_default

from snb_node.base.Interceptor import interceptor
from snb_node.exec_snb.SnbScheduler import scheduler
from snb_node.exec_snb.ExecuteSnb import  ExecuteSnb
import sys
import snb_plugin.utils.snb_RSA as snb_rsa
from snb_node.config.Config import SNB_SERVER_URL, config, pem, workspace_uid, envir_uid
import requests
from schema import Schema, And, Use, Optional, SchemaError, Regex

class setSchedulerHandler(web.RequestHandler):

    def recall(self,aciton,nb_uid):
        url_path="/api/snb_native/SchedulerRecall/%s/%s"
        url = ''.join([SNB_SERVER_URL,url_path]) % (aciton, nb_uid)
        sign_str = snb_rsa.sign(url_path % (aciton, nb_uid), pem)
        header = {"Cookie": "cookie", "sign": sign_str, "workspaceUid": workspace_uid}
        conn_info = requests.get(url, headers=header)
        print(conn_info.text)
        resp = conn_info.json()
        if resp["code"] == 200:
            return True
        else:
            return False


    # @web.authenticated
    @gen.coroutine
    @interceptor
    def get(self, ws_uid, nb_uid) -> {"GRADE": ["BASIC", "PRO", "ENT"], "ROLE": ["ADMIN", "EDITOR", "VIEWER"]}:
        try:
            if nb_uid=='list':
                data = []
                jobs = scheduler.get_jobs()
                keyword = self.get_argument('keyword','')
                ws_uid = self.get_argument('ws_uid', '')
                envirUid = self.get_argument('envir_uid', '')
                for job in jobs:
                    if job.next_run_time:
                        next_run_time = job.next_run_time.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        next_run_time=None
                    if job.kwargs["ws_uid"] == ws_uid and job.kwargs["envir_uid"] == envirUid:
                        job_info={"nb_uid": job.id, "nb_name": job.name, "cron": str(job.trigger), 'pending': job.pending,
                         "paused": job.next_run_time == None, "next_run_time": next_run_time, "custom_cron":job.kwargs["custom_cron"],
                                  "last_time": job.kwargs["last_time"],"last_status":job.kwargs["last_status"] ,"last_msg":job.kwargs["last_msg"]            }
                        if len(job.args) > 2:
                            job_info['success_email']=job.args[1]
                            job_info['fail_email']=job.args[2]
                        if keyword == '':
                            data.append(job_info)
                        elif job_info['nb_name'].__contains__(keyword):
                            data.append(job_info)

                res = {"code": 200, "msg": "查询调度信息成功", "data": data}
                self.finish(json.dumps(res, default=json_default))
            else:
                res = {}
                job = scheduler.get_job(nb_uid)
                ws_uid = self.get_argument('ws_uid', '')
                envirUid = self.get_argument('envir_uid', '')
                if job:
                    if job.next_run_time:
                        next_run_time = job.next_run_time.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        next_run_time = None
                    if job.kwargs["ws_uid"] == ws_uid and job.kwargs["envir_uid"] == envirUid:
                        data={"nb_uid":job.id, "nb_name":job.name, "cron":str(job.trigger), 'pending':job.pending, "paused":job.next_run_time == None, "next_run_time":next_run_time,
                              "custom_cron":job.kwargs["custom_cron"],"last_time": job.kwargs["last_time"],"last_status":job.kwargs["last_status"],"last_msg":job.kwargs["last_msg"]
                              }
                        if len(job.args) > 2:
                            data['success_email'] = job.args[1]
                            data['fail_email'] = job.args[2]
                        res = {"code": 200, "msg": "查询调度信息成功", "data": data }
                else:
                    res = {"code": 200, "msg": "查询调度信息成功", "data":[]}
                self.finish(json.dumps(res, default=json_default))
        except Exception as e :
            log = traceback.format_exc()
            print(log, file=sys.stderr)
            res = {"code": 400, "msg": "查询调度信息失败", "data": log}
            self.finish(json.dumps(res, default=json_default))

    @gen.coroutine
    @interceptor
    def post(self, ws_uid, nb_uid) -> {"GRADE": ["BASIC", "PRO", "ENT"], "ROLE": ["ADMIN", "EDITOR"]}:
        try:
            body = self.request.body.strip().decode('utf-8')
            json_body = json.loads(body)
            try:
                schema = Schema({
                    Optional('nb_name'): And(str, lambda n: len(n) <= 64, error='nb名称格式不正确，最大为64！'),
                    Optional('fail_email'): And(list, lambda emails: len(emails)==0 or [
                        Regex(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$').validate(email) for email in emails],
                                                error="fail_email 格式不正确!"),
                    Optional('success_email'): And(list, lambda emails: len(emails)==0 or [
                        Regex(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$').validate(email) for email in emails],
                                                   error="success_email 格式不正确!"),
                    Optional('nb_uid'): And(str, lambda n: len(n) <= 36, error='目录格式不正确，最大为36！'),
                    Optional('ws_uid'): And(str, lambda n: len(n) <= 36, error='目录格式不正确，最大为36！'),
                    Optional(str): object
                })
                validated = schema.validate(json_body)
                pass
            except Exception as e:
                err_txt = str(e)
                print(err_txt)
                self.write_err("格式校验失败！"+err_txt)
                return



            job=scheduler.get_job(json_body["nb_uid"])
            if job:
                job.remove()

            scheduler.add_job(id=json_body["nb_uid"],
                              name=json_body["nb_name"],
                              func=ExecuteSnb,
                              args=[json_body["nb_uid"],json_body['success_email'],json_body['fail_email']],
                              kwargs={"name":json_body["nb_name"],"ws_uid":json_body["ws_uid"],"envir_uid": envir_uid,"custom_cron":json_body["custom_cron"],"last_time":None,"last_status":None,"last_msg":None},
                              trigger=CronTrigger.from_crontab(json_body["cron"])
                              )
            self.recall("set",json_body["nb_uid"])
            res = {"code": 200, "msg": "设置调度信息成功", "data": json_body["nb_uid"]}
            self.finish(json.dumps(res, default=json_default))
        except Exception as e :
            log = traceback.format_exc()
            res = {"code": 400, "msg": "设置调度信息失败", "data": log}
            self.finish(json.dumps(res, default=json_default))

    @gen.coroutine
    @interceptor
    def put(self, ws_uid, nb_uid) -> {"GRADE": ["BASIC", "PRO", "ENT"], "ROLE": ["ADMIN", "EDITOR"]}:
        try:
            body = self.request.body.strip().decode('utf-8')
            json_body = json.loads(body)
            for nb_uid in json_body["nb_uid"]:
                job = scheduler.get_job(nb_uid)
                if job:
                    if json_body["action"]=='pause':
                        job.pause()
                    if json_body["action"] == 'resume':
                        job.resume()
            res = {"code": 200, "msg": "暂停/恢复 调度信息成功", "data": []}
            self.finish(json.dumps(res, default=json_default))
        except Exception as e:
            log = traceback.format_exc()
            res = {"code": 400, "msg": "暂停/恢复 调度信息失败", "data": log}
            self.finish(json.dumps(res, default=json_default))

    @gen.coroutine
    @interceptor
    def delete(self, ws_uid, nb_uid) -> {"GRADE": ["BASIC", "PRO", "ENT"], "ROLE": ["ADMIN", "EDITOR"]}:
        try:
            body = self.request.body.strip().decode('utf-8')
            json_body = json.loads(body)
            for nb_uid in json_body["nb_uid"]:
                job = scheduler.get_job(nb_uid)
                if job:
                    job.remove()
                    res = {"code": 200, "msg": "删除调度信息成功", "data": []}
                else:
                    res = {"code": 400, "msg": "不存在", "data": []}
                self.recall("cancel", nb_uid)
            self.finish(json.dumps(res, default=json_default))
        except Exception as e :
            log = traceback.format_exc()
            res = {"code": 400, "msg": "删除调度信息失败", "data": log}
            self.finish(json.dumps(res, default=json_default))

_nb_uid_regex = r"(?P<nb_uid>.*)"
_ws_uid = r"(?P<ws_uid>[^/]+)"
default_handlers = [
    (fr"/api/snb/node/nodeSched/{_ws_uid}/{_nb_uid_regex}", setSchedulerHandler)
]
