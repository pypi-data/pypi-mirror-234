import json
import sys

resultDic = {
    "result" : [ 
    ],
    "status" : 0,           #0 is success
    "message" : ""
}

## 输入data参数, JSON格式如下: 
#   {
#      "task_id": [task_id],                    #任务id
#      "widget_id": [widget_id],                #组件id
#      "pending_count": [pending_count],        #待处理任务数
#      "fn_name": "test",
#      "param": {
#          "text":"Hello World"
#      }
#   }
def runTask(data):
    #write program in here
    demoReturnText = "hello world"
    
    resultDic["result"].append({
        "type" : "text",
        "content": [ 
            demoReturnText
        ],
        "extension" : {
            "info": "",
            "cover_url": ""
        }
    })
    return resultDic
