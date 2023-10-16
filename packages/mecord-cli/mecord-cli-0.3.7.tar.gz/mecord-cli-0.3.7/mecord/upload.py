import requests
import os
from urllib.parse import *

from mecord import xy_pb
from mecord import store
from mecord import utils
from mecord import mecord_service
from pathlib import Path

def upload(src):
    if os.path.exists(src) == False:
        raise Exception(f"upload file not found")

    file_name = Path(src).name
    country = store.getCurrentServiceCountry()
    ossurl, content_type = xy_pb.GetOssUrl(country, os.path.splitext(file_name)[-1][1:])
    if len(ossurl) == 0:
        raise Exception(f"oss server is not avalid, msg = {content_type}")

    headers = dict()
    headers['Content-Type'] = content_type
    requests.adapters.DEFAULT_RETRIES = 3
    s = requests.session()
    s.keep_alive = False
    res = s.put(ossurl, data=open(src, 'rb').read(), headers=headers)
    s.close()
    if res.status_code == 200:
        realOssUrl = urljoin(ossurl, "?s")
        return realOssUrl
    else:
        raise Exception(f"upload file fail! res = {res}")

def uploadWidget(src, widgetid):
    ossurl, content_type = xy_pb.GetWidgetOssUrl(widgetid)
    if len(ossurl) == 0:
        raise Exception("oss server is not avalid")
    
    headers = dict()
    headers['Content-Type'] = content_type
    requests.adapters.DEFAULT_RETRIES = 3
    s = requests.session()
    s.keep_alive = False
    res = s.put(ossurl, data=open(src, 'rb').read(), headers=headers)
    s.close()
    if res.status_code == 200:
        realOssUrl = urljoin(ossurl, "?s")
        checkid = xy_pb.WidgetUploadEnd(realOssUrl)
        if checkid > 0:
            return realOssUrl, checkid
        else:
            raise Exception("check fail!")
    else:
        raise Exception(f"upload file fail! res = {res}")

def uploadModel(name, cover, model_url, type):
    curTaskUUID = store.getCurrentTaskUUID()
    country = store.getCurrentServiceCountry()
    if len(curTaskUUID) > 0:
        return xy_pb.UploadMarketModel(country, name, cover, model_url, type, curTaskUUID)
    else:
        raise Exception("no task running!")
    
    