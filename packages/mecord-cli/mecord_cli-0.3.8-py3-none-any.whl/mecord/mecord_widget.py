import os
import json
import sys
import shutil
import zipfile
import pkg_resources
import threading
import time
import requests
import random

from pathlib import Path
from mecord import store
from mecord import xy_pb
from mecord import upload
from mecord import utils

h5_name = "h5"
script_name = "script"
def GetWidgetConfig(path):
    #search h5 folder first, netxt search this folder
    if os.path.exists(os.path.join(path, h5_name)):
        for filename in os.listdir(os.path.join(path, h5_name)):
            pathname = os.path.join(path, h5_name, filename) 
            if (os.path.isfile(pathname)) and filename == "config.json":
                with open(pathname, 'r', encoding='UTF-8') as f:
                    return json.load(f)
    for filename in os.listdir(path):
        pathname = os.path.join(path, filename) 
        if (os.path.isfile(pathname)) and filename == "config.json":
            with open(pathname, 'r', encoding='UTF-8') as f:
                return json.load(f)
    return {}
    
def GetWidgetConfigWithId(widget_id):
    map = store.widgetMap()
    for it in map:
        if it.strip() == widget_id.strip():
            path = os.path.dirname(map[it])
            data = GetWidgetConfig(path)
            return data
    return {}

def folderIsH5(path):
    configFileExist = False
    iconFileExist = False
    htmlFileExist = False
    for filename in os.listdir(path):
        pathname = os.path.join(path, filename) 
        if (os.path.isfile(pathname)) and filename == "config.json":
            configFileExist = True
        if (os.path.isfile(pathname)) and filename == "icon.png":
            iconFileExist = True
        if (os.path.isfile(pathname)) and filename == "index.html":
            htmlFileExist = True
    return configFileExist and iconFileExist and htmlFileExist

def PathIsEmpty(path):
    return len(os.listdir(path)) == 0

def checkImportMecordJs(h5Root):
    jsPath = os.path.join(h5Root, "MekongJS.js")
    jsPathTmp = os.path.join(h5Root, "MekongJS.js.py")
    s = requests.session()
    s.keep_alive = False
    js_res = s.get(f"https://www.mecordai.com/prod/mecord/commonality/MecordJS/MecordJS.min.js?t={random.randint(100,99999999)}")
    with open(jsPathTmp, "wb") as c:
        c.write(js_res.content)
    if os.path.exists(jsPathTmp):
        if os.path.exists(jsPath):
            os.remove(jsPath)
        os.rename(jsPathTmp, jsPath)
    s.close()


def replaceIfNeed(dstDir, name, subfix):
    newsubfix = subfix + ".py"
    if name.find(newsubfix) != -1:
        os.rename(os.path.join(dstDir, name), os.path.join(dstDir, name.replace(newsubfix, subfix)))

def copyWidgetTemplate(root, name, dirname):
    templateDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)#sys.prefix
    dstDir = os.path.join(root, dirname)
    shutil.copytree(templateDir, dstDir)
    shutil.rmtree(os.path.join(dstDir, "__pycache__"))
    os.remove(os.path.join(dstDir, "__init__.py"))
    for filename in os.listdir(dstDir):
        replaceIfNeed(dstDir, filename, ".json")
        replaceIfNeed(dstDir, filename, ".js")
        replaceIfNeed(dstDir, filename, ".png")
        replaceIfNeed(dstDir, filename, ".html")

def createDemoWidget():
    demoZipFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo.zip")
    demoDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo")
    if os.path.exists(demoDir):
        shutil.rmtree(demoDir)
    os.makedirs(demoDir)
    
    s = requests.session()
    s.keep_alive = False
    file = s.get(f"https://mecord-web.oss-accelerate.aliyuncs.com/res/UploadWidget.zip?t={random.randint(100,99999999)}", verify=False)
    with open(demoZipFile, "wb") as c:
        c.write(file.content)
    s.close()
    if os.path.exists(demoZipFile):
        with zipfile.ZipFile(demoZipFile, "r") as zipf:
            zipf.extractall(demoDir)
        widgetid = xy_pb.CreateWidgetUUID()
        if len(widgetid) == 0:
            print("create demoWidget fail! mecord server is not avalid")
            return
        setWidgetData(demoDir, widgetid)
        addWidgetToEnv(os.path.join(demoDir, script_name))
    else: #if somthing wrong, use plan b
        createWidget(demoDir)
    publishWidget(demoDir)

default_max_task_number = 10
def setWidgetData(root, widgetid):
    #h5
    data = GetWidgetConfig(root)
    data["parent_widget_id"] = ""
    data["widget_id"] = widgetid
    data["group_id"] = store.groupUUID()
    data["device_keys"] = [
        utils.generate_unique_id()
    ]
    data["cmd"] = os.path.join(root, script_name, "main.py")
    data["max_task_number"] = default_max_task_number
    with open(os.path.join(root, h5_name, "config.json"), 'w') as f:
        json.dump(data, f)
    checkImportMecordJs(os.path.join(root, h5_name))
    #script
    with open(os.path.join(root, script_name, "config.json"), 'w') as f:
        json.dump({"widget_id": widgetid}, f)

def createWidget(root):
    if PathIsEmpty(root) == False:
        print("current folder is not empty, create widget fail!")
        return
        
    widgetid = xy_pb.CreateWidgetUUID()
    if len(widgetid) == 0:
        print("create widget fail! mecord server is not avalid")
        return
    
    copyWidgetTemplate(root, "widget_template", h5_name)
    copyWidgetTemplate(root, "script_template", script_name)
    setWidgetData(root, widgetid)
    addWidgetToEnv(os.path.join(root, script_name))
    print("create widget success")

