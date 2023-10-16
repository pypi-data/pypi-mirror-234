import datetime

import nbformat
import requests
from nbconvert.preprocessors import ExecutePreprocessor
import asyncio
import sys
import json
import time
from snb_node.config.Config import SNB_SERVER_URL, config, pem, workspace_uid, envir_uid
from snb_plugin.utils.snb_uuid import uuid1
import os
from snb_node.exec_snb.SnbScheduler import scheduler
import snb_plugin.utils.snb_RSA as snb_rsa
import traceback

if sys.platform == "win32" and sys.version_info > (3, 8, 0, "alpha", 3):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import re

# text= "\033[1;31;40m您输入的帐号或密码错误！\033[0m  fdfsdgf  \033[1;31;40m您输入的帐号或密码错误！\033[0m"


def ansi_to_text(text):
    ansi_codes_prog = re.compile("\033\\[([\\d;:]*)([a-zA-z])")
    last_end = 0
    restr = '<font color="red"> '
    for match in ansi_codes_prog.finditer(text):
        restr = restr + text[last_end : match.start()]
        last_end = match.end()
    restr = restr + text[last_end:] + " </font>"
    restr = restr.replace("\n", "<br />")
    return restr


def sendMail(email, name, status, status_msg, exec_time, snb_uid, ws_uid, report_uid):
    uri = "/api/snb_native/taskSendEmail?t=" + str(time.time())
    url = "".join([SNB_SERVER_URL, uri])
    sign_str = snb_rsa.sign(uri, pem)
    header = {"Cookie": "cookie", "sign": sign_str, "workspaceUid": workspace_uid}
    bd = {
        "email": email,
        "name": name,
        "status": status,
        "status_msg": status_msg,
        "exec_time": exec_time,
        "nb_uid": snb_uid,
        "ws_uid": ws_uid,
        "report_uid": report_uid,
    }
    conn_info = requests.post(url, data=json.dumps(bd), headers=header)
    if conn_info.status_code == 200:
        print("发送成功:", conn_info.text)
    else:
        print("发送失败:", conn_info.text)


# sendMail("wrss01@126.com","NB测试","success","","2022-10-24 10:01:01")


