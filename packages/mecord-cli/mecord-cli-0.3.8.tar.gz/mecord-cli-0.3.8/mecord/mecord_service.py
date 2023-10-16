import os
import sys
import time
import signal
import subprocess
import json
import platform
import psutil
from pathlib import Path
from urllib.parse import *
import socket
import calendar

from mecord import store
from mecord import xy_pb
from mecord import xy_user 
from mecord import utils
from mecord import progress_monitor

pid_file = utils.pid_file
stop_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stop.now")
class BaseService:
    def __init__(self, name):
        self.name = name
        self.running = False

    def start(self):
        with open(pid_file, 'w') as f:
            f.write(str(os.getpid()))
        self.running = True
        signal.signal(signal.SIGTERM, self.stop)
        self.run()
    
    def isIdling(self, cnt):
        if cnt >= (60*60) and cnt % (60*60) == 0:
            utils.idlingService(cnt)

    def run(self):
        idling_counter = 0
        while (os.path.exists(stop_file) == False):
            if self.run_internal() > 0:
                idling_counter = 0
            else:
                idling_counter += 1
            self.isIdling(idling_counter)
            time.sleep(1)
        if pid_file and os.path.exists(pid_file):
            os.remove(pid_file)
        print("MecordService stoped!")
        if os.path.exists(stop_file):
            os.remove(stop_file)
        store.save_product(False)

    def stop(self, signum=None, frame=None):
        with open(stop_file, 'w') as f:
            f.write("")
        self.running = False
        print("MecordService waiting stop...")
        while os.path.exists(stop_file):
            time.sleep(1)

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
            return self.running
    
class MecordService(BaseService):
    def __init__(self):
        super().__init__("MecordService")

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
        utils.taskPrint(f"exec => {command}")
        try:
            path = os.path.dirname(cmd)
            config_file = os.path.join(path, 'config.json')
            with open(config_file, "r") as f:
                data = json.load(f)

            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            if data is not None and 'type' in data and data['type'].lower() == 'sd':
                widget_infos = [{"widget":"SD", "port":6006, "name":"", "path":path}]
            else:
                widget_infos = [{"widget":"other", "port":"", "name":"", "pid": process.pid, "path":path}]
            # utils.taskPrint(f"monitor process: {path}")
            # progress_monitor.start(widget_infos)
            output, error = process.communicate(timeout=60*60)
            # progress_monitor.stop()
            if process.returncode == 0:
                utils.taskPrint(output.decode(encoding="utf8", errors="ignore"))
                if os.path.exists(outArgs):
                    with open(outArgs, 'r', encoding='UTF-8') as f:
                        outData = json.load(f)
                    executeSuccess = True
                    utils.taskPrint(f"exec success result => {outData}")
                else:
                    utils.taskPrint(f"task {taskUUID} result is empty!, please check {cmd}")
            else:
                utils.taskPrint("====================== script error ======================")
                o1 = output.decode(encoding="utf8", errors="ignore")
                o2 = error.decode(encoding="utf8", errors="ignore")
                utils.taskPrint(f"{o1}\n{o2}")
                utils.taskPrint("======================     end      ======================")
                utils.notifyScriptError(taskUUID, cmd)
        except Exception as e:
            utils.taskPrint("====================== process error ======================")
            utils.taskPrint(e)
            utils.taskPrint("======================      end      ======================")
            utils.notifyScriptError(taskUUID, cmd)
        finally:
            if os.path.exists(inputArgs):
                os.remove(inputArgs)
            if os.path.exists(outArgs):
                os.remove(outArgs)
        return executeSuccess, outData,

    def needChangeValue(self, data, type, key):
        if "type" not in data:
            utils.taskPrint("result is not avalid")
            return False
        if data["type"] != type:
            return False
        if "extension" not in data or key not in data["extension"] or len(data["extension"][key]) == 0:
            return True
        return False
             
    def checkResult(self, data):
        for it in data["result"]:
            if self.needChangeValue(it, "text", "cover_url"):
                it["extension"]["cover_url"] = ""
            if self.needChangeValue(it, "audio", "cover_url"):
                it["extension"]["cover_url"] = ""
            if self.needChangeValue(it, "image", "cover_url"):
                it["extension"]["cover_url"] = ""
            if self.needChangeValue(it, "video", "cover_url"):
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

    def start(self, isProduct=False):
        if os.path.exists(pid_file):
            #check pre process is finish successed!
            with open(pid_file, 'r') as f:
                pre_pid = str(f.read())
            if len(pre_pid) > 0:
                if utils.process_is_zombie_but_cannot_kill(int(pre_pid)):
                    print(f'start service fail! pre process {pre_pid} is uninterruptible sleep')
                    utils.notifyWechatRobot({
                        "msgtype": "text",
                        "text": {
                            "content": f"机器<{socket.gethostname()}>无法启动服务 进程<{pre_pid}>为 uninterruptible sleep"
                        }
                    })
                    return False
        store.save_product(isProduct)
        store.writeDeviceInfo(utils.deviceInfo())
        store.setCurrentTaskUUID("")
        store.setCurrentServiceCountry("US")
        super().start()

    def run_internal(self):
        processed_count = 0
        for service_country in xy_pb.supportCountrys(store.is_product()):
            taskUUID = ""
            try:
                if len(store.token()) <= 0:
                    self.stop()
                    return

                store.setCurrentServiceCountry(service_country)
                datas = xy_pb.GetTask(service_country)
                for it in datas:
                    taskUUID = it["taskUUID"]
                    utils.taskPrint(f"=== receive {service_country} task : {taskUUID}", True)
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
                    start_time = calendar.timegm(time.gmtime())
                    utils.taskPrint(f"=== start execute {service_country} task : {taskUUID}")
                    store.setCurrentTaskUUID(taskUUID)
                    executeSuccess, result_obj = self.executeLocalPython(taskUUID, cmd, params)
                    store.setCurrentTaskUUID("")
                    #result
                    is_ok = executeSuccess and result_obj["status"] == 0
                    msg = "Unknow Error"
                    if executeSuccess and len(msg) > 0:
                        msg = str(result_obj["message"])
                    if is_ok:
                        self.checkResult(result_obj)
                    utils.taskPrint(f"=== notify {service_country} task({taskUUID}) complate ")
                    utils.saveCounter(taskUUID, (calendar.timegm(time.gmtime()) - start_time), is_ok)
                    if xy_pb.TaskNotify(service_country, taskUUID, is_ok, msg, 
                                        json.dumps(result_obj["result"], separators=(',', ':'))):
                        utils.taskPrint(f"{service_country} task : {taskUUID} notify server success")
                        if is_ok == False:
                            utils.notifyTaskFail(taskUUID, msg)
                    else:
                        utils.taskPrint(f"{service_country} task : {taskUUID} server fail~~")
                        utils.notifyScriptError(taskUUID, cmd)
                    processed_count += 1
            except Exception as e:
                utils.taskPrint(f"=== {service_country} task exception : {e}")
                utils.notifyScriptError(taskUUID, cmd)
        return processed_count
        
    def status_ok(self):
        service_running = super()._is_running()
        socket_running = True #self.socket.isRunning()
        is_login =xy_user.User().isLogin()
        return socket_running and service_running and is_login