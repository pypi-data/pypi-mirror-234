import json
import hashlib
import time
import socket
import requests
import urllib3
import os
import random
import datetime
import base64
import ping3
import uuid

import mecord.pb.uauth_common_pb2 as uauth_common_pb2
import mecord.pb.uauth_ext_pb2 as uauth_ext_pb2
import mecord.pb.common_ext_pb2 as common_ext_pb2
import mecord.pb.aigc_ext_pb2 as aigc_ext_pb2
import mecord.pb.rpcinput_pb2 as rpcinput_pb2
from mecord import store 
from mecord import utils 
from mecord import taskUtils 
from mecord import constant 

OFFICIAL_PRODUCT_TOKEN = "NDl8NWU5OGI1ODk4N2ExNTZmZWE1MmI4YzM3MTNjNjI0MDd8ZjI2MzYwZTA2ZWVkODg0Y2ZlNjZlZTBlNzVhZDM1OWY="
NORMAL_TOKEN = "NzN8OGZmZmQ0N2UyNWY1NTY5ZWFhYWNjMzA5OGRiNDcxOTZ8YThmOWM3Nzg2NTM3YzVmMzMzNzY0MTI1NWM4MmZlNzU="
COUNTRY_DOMAIN =  {
    "us" : "https://api.mecordai.com/proxymsg",
    "sg" : "https://api-sg.mecordai.com/proxymsg"
}

def supportCountrys(isProduct):
    if isProduct:
        return ["US", "SG"]
    else:
        return ["test"]
    
def real_token():
    if store.is_product():
        return OFFICIAL_PRODUCT_TOKEN
    else:
        tk = store.token()
        if tk == OFFICIAL_PRODUCT_TOKEN:
            tk = NORMAL_TOKEN
        return tk

def _aigc_post_product(country, request, function):
    domain = COUNTRY_DOMAIN["us"]
    if country.lower() in COUNTRY_DOMAIN:
        domain = COUNTRY_DOMAIN[country.lower()]
    return _post(url=domain, 
                 objStr="mecord.aigc.AigcExtObj", 
                 request=request, 
                 function=function,
                 token=OFFICIAL_PRODUCT_TOKEN)
def _aigc_post(request, function):
    tk = store.token()
    if tk == OFFICIAL_PRODUCT_TOKEN:
        tk = NORMAL_TOKEN
    return _post(url="https://mecord-beta.2tianxin.com/proxymsg", 
                 objStr="mecord.aigc.AigcExtObj", 
                 request=request, 
                 function=function,
                 token=tk)

def _try_network():
    try:
        for url in ["https://www.baidu.com/"]:
            s = requests.session()
            s.keep_alive = False
            s.headers.update({'Connection':'close'})
            res = s.get(url=url, timeout=30)
            taskUtils.taskPrint(None, f"=== probe url={url} result_code={res.status_code}")
            s.close()
            
        for ip in ["www.baidu.com", "1.1.1.1", "8.8.8.8", "208.67.222.222"]:
            res = ping3.ping(ip, timeout=5)
            if res:
                taskUtils.taskPrint(None, f"=== ping {ip} success")
            else:
                taskUtils.taskPrint(None, f"=== probe {url} fail")
    finally:
        return

def _post(url, objStr, request, function, token):
    req = request.SerializeToString()
    opt = {
        "lang": "zh-Hans",
        "region": "CN",
        "appid": "80",
        "application": "mecord",
        "version": "1.0",
        "X-Token": token,
        "uid": "1",
    }
    input_req = rpcinput_pb2.RPCInput(obj=objStr, func=function, req=req, opt=opt)
    s = requests.session()
    try:
        requests.adapters.DEFAULT_RETRIES = 2
        s.keep_alive = False
        s.headers.update({'Connection':'close'})
        res = s.post(url=url, data=input_req.SerializeToString(), timeout=60)
        if res.status_code == 200:
            res_content = res.content
            res.close()
            pb_rsp = rpcinput_pb2.RPCOutput()
            pb_rsp.ParseFromString(res_content)
            if pb_rsp.ret == 0:
                return 0, "", pb_rsp.rsp
            else:
                taskUtils.taskPrint(None, f'''=============== request err_code={pb_rsp.ret} err_desc={pb_rsp.desc} {datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')} {"product" if store.is_product() else "test"} ===============
url={url}
func={function}
token={token}

req=
{request}
respose=
{res.content}
===============
''')
                return pb_rsp.ret, pb_rsp.desc, "" 
        else:
            raise Exception(f"status_code={res.status_code}")
    except Exception as e:
        taskUtils.taskPrint(None, f'''=============== mecord server error {datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')} {"product" if store.is_product() else "test"} ===============
url={url}
func={function}
token={token}

req=
{request}
exception={e}
===============
''')
        _try_network()
        return -99, str(e), ""
    finally:
        s.close()
    
