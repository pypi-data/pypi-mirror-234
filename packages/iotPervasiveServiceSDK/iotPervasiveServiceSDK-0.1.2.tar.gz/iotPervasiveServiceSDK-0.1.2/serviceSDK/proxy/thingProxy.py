from serviceSDK.core.loader import thingProxyFuncLoader
import json


'''
物模型属性读写代理
'''
class thingProxy():
  
  initdata = None
  def __init__(self,initdata) -> None:
    self.initdata = initdata
    pass

  def handle(self,request):
    if(self.initdata["operation"]=="read"):
      return thingProxyFuncLoader.readFunc()
    elif(self.initdata["operation"]=="writer"):
      request=json.loads(request)
      return thingProxyFuncLoader.writerFunc(request)
    else:
      raise Exception("no operation is"+ self.initdata["operation"])