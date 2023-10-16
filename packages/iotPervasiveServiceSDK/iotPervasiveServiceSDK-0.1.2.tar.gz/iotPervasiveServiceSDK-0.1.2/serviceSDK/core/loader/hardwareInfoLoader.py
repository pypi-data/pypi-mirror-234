from ...utils import logutil

log = logutil.get_logger(__name__)

class HardwareInfoLoader:

  
  def __init__(self):
    # 存储用户提供的静态硬件信息
    self.staticHardwareData = {}
    # 存储获取实时硬件信息的回调函数
    self.dynamicHardwareCallbacks = {}  

  """
  设置静态硬件信息。

  参数:
      dataDict (dict): 包含用户自定义静态硬件信息的字典。
  """
  def setStaticHardwareData(self, dataDict):
    self.staticHardwareData = dataDict  


  """
  注册获取实时硬件信息的回调函数。

  参数:
      key (str): 用户定义的硬件信息的键（key）。
      callbackFunc (function): 回调函数，用于获取实时硬件信息。
  """
  def registerDynamicHardwareCallback(self, key, callbackFunc):
    self.dynamicHardwareCallbacks[key] = callbackFunc

  """
  获取用户定义的硬件信息。

  返回:
      dict: 包含用户定义的硬件信息。
  """
  def getHardwareInfo(self):

    hardwareInfo = self.staticHardwareData.copy()

    # 获取实时硬件信息
    for key, callback in self.dynamicHardwareCallbacks.items():
      try:
        hardwareInfo[key] = callback()
      except Exception as e:
        log.error("动态获取硬件信息异常，请检查HardwareInfo回调"+key+":"+str(e))

    return hardwareInfo