def ExecuteSnb(snb_uid, success_email=None, fail_email=None, **kwargs):
    try:
        print(success_email, fail_email)
        start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if sys.platform == "win32":
            home = "c://smartnotebook/test/.report"
        else:
            home = "/home/.report"
        # 调度执行之前先判断当前调度是否正常

        env_url = "".join([SNB_SERVER_URL, "/api/snb_native/env/" + envir_uid])
        env_sign_str = snb_rsa.sign("/api/snb_native/env/" + envir_uid, pem)
        env_header = {"Cookie": "cookie", "sign": env_sign_str, "workspaceUid": workspace_uid}
        env_info = requests.get(env_url, headers=env_header)
        env_resp = env_info.json()
        if env_resp["code"] == 200:
            cntr_status = env_resp["data"]["cntr_status"]
            status = "1"
            if cntr_status != status:
                return

        url = "".join([SNB_SERVER_URL, "/api/snb_native/nbver_last/" + snb_uid])
        sign_str = snb_rsa.sign("/api/snb_native/nbver_last/" + snb_uid, pem)
        header = {"Cookie": "cookie", "sign": sign_str, "workspaceUid": workspace_uid}
        conn_info = requests.get(url, headers=header)
        print(url)
        resp = conn_info.json()
        print("*" * 10, " 执行SNB  ", "*" * 10, time.strftime("%Y-%m-%d %H:%M:%S %Z"))
        if resp["code"] == 200:
            snb = json.loads(resp["data"])
            snb_new = []
            report_uid = uuid1()
            path_name = home + "/" + snb_uid
            if not os.path.exists(path_name):
                os.makedirs(path_name)
            ep = ExecutePreprocessor(timeout=3600, kernel_name="python3")
            """
              --allow-errors
              Continue notebook execution even if one of the cells throws an error and include the error message in the cell output (the default behaviour is to abort conversion). 
              This flag is only relevant if '--execute' was specified, too. Equivalent to: [--ExecutePreprocessor.allow_errors=True]
            """
            ep.allow_errors = True
            cell_error = False
            cell_error_msg = None
            for snb_sheet in snb:
                nb = nbformat.reads(json.dumps(snb_sheet), as_version=4)
                ep.preprocess(nb, resources={})
                snb_new.append(nb)
                for num, cell in enumerate(nb.cells):
                    if "outputs" in cell:
                        for output in cell["outputs"]:
                            if output.output_type == "error":
                                cell_error = True
                                if cell_error_msg:
                                    cell_error_msg = cell_error_msg + "\n".join(output.traceback)
                                else:
                                    cell_error_msg = "\n".join(output.traceback)
                                break
                    if cell_error:
                        break
                with open(path_name + "/%s_%s.ipynb" % (report_uid, snb_sheet["name"]), "w", encoding="utf-8") as f:
                    nbformat.write(nb, f)
            print("*" * 10, " 写入report ", "*" * 10, time.strftime("%Y-%m-%d %H:%M:%S %Z"))

            with open(path_name + "/%s.snb" % (report_uid), "w", encoding="utf-8") as f:
                f.write(json.dumps(snb_new))

            url = SNB_SERVER_URL + "/api/snb/snb_native/report/" + snb_uid
            body = {
                "name": kwargs["name"],
                "start_time": start_time,
                "end_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "data": snb_new,
                "envir_uid": envir_uid,
            }
            if cell_error:
                body["status"] = 0
            else:
                body["status"] = 1

            sign_str = snb_rsa.sign("/api/snb/snb_native/report/" + snb_uid, pem)
            headers = {
                "authorization": "",
                "content-type": "application/json;charset=UTF-8",
                "sign": sign_str,
                "workspaceUid": workspace_uid,
            }

            response = requests.post(url, data=json.dumps(body), headers=headers)
            print(response.text)
            responseJson = response.json()
            if responseJson["code"] == 200:
                report_uid = responseJson["data"]
            if cell_error:
                if fail_email:
                    sendMail(
                        fail_email,
                        body["name"],
                        "fail",
                        ansi_to_text(cell_error_msg),
                        body["end_time"],
                        snb_uid,
                        kwargs["ws_uid"],
                        report_uid,
                    )
            else:
                if success_email:
                    sendMail(
                        success_email,
                        body["name"],
                        "success",
                        "success",
                        body["end_time"],
                        snb_uid,
                        kwargs["ws_uid"],
                        report_uid,
                    )

            job = scheduler.get_job(snb_uid)
            kwargs = job.kwargs
            kwargs["last_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if cell_error:
                kwargs["last_status"] = "fail"
                kwargs["last_msg"] = cell_error_msg[0:1024]
            else:
                kwargs["last_status"] = "success"
                kwargs["last_msg"] = "success"
            scheduler.modify_job(snb_uid, kwargs=kwargs)

    except Exception as e:
        log = traceback.format_exc()
        print(log, file=sys.stderr)
        if fail_email:
            sendMail(
                fail_email,
                kwargs["name"],
                "fail",
                log,
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                snb_uid,
                kwargs["ws_uid"],
                report_uid,
            )

        job = scheduler.get_job(snb_uid)
        kwargs = job.kwargs
        kwargs["last_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        kwargs["last_status"] = "fail"
        kwargs["last_msg"] = log[0:1024]
        scheduler.modify_job(snb_uid, kwargs=kwargs)


# ExecuteSnb('0242ac110004-11ed3a50-3f7e3ed0-ad58','success_email111')
# ExecuteSnb('0242ac110004-11ed37fb-e514f7e6-9541',success_email="wrss01@126.com",fail_email="wrss01@126.com",**{"name":"NB测试"})
