from ..scheduleService import ScheduleBase
from ...proxy.thingProxy import thingProxy
from .. import applicationContext
 
class EventListenerJob(ScheduleBase):
  
  """
  * 监听事件
  """
  def handleInterrupt(self):
    thingModel = thingProxy({"operation":"read"}).handle(None)
    print(thingModel)
    for event in applicationContext.events:
        applicationContext.pervasiveMqttClient.sendMsg("/service/event/test","test")
#     print(self.events)
