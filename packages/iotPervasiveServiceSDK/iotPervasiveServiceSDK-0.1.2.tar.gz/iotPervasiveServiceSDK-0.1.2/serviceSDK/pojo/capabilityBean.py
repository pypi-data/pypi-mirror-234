
# 能力bean

class CapabilityBean:
  # 能力id
  capabilityId = None
  # 代理类型
  proxyType = None
  # 参数
  attributes = {}
  # 输入模板的语言
  inputLanguage = None
  # 输入模板
  inputMapper = None
  # 输出模板的语言
  outputLanguage = None
  # 输出模板
  outputMapper = None

  # 定义__str__方法，返回所有属性和值的字符串表示
  def __init__(self) -> None:
    self.attributes = {}

  def __str__(self):
    return f"CapabilityBean(capabilityId={self.capabilityId}, proxyType={self.proxyType}, attributes={self.attributes}, inputLanguage={self.inputLanguage}, inputMapper={self.inputMapper}, outputLanguage={self.outputLanguage}, outPutMapper={self.outputMapper})"
