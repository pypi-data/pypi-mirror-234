from ..core.serverInvoker import CapabilityInvoker
from .. import config
import json
from ..core import applicationContext
from ..utils import TimeUtil
from ..utils import logutil
from ..systemService import updateService
import sys

routerLog = logutil.get_logger(__name__+" MQTT router")
serviceLog = logutil.get_logger(__name__ + " service invoke")
updateLog = logutil.get_logger(__name__ + " update invoke")

def topicRouter(topic,msg):
  
  topic = topic.split("/")
  print(topic)

  # 调用能力接口
  if topic[2] == config.INCOCATION_ENUM:
    msgJson = json.loads(msg)
    msgId = msgJson.get("messageId","null")
    runSuccess = False
    responce = None
    routerLog.info("======mqtt server invoke======",msgId)
    try:
      responce = CapabilityInvoker.invokeCapability(topic[-2],topic[-1],msgJson["param"])
      runSuccess = True
    except Exception as e:
      serviceLog.error(str(e))
      runSuccess = False
      responce = {"errorMsg":str(e)}
    routerLog.info("====callback====")
    # 拼接topic
    callbackTopic = config.INVOCATION_SERVICE_CALLBACK_TOPIC
    callbackTopic = callbackTopic.replace("${service}",topic[-2])
    callbackTopic = callbackTopic.replace("${capability}",topic[-1])
    callbackTopic = callbackTopic.replace("${msgid}",msgId)
    if (msgId==None):
        serviceLog.error("The message body does not contain the 'messageId'")
    routerLog.info(callbackTopic)
    # 拼接msg
    msgDict = {
      "success" : runSuccess,
      "data" : responce,
      "timestamp": TimeUtil.getTimerMs()
    }
    routerLog.info(msgDict)
    applicationContext.pervasiveMqttClient.sendMsg(callbackTopic,json.dumps(msgDict, ensure_ascii=False))
  # 脚本更新能力
  elif topic[2] == config.UPDATE_ENUM:
    msgJson = json.loads(msg)
    print(msgJson)
    msgId = msgJson.get("messageId","null")
    isInstall = msgJson.get("installStatus",True)
    # 拼接topic
    callbackTopic = config.UPDATE_SERVICE_CALLBACK_TOPIC
    callbackTopic = callbackTopic.replace("${service}","download")
    callbackTopic = callbackTopic.replace("${msgid}",msgId)
    runSuccess = True
    responce = {}
    try :
      if isInstall:
        routerLog.info("======mqtt update service======")
        callbackTopic = callbackTopic.replace("${capability}","install")
        updateService.updateService(topic[4])
      else:
        routerLog.info("======mqtt delete service======")
        callbackTopic = callbackTopic.replace("${capability}","uninstall")
        updateService.deleteService(topic[4])
    except Exception as e:
        runSuccess = False
        updateLog.error(str(e))
        # sys.print_exception(e)
        responce = {"errorMsg":str(e)}
    msgDict = {
      "success" : runSuccess,
      "timestamp": TimeUtil.getTimerMs(),
      "data":responce
    }
    applicationContext.pervasiveMqttClient.sendMsg(callbackTopic,json.dumps(msgDict, ensure_ascii=False))
  else:
    routerLog.error("no topic path")
   


