from ..core.scheduleService import ScheduleService
from ..systemService.mqttService import MqttService
from .loader.hardwareInfoLoader import HardwareInfoLoader
from ..import config
from datetime import datetime


# 代理加载存储字典
proxyDict:dict = None

# 服务加载存储字典
serviceDict:dict = None

stateInfo:dict = None

# mqtt客户端
pervasiveMqttClient:MqttService = None


# 定时器
taskServer:ScheduleService = None

# 硬件信息加载器
hardwareInfoLoader:HardwareInfoLoader = None

"""
* 返回service信息列表，每个节点是一个字典格式：
* {
*    'versionCode':服务版本号，
*    'id':服务id,
*    'serviceId':服务id,与上面id等价
* }
"""
def getServiceListInfo():
    services = []
    for key in serviceDict.keys():
        serviceItem= serviceDict[key].__dict__
        serviceItem =  {
            'versionCode': serviceItem['versionCode'],
            'id': serviceItem['url'],
            'serviceId': serviceItem['url']
        }
        services.append(serviceItem)
    return services

"""
* 返回service列表，每个节点是一个ServiceBean
"""
def getServiceList():
    services = []
    for key in serviceDict.keys():
        serviceItem = serviceDict[key]
        services.append(serviceItem)
    return services


def getSystemInfo():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%S")
    resDict = {
        "deviceId":config.DEVICE_ID,
        "dateTime":formatted_time,
        "stateInfo":stateInfo,
        "hardwareInfo":hardwareInfoLoader.getHardwareInfo()
    }
    return resDict
