from ..scheduleService import ScheduleBase
from .. import applicationContext

class MqttCheckMessageJob(ScheduleBase):

  """
  * 中断处理 接收mqtt消息
  """
  def handleInterrupt(self):
    applicationContext.pervasiveMqttClient.check_msg() 



    