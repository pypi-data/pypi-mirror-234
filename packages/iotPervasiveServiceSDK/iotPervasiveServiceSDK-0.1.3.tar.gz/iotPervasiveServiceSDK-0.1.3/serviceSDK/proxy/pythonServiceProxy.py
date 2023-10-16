from serviceSDK.proxy.proxyBase import ProxyBase 
import os
import importlib

'''
python服务代理
'''
class pythonServiceProxy(ProxyBase):
  script = None

  '''
  python服务代理初始化
  '''
  def __init__(self,initData) -> None:
    print("====pythonServiceProxy====")
    file_name = os.path.basename(initData["script"])
    file_name = os.path.splitext(file_name)[0]
    spec = importlib.util.spec_from_file_location(file_name, initData["script"])

    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    self.script = module
    


  def handle(self,request):
    return self.script.execute(request)
    