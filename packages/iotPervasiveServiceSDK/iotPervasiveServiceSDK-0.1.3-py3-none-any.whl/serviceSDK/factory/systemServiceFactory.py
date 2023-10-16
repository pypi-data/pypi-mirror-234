from ..pojo.serviceBean import ServiceBean
from . import systemEventFactory
from .. import config

'''
* 系统自带的service
* 系统服务工厂
'''
class SystemServiceFactory:
  def loadSystemService()-> ServiceBean:
    res = ServiceBean()
    res.url = "systemService"
    res.name = "systemService"
    res.versionCode = 0
    eventBeanDict = {}
    
    online = systemEventFactory.createSystemEvent("ONLINE",config.ON_EVENT_TOPIC)
    offline = systemEventFactory.createSystemEvent("OFFLINE",config.ON_EVENT_TOPIC)

    eventBeanDict[online.eventId] = online
    eventBeanDict[offline.eventId] = offline

    res.eventBeanDict = eventBeanDict
    return res