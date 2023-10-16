
# 事件Bean

class EventBean:
  
  #事件id
  eventId = None
  
  # 参数
  attributes = {}
  
  # 推送类型
  protocolType = None 
  
  # 输入模板
  messageMapper = None
  
  # 输出模板的语言
  messageLanguage = None

  
  def __init__(self) -> None:
    self.capabilityBeanDict = {}
    
  def __str__(self):
    return f"EventBean(EventId={self.eventId}, protocolType={self.protocolType}, attributes={self.attributes}, messageMapper={self.messageMapper}, messageLanguage={self.messageLanguage})"

