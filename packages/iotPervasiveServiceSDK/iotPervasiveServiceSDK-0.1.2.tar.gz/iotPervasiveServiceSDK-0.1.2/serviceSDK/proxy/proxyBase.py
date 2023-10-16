# 代理类型的基类
class ProxyBase:
  operation = None
  def __init__(self,initData):
    print("编写代理类时需要重写代理类型的__init__方法")
  
  def handle(self,request)->dict:
    print("编写代理类时需要重写代理类型的handle方法")