def CheckWidgetDataInPath(path):
    data = GetWidgetConfig(path)
    if "widget_id" not in data:
        print("folder is not widget")
        return False

    if "widget_id" in data:
        widget_id = data["widget_id"]
        if len(widget_id) == 0:
            print("widget_id is empty!")
            return False
        
    return True

def addWidgetToEnv(root):
    if CheckWidgetDataInPath(root) == False:
        return
        
    data = GetWidgetConfig(root)
    widget_id = data["widget_id"]
    mainPythonPath = os.path.join(root, "main.py")
    if os.path.exists(os.path.join(root, script_name)):
        mainPythonPath = os.path.join(root, script_name, "main.py")
    if store.insertWidget(widget_id, mainPythonPath):
        print(f"add {widget_id.ljust(len(widget_id)+4)} {mainPythonPath}")

def remove(args):
    widget_id = args
    if os.path.exists(args):
        #find widgetid in args path
        data = GetWidgetConfig(args)
        if "widget_id" not in data:
            print(f"path {args} is not widget folder!")
            return
        widget_id = data["widget_id"]
    if xy_pb.DeleteWidget(widget_id):
        store.removeWidget(widget_id)
        print(f"widget:{widget_id} is removed from mecord server")
        
def enable(args):
    widget_id = args
    if os.path.exists(args):
        #find widgetid in args path
        data = GetWidgetConfig(args)
        if "widget_id" not in data:
            print(f"path {args} is not widget folder!")
            return
        widget_id = data["widget_id"]
    store.enableWidget(widget_id)
    print(f"widget:{widget_id} updated")
        
def disable(args):
    widget_id = args
    if os.path.exists(args):
        #find widgetid in args path
        data = GetWidgetConfig(args)
        if "widget_id" not in data:
            print(f"path {args} is not widget folder!")
            return
        widget_id = data["widget_id"]
    store.disableWidget(widget_id)
    print(f"widget:{widget_id} updated")
        
def getTaskCount(args):
    widget_id = args
    if os.path.exists(args):
        #find widgetid in args path
        data = GetWidgetConfig(args)
        if "widget_id" not in data:
            print(f"path {args} is not widget folder!")
            return
        widget_id = data["widget_id"]
    datas = xy_pb.GetTaskCount(widget_id)
    for it in datas:
        if it["widgetUUID"] == widget_id:
            return it["taskCount"]
    return -1

def publishWidget(root):
    if CheckWidgetDataInPath(root) == False:
        return
    #h5 folder
    package_folder = ""
    script_folder = ""
    if folderIsH5(root):
        package_folder = root
    elif folderIsH5(os.path.join(root, h5_name)):
        script_folder = os.path.join(root, script_name)
        package_folder = os.path.join(root, h5_name) 
        
    data = GetWidgetConfig(package_folder)
    widget_id = data["widget_id"]
    group_id = data["group_id"]

    # #check permission
    # changeOwner = False
    # hasPermission = group_id == store.groupUUID()
    # if hasPermission == False:
    #     inputed = False
    #     while inputed == False:
    #         print(f"you do not have permission to access widget:[{widget_id}]")
    #         word = input("do you want to override it? Y/n:")
    #         if "Y" in word:
    #             changeOwner = True
    #         inputed = True
    # if hasPermission == False and changeOwner == False:
    #     print("publish abandon")
    #     return
    
    # #override setting
    # if changeOwner:
    #     device_keys = data["device_keys"]
    #     deviceHasMe = False
    #     for it in device_keys:
    #         if it == utils.generate_unique_id():
    #             deviceHasMe = True
    #     if deviceHasMe == False:
    #         device_keys.append(utils.generate_unique_id())
    #     data["device_keys"] = device_keys
    #     data["parent_widget_id"] = widget_id
    #     newWidgetid = xy_pb.CreateWidgetUUID()
    #     if len(newWidgetid) == 0:
    #         print("override fail! mecord server is not avalid")
    #         return
    #     data["widget_id"] = newWidgetid
    #     data["group_id"] = store.groupUUID()
    #     with open(os.path.join(package_folder, "config.json"), 'w') as f:
    #         json.dump(data, f)
    #     #script
    #     if len(script_folder) > 0:
    #         with open(os.path.join(script_folder, "config.json"), 'w') as f:
    #             json.dump({"widget_id": newWidgetid}, f)
    #     widget_id = newWidgetid
        
    #if in h5&script parent folder, add env path
    if len(script_folder) > 0:
        addWidgetToEnv(script_folder)
        
    distname = utils.generate_unique_id() + "_" + widget_id
    dist = os.path.join(os.path.dirname(package_folder), distname + ".zip")
    zip = zipfile.ZipFile(dist, "w", zipfile.ZIP_DEFLATED) 

    checkImportMecordJs(package_folder)
    for rt,dirs,files in os.walk(package_folder):
        for file in files:
            if str(file).startswith("~$"):
                continue
            filepath = os.path.join(rt, file)
            writepath = os.path.relpath(filepath, package_folder)
            zip.write(filepath, writepath)
    zip.close()
    (ossurl, checkid) = upload.uploadWidget(dist, widget_id)
    if checkid > 0:
        checkUploadComplete(checkid, dist)
    else:
        os.remove(dist)

def checkUploadComplete(checkid, dist):
    rst = xy_pb.UploadWidgetCheck(checkid)
    if rst == 1: #success
        print("publish widget success")
        # xy_pb.UploadWidget(widget_id, ossurl)  #暂时不用
        os.remove(dist)
        store.finishCreateWidget()
    elif rst == -1:
        threading.Timer(1, checkUploadComplete, (checkid, dist, )).start()
    else: #fail
        print("publish fail")
        return