#======================================== Task Function ==============================
def _extend():
    extInfo = store.readDeviceInfo()
    extInfo["app_version"] = constant.app_version
    extInfo["app_bulld_number"] = constant.app_bulld_number
    extInfo["app_name"] = constant.app_name
    extInfo["dts"] = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
    extInfo["trace_id"] = ''.join(str(uuid.uuid4()).split('-'))
    extInfo["salt"] = utils.get_salt()
    return json.dumps(extInfo)

def GetTask(country):
    req = aigc_ext_pb2.GetTaskReq()
    req.version = constant.app_version
    req.DeviceKey = utils.generate_unique_id()
    map = store.widgetMap()
    for it in map:
        if isinstance(map[it], (dict)):
            if map[it]["isBlock"] == False:
                req.widgets.append(it)
        else:
            req.widgets.append(it)
    req.token = real_token()
    req.limit = store.multitaskNum()
    req.extend = _extend()
    
    rsp = aigc_ext_pb2.GetTaskRes()
    if store.is_product():
        r1, r2, r3 = _aigc_post_product(country, req, "GetTask")
    else:
        r1, r2, r3 = _aigc_post(req, "GetTask")
    if r1 != 0:
        return []
    rsp.ParseFromString(r3)
    datas = []
    for it in rsp.list:
        datas.append({
            "taskUUID": it.taskUUID,
            "pending_count": rsp.count - rsp.limit,
            "config": it.config,
            "data": it.data,
        })
    #Previous tasks may have failed due to network problems, so collect and resend
    retryLastTaskNotify()
    return datas
    # if random.randint(0, 10) != 5:
    #     return []
    # return [{
    #     "taskUUID": ''.join(str(uuid.uuid4()).split('-')),
    #     "pending_count": 1,
    #     "config": "{\"widget_id\":\"Light-widget\",\"group_id\":\"\",\"cmd\":\"E:\\\\aigc\\\\lora\\\\script\\\\main.py\"}",
    #     "data": "{\"fn_name\":\"Light-widget\",\"param\":{\"batch_count\":1,\"batch_size\":1,\"cfg_scale\":7,\"creative_strength\":1,\"denoising_strength\":1,\"era\":\"deploy_cart_PL05\",\"fn_name\":\"Light-widget\",\"fuse\":true,\"height\":400,\"musicUrl\":\"\",\"negative_prompt\":\"\",\"package_url\":\"https://m-beta-yesdesktop.2tianxin.com/upload/beta/undefined/6074/256D/6074367D73E9256D.zip\",\"prompt\":\"\",\"restore_faces\":true,\"sampler_index\":\"DPM++ SDE Karras\",\"scratch\":1,\"seed\":-1,\"steps\":25,\"text_mark_url\":\"\",\"type\":\"image\",\"user_file_name\":\"e623252d-10d6-4b0c-806b-16f0495f045d.jpg\",\"user_url\":\"\",\"width\":400}}",
    # }]

TASK_NOTIFY_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"task_notify_data.json")
def saveTaskNotifyData(country, taskUUID, status, msg, dataStr):
    taskUtils.taskPrint(taskUUID, f"save {taskUUID} to next notify")
    try:
        if not os.path.exists(TASK_NOTIFY_DATA):
            with open(TASK_NOTIFY_DATA, 'w') as f:
                json.dump([], f)
        with open(TASK_NOTIFY_DATA, 'r') as f:
            data = json.load(f)
        data.append({
            "taskUUID":taskUUID,
            "status":status,
            "country":country,
            "msg":msg,
            "dataStr":dataStr
        })
        with open(TASK_NOTIFY_DATA, 'w') as f:
            json.dump(data, f)
    finally:
        return
