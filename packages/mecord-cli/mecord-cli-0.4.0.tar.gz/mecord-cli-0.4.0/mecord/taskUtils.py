import os
import requests
import datetime
import json
import socket
from requests_toolbelt import MultipartEncoder
from urllib import parse
import matplotlib.pyplot as plt
import base64
import hashlib
from mecord import utils

task_config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)) , f"task_config.txt")
def taskCountryWithUUID(uuid):
    if os.path.exists(task_config_file):
        with open(task_config_file, 'r') as f:
            data = json.load(f)
        if uuid in data:
            return data[uuid]["country"]
    return None

def getCurrentTask():
    if os.path.exists(task_config_file):
        with open(task_config_file, 'r') as f:
            data = json.load(f)
        infos = ""
        for it in data:
            c = data[it]["country"]
            infos += f",{c}:{it}"
        return infos[1:]
    return ""

# WECHAT_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a771d063-45f9-4926-8543-538595833b74" #大群
WECHAT_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=46692305-49b8-4428-b47a-b34342fafd7d" #mecord-cli小群
# WECHAT_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a24496ad-5af6-4c95-a7e4-39cc8e9bb243" #轰炸机
def uploadFile2Wechat(filepath):
    params = parse.parse_qs( parse.urlparse( WECHAT_URL ).query )
    webHookKey=params['key'][0]
    upload_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={webHookKey}&type=file'
    headers = {"Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip, deflate",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36"}
    filename = os.path.basename(filepath)
    try:
        multipart = MultipartEncoder(
            fields={'filename': filename, 'filelength': '', 'name': 'media', 'media': (filename, open(filepath, 'rb'), 'application/octet-stream')},
            boundary='-------------------------acebdf13572468')
        headers['Content-Type'] = multipart.content_type
        resp = requests.post(upload_url, headers=headers, data=multipart, timeout=300)
        json_res = resp.json()
        if json_res.get('media_id'):
            return json_res.get('media_id')
    except Exception as e:
        return ""
def notifyWechatRobot(param):
    try:
        s = requests.session()
        s.headers.update({'Connection':'close'})
        headers = dict()
        headers['Content-Type'] = "application/json"
        res = s.post(WECHAT_URL, json.dumps(param), headers=headers, verify=False, timeout=30)
        s.close()
    except Exception as e:
        print(f"===== qyapi.weixin.qq.com fail ", True)

logs = {}
def taskPrint(taskUUID, msg):
    global logs
    if len(taskUUID) == 0 and msg == None:
        return
    if taskUUID and msg == None:
        del logs[taskUUID]
        return
    if taskUUID and msg:
        if taskUUID not in logs:
            logs[taskUUID] = []
        logs[taskUUID].append(msg)
    if taskUUID == None and msg:
        for uuid in logs:
            logs[uuid].append(msg)
    print(msg)
def getTaskLog(taskUUID):
    if taskUUID in logs:
        return logs[taskUUID]
    return []

def notifyTaskFail(taskUUID, reason):
    try:
        real_reason = ""
        if len(reason) > 410:
            real_reason = f"{reason[0:199]}\n...\n{reason[len(reason)-200:]}"
        else:
            real_reason = reason
        notifyWechatRobot({
            "msgtype": "markdown",
            "markdown": {
                "content": f"机器<<font color=\"warning\">{socket.gethostname()}</font>> 执行任务<{taskUUID}>失败\n<{real_reason}>"
            }
        })
        log_path = f"{os.path.dirname(os.path.abspath(__file__))}/log_{taskUUID}.log"
        with open(log_path, 'w') as f:
            f.write("\n".join(getTaskLog(taskUUID)))
        notifyWechatRobot({
            "msgtype": "file",
            "file": {
                "media_id": uploadFile2Wechat(log_path)
            }
        })
        if os.path.exists(log_path):
            os.remove(log_path)
    except:
        print("")

def notifyScriptError(taskUUID, cmd):
    try:
        notifyWechatRobot({
            "msgtype": "markdown",
            "markdown": {
                "content": f"机器<<font color=\"warning\">{socket.gethostname()}</font>> 执行任务<{taskUUID}>异常\n脚本位置:<{cmd}>"
            }
        })
        log_path = f"{os.path.dirname(os.path.abspath(__file__))}/log_{taskUUID}.log"
        with open(log_path, 'w') as f:
            f.write("\n".join(getTaskLog(taskUUID)))
        notifyWechatRobot({
            "msgtype": "file",
            "file": {
                "media_id": uploadFile2Wechat(log_path)
            }
        })
        if os.path.exists(log_path):
            os.remove(log_path)
    except:
        print("")

def idlingNotify(cnt):
    device_id = utils.generate_unique_id()
    machine_name = socket.gethostname()
    hour = int(float(cnt)/(60.0*60.0))
    notifyWechatRobot({
        "msgtype": "text",
        "text": {
            "content": f"机器<{machine_name}[{device_id}]> 空转{hour}小时"
        }
    })

def onlineNotify():
    device_id = utils.generate_unique_id()
    machine_name = socket.gethostname()
    notifyWechatRobot({
        "msgtype": "text",
        "text": {
            "content": f"机器<{machine_name}[{device_id}]> 上线"
        }
    })

def offlineNotify():
    device_id = utils.generate_unique_id()
    machine_name = socket.gethostname()
    notifyWechatRobot({
        "msgtype": "text",
        "text": {
            "content": f"机器<{machine_name}[{device_id}]> 下线"
        }
    })
#===================================================== counter ===============================================#
task_counter_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "task_counter.txt")
def notifyCounterIfNeed():
    if os.path.exists(task_counter_file) == False:
        return
    with open(task_counter_file, 'r') as f:
        data = json.load(f)
    now_hour = datetime.datetime.now().hour
    if now_hour == 0 and len(data) > 2:
        yesterday = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
        s_cnt = 0
        f_cnt = 0
        all_day_usage = 0
        t_l = []
        s_l = []
        f_l = []
        for i in range(0,24):
            tips = ""
            if str(i) in data:
                s_cnt += data[str(i)]["success"]
                f_cnt += data[str(i)]["fail"]
                s_l.append(data[str(i)]["success"])
                f_l.append(data[str(i)]["fail"])
                if "usage" in data[str(i)]:
                    all_day_usage += data[str(i)]["usage"]
                    usage_percentage = int((float(data[str(i)]["usage"])/float(60*60))*100)
                    tips = f"({usage_percentage}%)"
            else:
                s_cnt += 0
                f_cnt += 0
                s_l.append(0)
                f_l.append(0)
            t_l.append(f"{i}{tips}")
        usage_percentage = int((float(all_day_usage)/float(24*60*60))*100)
        notifyWechatRobot({
            "msgtype": "markdown",
            "markdown": {
                "content": f"机器<<font color=\"warning\">{socket.gethostname()}</font>> {yesterday} 日报 \n\n\
                                >过去24小时执行任务<<font color=\"warning\">{s_cnt+f_cnt}</font>>个, 负载<<font color=\"warning\">{usage_percentage}%</font>> \n\
                                >成功<font color=\"warning\">{s_cnt}</font>个 \n\
                                >失败<font color=\"warning\">{f_cnt}</font>个"
            }
        })
        
        plt.figure(figsize=(8,3))
        plt.rcParams.update({
            'font.size': 7
        })
        plt.bar(t_l, s_l, color='g', label='success')
        plt.bar(t_l, f_l, bottom=s_l, color='r', label='fail')
        plt.title(f'[{socket.gethostname()}] [{yesterday}] success/fail={s_cnt}/{f_cnt}')
        plt.xlabel('time')
        plt.xticks(ticks=t_l,rotation=45)
        plt.ylabel('count')
        plt.subplots_adjust(bottom=0.25)
        plt.legend()
        fff = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plt.png")
        plt.savefig(fff)
        with open(fff, "rb") as f:
            encode_string = str(base64.b64encode(f.read()), encoding='utf-8')
        md5 = hashlib.md5()
        md5.update(base64.b64decode(encode_string))
        hash = md5.hexdigest()
        notifyWechatRobot({
            "msgtype": "image",
            "image": {
                "base64": encode_string,
                "md5": hash
            }
        })
        os.remove(fff)
        os.remove(task_counter_file)

def saveCounter(taskUUID, duration, isSuccess):
    try:
        notifyCounterIfNeed()
        if os.path.exists(task_counter_file) == False:
            with open(task_counter_file, 'w') as f:
                json.dump({}, f)
        with open(task_counter_file, 'r') as f:
            data = json.load(f)
        #update
        now_hour = str(datetime.datetime.now().hour)
        if now_hour in data:
            if isSuccess:
                data[now_hour]["success"] += 1
            else:
                data[now_hour]["fail"] += 1
            if "usage" not in data[now_hour]:
                data[now_hour]["usage"] = 0
            data[now_hour]["usage"] += duration
        else:
            data[now_hour] = {
                "success" : 1 if isSuccess else 0,
                "fail" : 0 if isSuccess else 1,
                "usage" : 0
            }
        #save
        with open(task_counter_file, 'w') as f:
            json.dump(data, f)
    except:
        print("")