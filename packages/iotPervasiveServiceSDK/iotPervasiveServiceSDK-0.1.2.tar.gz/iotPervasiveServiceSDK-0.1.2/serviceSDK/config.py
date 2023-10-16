from .utils import pathUtils as PathUtil

BASE_NAME = "SDK"

# 设备实例id
DEVICE_ID = "UnknownDevice"

# topic 
INCOCATION_ENUM = 'invocation' 
CALLBACK_ENUM = 'callback'
UPDATE_ENUM = 'update'
# 泛在服务平台TOPIC
##接收
# 服务调用
INVOCATION_SERVICE_EXECUTE_TOPIC = ''
# 服务调用回调消息
INVOCATION_SERVICE_CALLBACK_TOPIC = ''
# 服务更新回调消息
UPDATE_SERVICE_CALLBACK_TOPIC = ''
# 更新服务topic
UPDATE_SERVICE_TOPIC = ''

## 上报
# 事件触发topic
ON_EVENT_TOPIC = ''
# 情境上报topic
UPLOAD_CONTEXT_TOPIC = ''
# 服务列表上报topic
UPLOAD_SERVICE_LIST_TOPIC = ''
# 设备硬件信息上报
UPLOAD_HARDWARE_TOPIC = ''

# mqtt服务器相关配置
MQTT_ADDRESS="116.204.102.248"
MQTT_PORT=1883

# 基础路径
BASE_PATH="/"
SERVICE_PATH = "/service"
SERVICE_RELATIVE_PATH = "service"
PROXY_PATH = "/proxy"


# url相关
BASE_URL = "http://192.168.0.103:8084"

# 初试化TOPIC
def initTopic(deviceId:str):
  global DEVICE_ID
  DEVICE_ID = deviceId
  global INVOCATION_SERVICE_EXECUTE_TOPIC
  INVOCATION_SERVICE_EXECUTE_TOPIC='/client/invocation/%s/+/+'%(DEVICE_ID)
  global INVOCATION_SERVICE_CALLBACK_TOPIC
  INVOCATION_SERVICE_CALLBACK_TOPIC = '/server/invocation/callback/%s/${service}/${capability}/${msgid}'%(DEVICE_ID)
  global UPDATE_SERVICE_CALLBACK_TOPIC
  UPDATE_SERVICE_CALLBACK_TOPIC = '/server/update/callback/${service}/${capability}/${msgid}'
  global UPDATE_SERVICE_TOPIC
  UPDATE_SERVICE_TOPIC='/client/%s/%s/+'%(UPDATE_ENUM,DEVICE_ID)

  global ON_EVENT_TOPIC
  ON_EVENT_TOPIC='/server/event/%s'%(DEVICE_ID)
  global UPLOAD_CONTEXT_TOPIC
  UPLOAD_CONTEXT_TOPIC='/server/context/%s'%(DEVICE_ID)
  global UPLOAD_SERVICE_LIST_TOPIC
  UPLOAD_SERVICE_LIST_TOPIC = '/server/deviceInfo/%s'%(DEVICE_ID)
  global UPLOAD_HARDWARE_TOPIC
  UPLOAD_HARDWARE_TOPIC = '/server/deviceHardwareInfo/%s'%(DEVICE_ID)
  

# 初始化路径信息 
def initPath(basePath:str,servicePath:str,proxyPath:str):
    global BASE_PATH
    BASE_PATH = basePath
    global SERVICE_RELATIVE_PATH
    SERVICE_RELATIVE_PATH = servicePath
    global SERVICE_PATH
    SERVICE_PATH =  PathUtil.joinPath(basePath,servicePath)
    global PROXY_PATH
    PROXY_PATH = PathUtil.joinPath(basePath,proxyPath)
    
