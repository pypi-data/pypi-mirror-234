

# 服务bean
class ServiceBean:
  # 服务实现的包名，不同版本保持一致
  url = None

  # 名称
  name = None

  # 版本
  versionCode = None

  # 能力 K:能力id   V: CapabilityBean
  capabilityBeanDict = {}
  
  # 事件 k:事件id  V: EventBean
  eventBeanDict = {}

  # 文件所在路径
  filePath = None
  
  def __init__(self) -> None:
    self.capabilityBeanDict = {}

  def __str__(self):
    capabilityStr = "{"
    for key, value in self.capabilityBeanDict.items():
      capabilityStr += "\n \t\t "+value.__str__()
    eventBeanStr = "{"
    for key, value in self.eventBeanDict.items():
      eventBeanStr += "\n \t\t "+value.__str__()
    return f"\nServiceBean(filePath={self.filePath},url={self.url}, name={self.name}, versionCode={self.versionCode}, \n \t capabilityBeanDict={capabilityStr} ,\n \t eventBeanDict = {eventBeanStr}) \n"
 