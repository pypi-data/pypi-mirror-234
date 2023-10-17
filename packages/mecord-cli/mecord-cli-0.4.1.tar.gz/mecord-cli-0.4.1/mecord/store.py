import os
import json
from mecord import utils

def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner

def updateIfNeed():
    thisDir = os.path.dirname(os.path.abspath(__file__))
    for root,dirs,files in os.walk(thisDir):
        for file in files:
            if "_test.json" in file:
                pname = file.replace("_test", "")
                if os.path.exists(os.path.join(root, pname)):
                    os.remove(os.path.join(root, pname))
                os.rename(os.path.join(root, file), os.path.join(root, pname))
            if os.path.exists(os.path.join(root, "env.txt")):
                os.remove(os.path.join(root, "env.txt"))
        if root != files:
            break

@singleton
class Store(object):

    def __init__(self):
        uuid = utils.generate_unique_id()
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"data_{uuid}.json")

        # update with pengjun
        # remove env , all product env -> test env
        updateIfNeed()
        
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                json.dump({}, f)
                
    def read(self):
        with open(self.path, 'r') as f:
            data = json.load(f)
            
        return data
    
    def write(self, data):
        with open(self.path, 'w') as f:
            json.dump(data, f)

def groupUUID():
    sp = Store()
    read_data = sp.read()
    if "groupUUID" in read_data:
        return read_data["groupUUID"]
    else:
        return ""
    
def token():
    sp = Store()
    read_data = sp.read()
    if "token" in read_data:
        return read_data["token"]
    else:
        return ""
    
def multitaskNum():
    sp = Store()
    read_data = sp.read()
    if "multitasking_num" in read_data:
        return read_data["multitasking_num"]
    else:
        return 1

def setMultitaskNum(num):
    sp = Store()
    read_data = sp.read()
    read_data["multitasking_num"] = num
    sp.write(read_data)
    
#============================== widget ================================
def isCreateWidget():
    sp = Store()
    read_data = sp.read()
    if "isCreateWidget" in read_data:
        return read_data["isCreateWidget"]
    else:
        return False
    
def finishCreateWidget():
    sp = Store()
    read_data = sp.read()
    read_data["isCreateWidget"] = False
    sp.write(read_data)

def widgetMap():
    sp = Store()
    read_data = sp.read()
    if "widgets" in read_data:
        return read_data["widgets"]
    else:
        return {}
    
def insertWidget(widget_id, path):
    sp = Store()
    read_data = sp.read()
    if "widgets" not in read_data:
        read_data["widgets"] = {}
    widgetsMap = read_data["widgets"]
    widgetsMap[widget_id] = {
        "isBlock": False,
        "path" : path
    }
    for k in list(widgetsMap.keys()):
        if isinstance(widgetsMap[k], (dict)):
            if os.path.exists(widgetsMap[k]["path"]) == False:
                del widgetsMap[k]
        else:
            if os.path.exists(widgetsMap[k]) == False:
                del widgetsMap[k]
    sp.write(read_data)

def removeWidget(widget_id):
    sp = Store()
    read_data = sp.read()
    if "widgets" not in read_data:
        read_data["widgets"] = {}
    widgetsMap = read_data["widgets"]
    if widget_id in widgetsMap:
        del widgetsMap[widget_id]
    sp.write(read_data)
    
def disableWidget(widget_id):
    sp = Store()
    read_data = sp.read()
    if "widgets" not in read_data:
        read_data["widgets"] = {}
    widgetsMap = read_data["widgets"]
    if widget_id in widgetsMap:
        if isinstance(widgetsMap[widget_id], (dict)):
            widgetsMap[widget_id]["isBlock"] = True
        else:
            path = widgetsMap[widget_id]
            widgetsMap[widget_id] = {
                "isBlock": True,
                "path" : path
            }
    sp.write(read_data)

def enableWidget(widget_id):
    sp = Store()
    read_data = sp.read()
    if "widgets" not in read_data:
        read_data["widgets"] = {}
    widgetsMap = read_data["widgets"]
    if widget_id in widgetsMap:
        if isinstance(widgetsMap[widget_id], (dict)):
            widgetsMap[widget_id]["isBlock"] = False
        else:
            path = widgetsMap[widget_id]
            widgetsMap[widget_id] = {
                "isBlock": False,
                "path" : path
            }
    sp.write(read_data)
    
#============================== device id ================================

def writeDeviceInfo(data):
    sp = Store()
    read_data = sp.read()
    read_data["deviceInfo"] = data
    sp.write(read_data)
    
def readDeviceInfo():
    sp = Store()
    read_data = sp.read()
    if "deviceInfo" in read_data:
        return read_data["deviceInfo"]
    else:
        return {}

# def clear():
#     sp = Store()
#     sp.write({})

def is_product():    
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "start.env")
    try:
        with open(env_file, 'r', encoding='UTF-8') as f:
            v = int(f.read())
            if v == 1:
                return True
            return False
    except:
        return False
    
def save_product(b):
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "start.env")
    try:
        with open(env_file, 'w') as f:
            f.write(str(1 if b else 0))
    except:
        return