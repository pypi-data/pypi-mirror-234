import os
import sys
import time
import signal
import subprocess
import json
import platform
import math
from pathlib import Path
from urllib.parse import *
import socket
import calendar
from threading import Thread, current_thread, Lock

from mecord import store
from mecord import xy_pb
from mecord import xy_user 
from mecord import utils
from mecord import taskUtils
from mecord import progress_monitor

thisFileDir = os.path.dirname(os.path.abspath(__file__)) 
pid_file = os.path.join(thisFileDir, "MecordService.pid")
stop_file = os.path.join(thisFileDir, "stop.now")
stop_thread_file = os.path.join(thisFileDir, "stop.thread")
class MecordService:
    def __init__(self):
        self.THEADING_LIST = []

    def start(self, isProduct=False, threadNum=1):
        if os.path.exists(pid_file):
            #check pre process is finish successed!
            with open(pid_file, 'r') as f:
                pre_pid = str(f.read())
            if len(pre_pid) > 0:
                if utils.process_is_zombie_but_cannot_kill(int(pre_pid)):
                    print(f'start service fail! pre process {pre_pid} is uninterruptible sleep')
                    taskUtils.notifyWechatRobot({
                        "msgtype": "text",
                        "text": {
                            "content": f"机器<{socket.gethostname()}>无法启动服务 进程<{pre_pid}>为 uninterruptible sleep"
                        }
                    })
                    return False
        with open(pid_file, 'w') as f:
            f.write(str(os.getpid()))
        signal.signal(signal.SIGTERM, self.stop)
        store.save_product(isProduct)
        store.writeDeviceInfo(utils.deviceInfo())
        _clearTask()
        for i in range(0, threadNum):
            self.THEADING_LIST.append(MecordThread(str(i+1)))
        self.THEADING_LIST.append(MecordStateThread())
        while (os.path.exists(stop_file) == False):
            time.sleep(10)
        print("prepare stop")
        with open(stop_thread_file, 'w') as f:
            f.write("")
        for t in self.THEADING_LIST:
            t.markStop()
        for t in self.THEADING_LIST:
            t.join()
        if pid_file and os.path.exists(pid_file):
            os.remove(pid_file)
        if os.path.exists(stop_thread_file):
            os.remove(stop_thread_file)
        if os.path.exists(stop_file):
            os.remove(stop_file)
        store.save_product(False)
        taskUtils.offlineNotify()
        print("MecordService has ended!")

    def is_running(self):
        if pid_file and os.path.exists(pid_file):
            with open(pid_file, 'r', encoding='UTF-8') as f:
                pid = int(f.read())
                try:
                    if utils.process_is_alive(pid):
                        return True
                    else:
                        return False
                except OSError:
                    return False
        else:
            return False
        
    def stop(self, signum=None, frame=None):
        with open(stop_file, 'w') as f:
            f.write("")
        print("MecordService waiting stop...")
        while os.path.exists(stop_file):
            time.sleep(1)
        print("MecordService has ended!")
    
lock = Lock()
task_config_file = os.path.join(thisFileDir, f"task_config.txt")
def _readTaskConfig():
    if os.path.exists(task_config_file) == False:
        with open(task_config_file, 'w') as f:
            json.dump({
                "last_task_pts": 0
            }, f)
    with open(task_config_file, 'r') as f:
        data = json.load(f)
    return data
def _saveTaskConfig(data):
    with open(task_config_file, 'w') as f:
        json.dump(data, f)
def _appendTask(taskUUID, country):
    lock.acquire()
    task_config = _readTaskConfig()
    task_config[taskUUID] = {
        "country": country,
        "pts": calendar.timegm(time.gmtime())
    }
    task_config["last_task_pts"] = task_config[taskUUID]["pts"]
    _saveTaskConfig(task_config)
    lock.release() 
def _clearTask():
    lock.acquire()
    task_config = _readTaskConfig()
    task_config = {
        "last_task_pts": 0
    }
    _saveTaskConfig(task_config)
    lock.release() 
def _removeTask(taskUUID):
    lock.acquire()
    task_config = _readTaskConfig()
    if taskUUID in task_config:
        del task_config[taskUUID]
    _saveTaskConfig(task_config)
    lock.release() 
def _taskCreateTime(taskUUID):
    pts = 0
    lock.acquire()
    task_config = _readTaskConfig()
    if taskUUID in task_config:
        pts = task_config[taskUUID]["pts"]
    lock.release()
    return pts 
def _getTaskConfig():
    lock.acquire()
    task_config = _readTaskConfig()
    lock.release() 
    return task_config

