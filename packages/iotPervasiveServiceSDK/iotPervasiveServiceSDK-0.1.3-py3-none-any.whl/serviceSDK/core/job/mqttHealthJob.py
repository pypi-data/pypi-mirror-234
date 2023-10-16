from ..scheduleService import ScheduleBase
from .. import applicationContext


class MqttHealthJob(ScheduleBase):

  """
  * 发送心跳包
  """
  def handleInterrupt(self):
    print("beat")
    # applicationContext.pervasiveMqttClient.ping()