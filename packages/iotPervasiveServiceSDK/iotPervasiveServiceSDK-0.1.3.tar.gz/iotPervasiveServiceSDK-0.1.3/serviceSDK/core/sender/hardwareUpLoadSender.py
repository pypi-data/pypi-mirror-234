from .. import applicationContext
from ... import config
from .baseSender import BaseSender
import json

class HardwareUpLoadSender(BaseSender):

  def send():
    hardwareInfo = applicationContext.hardwareInfoLoader.getHardwareInfo()
    applicationContext.pervasiveMqttClient.sendMsg(config.UPLOAD_HARDWARE_TOPIC,json.dumps(hardwareInfo, ensure_ascii=False))