def retryLastTaskNotify():
    try:
        if os.path.exists(TASK_NOTIFY_DATA):
            with open(TASK_NOTIFY_DATA, 'r') as f:
                data = json.load(f)
            newData = []
            for it in data:
                msg = it["msg"]
                counrty = "US"
                if "country" in it:
                    counrty = it["country"]
                if TaskNotify(counrty, it["taskUUID"], it["status"], f"{msg} *", it["dataStr"]) == False:
                    newData.append(it)
            with open(TASK_NOTIFY_DATA, 'w') as f:
                json.dump(newData, f)
    finally:
        return

def TaskNotify(country, taskUUID, status, msg, dataStr):
    req = aigc_ext_pb2.TaskNotifyReq()
    req.version = constant.app_version
    req.taskUUID = taskUUID
    if status:
        req.taskStatus = common_ext_pb2.TaskStatus.TS_Success
    else:
        req.taskStatus = common_ext_pb2.TaskStatus.TS_Failure
    req.failReason = msg
    req.data = dataStr
    req.extend = _extend()
    
    rsp = aigc_ext_pb2.TaskNotifyRes()
    if store.is_product():
        r1, r2, r3 = _aigc_post_product(country, req, "TaskNotify")
    else:
        r1, r2, r3 = _aigc_post(req, "TaskNotify")
    if r1 != 0:
        #tasks may have failed due to network problems, so collect and resend
        saveTaskNotifyData(country, taskUUID, status, msg, dataStr)
        return False
    rsp.ParseFromString(r3)
    taskUtils.taskPrint(taskUUID, f"receive server ok={rsp.ok} notify_id = {rsp.notify_id}")
    if len(rsp.notify_id) == 0:
        #tasks may have failed due to network problems, so collect and resend
        saveTaskNotifyData(country, taskUUID, status, msg, dataStr)
    return rsp.ok == True

def GetOssUrl(country, ext):
    req = aigc_ext_pb2.UploadFileUrlReq()
    req.token = real_token()
    req.version = constant.app_version
    req.fileExt = ext

    rsp = aigc_ext_pb2.UploadFileUrlRes()
    if store.is_product():
        r1, r2, r3 = _aigc_post_product(country, req, "UploadFileUrl")
    else:
        r1, r2, r3 = _aigc_post(req, "UploadFileUrl")
    if r1 != 0:
        return "", r2
    rsp.ParseFromString(r3)
    return rsp.url, rsp.contentType

def UploadMarketModel(country, name, cover, model_url, type, taskuuid):
    req = aigc_ext_pb2.MarketModelCreateWithTaskReq()
    req.name = name
    req.cover = cover
    req.url = model_url
    req.type = type
    req.TaskUUID = taskuuid

    rsp = aigc_ext_pb2.MarketModelCreateWithTaskRes()
    if store.is_product():
        r1, r2, r3 = _aigc_post_product(country, req, "MarketModelCreateWithTask")
    else:
        r1, r2, r3 = _aigc_post(req, "MarketModelCreateWithTask")
    if r1 != 0:
        return 0
    rsp.ParseFromString(r3)
    return True

#======================================== Other Function ==============================
def DeviceUnbind():
    req = aigc_ext_pb2.AigcDeviceUnBindReq()
    req.deviceToken = store.token()

    rsp = aigc_ext_pb2.AigcDeviceUnBindRes()
    r1, r2, r3 = _aigc_post(req, "DeviceUnBind")
    if r1 != 0:
        return False
    rsp.ParseFromString(r3)
    return False

def GetAigcDeviceInfo():
    req = aigc_ext_pb2.AigcDeviceInfoReq()
    req.version = constant.app_version
    req.deviceKey = utils.generate_unique_id()
    extInfo = store.readDeviceInfo()
    extInfo["app_version"] = constant.app_version
    extInfo["app_bulld_number"] = constant.app_bulld_number
    extInfo["app_name"] = constant.app_name
    req.extend = json.dumps(extInfo)

    rsp = aigc_ext_pb2.AigcDeviceInfoRes()
    r1, r2, r3 = _aigc_post(req, "DeviceInfo")
    if r1 != 0:
        if r1 != 11000:
            print(f'get DeviceInfo failed: {r1} {r2}')
        return False
    rsp.ParseFromString(r3)
    
    if len(rsp.groupUUID) > 0:
        sp = store.Store()
        data = sp.read()
        data["groupUUID"] = rsp.groupUUID
        data["token"] = rsp.token
        if rsp.isCreateWidget == True:
            data["isCreateWidget"] = rsp.isCreateWidget
        sp.write(data)
        return True
    return False

