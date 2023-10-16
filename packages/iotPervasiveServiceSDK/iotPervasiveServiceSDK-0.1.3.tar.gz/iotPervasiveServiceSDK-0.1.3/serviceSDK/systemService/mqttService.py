from paho.mqtt.client import Client as MQTTClient
from ..core.scheduleService import ScheduleBase
from .. import config

# from ..router import httpRouter

import json
import _thread
from ..utils import logutil
import uuid

log = logutil.get_logger(__name__)

# 泛在云mqtt服务
class MqttService(ScheduleBase):
  #mqtt客户端
  client = None
  deviceId = "Unknown Device"
  lock=_thread.allocate_lock()

  
  """
  * deviceId   泛在平台设备id
  * address   mqtt地址
  * port  mqtt端口号
  """
  def __init__(self,deviceId:str,address:str=config.MQTT_ADDRESS ,port=config.MQTT_PORT):
    print(address)
    print(port)
    self.deviceId = deviceId
    if address == config.MQTT_ADDRESS and port == config.MQTT_PORT:
        self._SystemMqttInit()
    else:
        self._MqttInit(address,port)
    print("MQTT Init Success")

    

  '''
  * 消息监听
  '''
  def check_msg(self):
    try:
      self.client.loop()
    except Exception as e:
      log.error(f"消息监听失败: {str(e)}")
    

  """
  * mqtt初始化
  """
  def _SystemMqttInit(self):
    log.info("init mqtt")
    self.client = MQTTClient(self.deviceId,clean_session=True)  # 创建MQTT对象
    willMsg = {
      "deviceInstanceId":config.DEVICE_ID,
      "serviceUrl": "systemService",
	    "versionCode": 0,
	    "eventId": "OFFLINE",
	    "msg": None
      }
    self.client.will_set(topic = config.ON_EVENT_TOPIC, payload=json.dumps(willMsg, ensure_ascii=False))

    # 设置连接和消息回调函数
    self.client.on_connect = self.on_connect
    self.client.on_message = self.sub_cb

    self.client.connect(host = config.MQTT_ADDRESS, port = config.MQTT_PORT, keepalive = 60)
    # 开始循环处理网络流量和消息回调
    self.client.loop()


  """
  * mqtt初始化
  """
  def _MqttInit(self,address:str,port:int):
    self.client = MQTTClient(self.deviceId + str(uuid.uuid1()))  # 创建MQTT对象
    self.client.connect(host = address, port = port, keepalive = 60)


  """
  * 发送消息
  * topIc 主题消息 字符串消息
  * message 一般为一个json格式的字符串
  """
  def sendMsg(self,topic:str,message:str):
    if self.lock.acquire():
        try:
            self.client.publish(topic,message,qos=2)
        except :
            self._SystemMqttInit()
        finally :
            self.lock.release()

  def ping(self):
    self.client.ping()


  """
  * 消息回调
  """
  def sub_cb(self, client, userdata, msg):
    try:
      from ..router import mqttRouter
      topic = msg.topic
      msg = msg.payload.decode()
      mqttRouter.topicRouter(topic,msg)
    except Exception as e:
      log.error(f" {str(e)}")
  
  def close(self):
    self.client.disconnect()


  # 定义 MQTT 客户端的回调函数
  def on_connect(self, client, userdata, flags, rc):
    if rc == 0:
      # 消息订阅    
      client.subscribe(config.INVOCATION_SERVICE_EXECUTE_TOPIC)
      client.subscribe(config.UPDATE_SERVICE_TOPIC)
      log.info("系统mqtt初始化成功")
    else:
      log.error("Failed to connect, return code {0}".format(rc))




