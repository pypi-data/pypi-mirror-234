import base64
import time
import signal
import threading
import qrcode_terminal

from mecord import store 
from mecord import xy_pb 
from mecord import utils 

def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner

@singleton
class User(object):
    logined = False
    login_data = None

    def __init__(self):
        self.checkLoginStatus()

    def checkLoginStatus(self):
        if store.groupUUID() and store.token():
            self.logined = True
            return True
        self.logined = False        
        
    def isLogin(self):
        self.checkLoginStatus()
        if self.logined == False:
            #try get login info once
            self.loginIfNeed()
        return self.logined
    
    def logout(self):
        store.clear()
        self.logined = False

    def loginIfNeed(self):
        if xy_pb.GetAigcDeviceInfo():
            self.checkLoginStatus()

    #     if self.isLogin() == False:
    #         #need login
    #         logincode = xy_pb.GetQrcodeLoginCode()
    #         if logincode:
    #             logincode_encoded = base64.b64encode(bytes(logincode, encoding='UTF-8')).decode(encoding='UTF-8').replace("==","fuckEqual")
    #             uuid = utils.generate_unique_id()
    #             qrcode = f"https://main_page.html?action=scan&code={logincode_encoded}&deviceCode=143383612&deviceId={uuid}"
    #             utils.displayQrcode(qrcode)
    #             # qrcode_terminal.draw(qrcode)
    #             # print(qrcode)
    #             # utils.displayQRcodeOnTerminal(qrcode)
    #             self.checkLoginComplete(logincode)
    #             print("waiting for scan qrcode & login complete ~~~")

    # def checkLoginComplete(self, qrcode):
    #     rst = xy_pb.CheckLoginLoop(qrcode)
    #     if rst == 1: #success
    #         print("login success")
    #         self.logined = True
    #     elif rst == -1:
    #         threading.Timer(1, self.checkLoginComplete, (qrcode, )).start()
    #     else: #fail
    #         print("login fail !!!")