def CreateWidgetUUID():
    req = aigc_ext_pb2.ApplyWidgetReq()
    rsp = aigc_ext_pb2.ApplyWidgetRes()
    r1, r2, r3 = _aigc_post(req, "ApplyWidget")
    if r1 != 0:
        return ""
    rsp.ParseFromString(r3)
    return rsp.widgetUUID

def DeleteWidget(widgetid):
    req = aigc_ext_pb2.DeleteAigcWidgetReq()
    req.widgetUUID = widgetid
    req.deviceToken = store.token()
    rsp = aigc_ext_pb2.DeleteAigcWidgetRes()
    r1, r2, r3 = _aigc_post(req, "DeleteWidget")
    if r1 != 0:
        return False
    rsp.ParseFromString(r3)
    return True

def GetTaskCount(widgetid):
    req = aigc_ext_pb2.TaskCountReq()
    req.deviceToken = store.token()
    rsp = aigc_ext_pb2.TaskCountRes()
    r1, r2, r3 = _aigc_post(req, "TaskCount")
    if r1 != 0:
        return []
    rsp.ParseFromString(r3)
    datas = []
    for it in rsp.items:
        datas.append({
            "widgetUUID": it.widgetUUID,
            "taskCount": it.taskCount
        })
    return datas

def RemoteWidgetList(widgetid):
    req = aigc_ext_pb2.AigcWidgetListReq()
    req.deviceToken = store.token()
    rsp = aigc_ext_pb2.AigcWidgetListRes()
    r1, r2, r3 = _aigc_post(req, "WidgetList")
    if r1 != 0:
        return []
    rsp.ParseFromString(r3)
    datas = []
    for it in rsp.items:
        datas.append({
            "uuid": it.uuid,
            "name": it.name,
            "updated_at": it.updated_at,
        })
    return datas

def ExpansionWithToken(token):
    req = aigc_ext_pb2.AigcDeviceExpansionReq()
    req.DeviceToken = token
    req.DeviceKey = utils.generate_unique_id()

    rsp = aigc_ext_pb2.AigcDeviceExpansionRes()
    r1, r2, r3 = _aigc_post(req, "DeviceExpansion")
    if r1 == 11000:
        return False, r1
    elif r1 != 0:
        return ""
    rsp.ParseFromString(r3)

    if len(rsp.groupUUID) > 0:
        sp = store.Store()
        data = sp.read()
        data["groupUUID"] = rsp.groupUUID
        data["token"] = rsp.deviceToken
        sp.write(data)
        return True, 0
    return False, -1
   
def GetWidgetOssUrl(widgetid):
    req = aigc_ext_pb2.UploadWidgetUrlReq()
    req.version = constant.app_version
    req.widgetUUID = widgetid

    rsp = aigc_ext_pb2.UploadWidgetUrlRes()
    r1, r2, r3 = _aigc_post(req, "UploadWidgetUrl")
    if r1 != 0:
        return "", ""
    rsp.ParseFromString(r3)
    return rsp.url, rsp.contentType

def WidgetUploadEnd(url):
    req = aigc_ext_pb2.UploadWidgetReq()
    req.version = constant.app_version
    req.fileUrl = url
    
    rsp = aigc_ext_pb2.UploadWidgetRes()
    r1, r2, r3 = _aigc_post(req, "UploadWidget")
    if r1 != 0:
        return 0
    rsp.ParseFromString(r3)
    return rsp.checkId
    
def UploadWidgetCheck(checkId):
    req = aigc_ext_pb2.UploadWidgetCheckReq()
    req.version = constant.app_version
    req.checkId = checkId

    rsp = aigc_ext_pb2.UploadWidgetCheckRes()
    r1, r2, r3 = _aigc_post(req, "UploadWidgetCheck")
    if r1 != 0:
        return 0
    rsp.ParseFromString(r3)
    if rsp.status == aigc_ext_pb2.UploadWidgetStatus.UWS_SUCCESS:
        return 1
    elif rsp.status == aigc_ext_pb2.UploadWidgetStatus.UWS_FAILURE:
        print(f"widget pulish fail msg => {rsp.failReason}")
        return 0
    else:
        return -1