class MecordStateThread(Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.tik_time = 30.0
        self.start()
    def run(self):
        taskUtils.onlineNotify()
        while (os.path.exists(stop_thread_file) == False):
            time.sleep(self.tik_time)
            try:
                task_config = _getTaskConfig()
                if task_config["last_task_pts"] > 0:
                    cnt = (calendar.timegm(time.gmtime()) - task_config["last_task_pts"]) #second
                    if cnt >= (60*60) and cnt/(60*60)%1 <= self.tik_time/3600:
                        taskUtils.idlingNotify(cnt)
                        #clear trush
                        for root,dirs,files in os.walk(thisFileDir):
                            for file in files:
                                if file.find(".") <= 0:
                                    continue
                                ext = file[file.rindex("."):]
                                if ext in [ ".in", ".out" ]:
                                    os.remove(os.path.join(thisFileDir, file))
                            if root != files:
                                break
            except:
                time.sleep(60)
        print(f"   StateChecker stop")
    def markStop(self):
        print(f"   StateChecker waiting stop")

class MecordThread(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = f"MecordThread-{name}"
        self.start()
        
    def executeLocalPython(self, taskUUID, cmd, param):
        inputArgs = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{taskUUID}.in")
        if os.path.exists(inputArgs):
            os.remove(inputArgs)
        with open(inputArgs, 'w') as f:
            json.dump(param, f)
        outArgs = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{taskUUID}.out")
        if os.path.exists(outArgs):
            os.remove(outArgs)
            
        outData = {
            "result" : [ 
            ],
            "status" : -1,
            "message" : "script error"
        }
        executeSuccess = False
        command = f'{sys.executable} "{cmd}" --run "{inputArgs}" --out "{outArgs}"'
        taskUtils.taskPrint(taskUUID, f"{current_thread().name}=== exec => {command}")
        try:
            # import random
            # if random.randint(0, 20) != 1:
            #     if random.randint(0, 5) == 1:
            #         outData = {'result': [{'type': 'image', 'content': [], 'extension': {'info': '', 'cover_url': ''}}], 'status': 1, 'message': 'excuting task fail'}
            #     else:
            #         outData = {'result': [{'type': 'image', 'content': [], 'extension': {'info': '', 'cover_url': ''}}], 'status': 0, 'message': ''}
            #     executeSuccess = True
            # else:
            #     executeSuccess = False
            # time.sleep(random.randint(5, 20))

            # path = os.path.dirname(cmd)
            # config_file = os.path.join(path, 'config.json')
            # with open(config_file, "r") as f:
            #     data = json.load(f)
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            # if data is not None and 'type' in data and data['type'].lower() == 'sd':
            #     widget_infos = [{"widget":"SD", "port":6006, "name":"", "path":path}]
            # else:
            #     widget_infos = [{"widget":"other", "port":"", "name":"", "pid": process.pid, "path":path}]
            # taskUtils.taskPrint(taskUUID, f"monitor process: {path}")
            # progress_monitor.start(widget_infos)
            output, error = process.communicate(timeout=60*60)
            # progress_monitor.stop()
            if process.returncode == 0:
                taskUtils.taskPrint(taskUUID, output.decode(encoding="utf8", errors="ignore"))
                if os.path.exists(outArgs):
                    with open(outArgs, 'r', encoding='UTF-8') as f:
                        outData = json.load(f)
                    executeSuccess = True
                    taskUtils.taskPrint(taskUUID, f"exec success result => {outData}")
                else:
                    taskUtils.taskPrint(taskUUID, f"task {taskUUID} result is empty!, please check {cmd}")
            else:
                taskUtils.taskPrint(taskUUID, "====================== script error ======================")
                o1 = output.decode(encoding="utf8", errors="ignore")
                o2 = error.decode(encoding="utf8", errors="ignore")
                taskUtils.taskPrint(taskUUID, f"{o1}\n{o2}")
                taskUtils.taskPrint(taskUUID, "======================     end      ======================")
                taskUtils.notifyScriptError(taskUUID, cmd)
        except Exception as e:
            taskUtils.taskPrint(taskUUID, "====================== process error ======================")
            taskUtils.taskPrint(taskUUID, e)
            taskUtils.taskPrint(taskUUID, "======================      end      ======================")
            taskUtils.notifyScriptError(taskUUID, cmd)
        finally:
            if os.path.exists(inputArgs):
                os.remove(inputArgs)
            if os.path.exists(outArgs):
                os.remove(outArgs)
        return executeSuccess, outData,

    def needChangeValue(self, taskUUID, data, type, key):
        if "type" not in data:
            taskUtils.taskPrint(taskUUID, "result is not avalid")
            return False
        if data["type"] != type:
            return False
        if "extension" not in data or key not in data["extension"] or len(data["extension"][key]) == 0:
            return True
        return False
             
    def checkResult(self, taskUUID, data):
        for it in data["result"]:
            if self.needChangeValue(taskUUID, it, "text", "cover_url"):
                it["extension"]["cover_url"] = ""
            if self.needChangeValue(taskUUID, it, "audio", "cover_url"):
                it["extension"]["cover_url"] = ""
            if self.needChangeValue(taskUUID, it, "image", "cover_url"):
                it["extension"]["cover_url"] = ""
            if self.needChangeValue(taskUUID, it, "video", "cover_url"):
                it["extension"]["cover_url"] = ""
               
            if "extension" in it and "cover_url" in it["extension"] and len(it["extension"]["cover_url"]) > 0:
                w, h = utils.getOssImageSize(it["extension"]["cover_url"])
                if w > 0 and h > 0:
                    if "?" in str(it["extension"]["cover_url"]):
                        it["extension"]["cover_url"] += f"&width={w}&height={h}"
                        it["extension"]["width"] = w
                        it["extension"]["height"] = h
                    else:
                        it["extension"]["cover_url"] = urljoin(it["extension"]["cover_url"], f"?width={w}&height={h}")

    def cmdWithWidget(self, widget_id):
        map = store.widgetMap()
        if widget_id in map:
            path = ""
            is_block = False
            if isinstance(map[widget_id], (dict)):
                is_block = map[widget_id]["isBlock"]
                path = map[widget_id]["path"]
            else:
                is_block = False
                path = map[widget_id]
            if len(path) > 0 and is_block == False:
                return path
        return None

    def run(self):
        while (os.path.exists(stop_thread_file) == False):
            for service_country in xy_pb.supportCountrys(store.is_product()):
                taskUUID = ""
                try:
                    datas = xy_pb.GetTask(service_country)
                    for it in datas:
                        taskUUID = it["taskUUID"]
                        _appendTask(taskUUID, service_country)
                        taskUtils.taskPrint(taskUUID, f"{current_thread().name}=== receive {service_country} task : {taskUUID}")
                        pending_count = it["pending_count"]
                        config = json.loads(it["config"])
                        params = json.loads(it["data"])
                        widget_id = config["widget_id"]
                        group_id = config["group_id"]
                        #cmd
                        local_cmd = self.cmdWithWidget(widget_id)
                        cmd = ""
                        if local_cmd:
                            cmd = local_cmd
                        else:
                            cmd = str(Path(config["cmd"]))
                        #params
                        params["task_id"] = taskUUID
                        params["pending_count"] = pending_count
                        #run
                        taskUtils.taskPrint(taskUUID, f"{current_thread().name}=== start execute {service_country} task : {taskUUID}")
                        executeSuccess, result_obj = self.executeLocalPython(taskUUID, cmd, params)
                        #result
                        is_ok = executeSuccess and result_obj["status"] == 0
                        msg = "Unknow Error"
                        if executeSuccess and len(msg) > 0:
                            msg = str(result_obj["message"])
                        if is_ok:
                            self.checkResult(taskUUID, result_obj)
                        taskUtils.taskPrint(taskUUID, f"{current_thread().name}=== notify {service_country} task({taskUUID}) complate ")
                        taskUtils.saveCounter(taskUUID, (calendar.timegm(time.gmtime()) - _taskCreateTime(taskUUID)), is_ok)
                        if xy_pb.TaskNotify(service_country, taskUUID, is_ok, msg, 
                                            json.dumps(result_obj["result"], separators=(',', ':'))):
                            taskUtils.taskPrint(taskUUID, f"{current_thread().name}=== {service_country} task : {taskUUID} notify server success")
                            if is_ok == False:
                                taskUtils.notifyTaskFail(taskUUID, msg)
                        else:
                            taskUtils.taskPrint(taskUUID, f"{current_thread().name}=== {service_country} task : {taskUUID} server fail~~")
                            taskUtils.notifyScriptError(taskUUID, cmd)
                        _removeTask(taskUUID)
                except Exception as e:
                    taskUtils.taskPrint(taskUUID, f"{current_thread().name}=== {service_country} task exception : {e}")
                    taskUtils.notifyScriptError(taskUUID, cmd)
                finally:
                    taskUtils.taskPrint(taskUUID, None)
            time.sleep(1)
        print(f"   {current_thread().name} stop")

    def markStop(self):
        print(f"   {current_thread().name} waiting stop")