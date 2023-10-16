import os
import sys
from ...utils import logutil as logUtil
import importlib
from ...utils import pathUtils as PathUtil
# import importlib.util

log = logUtil.get_logger(__name__)
'''
代理加载工具
''' 
class ProxyLoader:
  """
  * 读取模块字典
  * modelPath   model所在路径,相对于src目录
  """
  def loadProxyDict(proxyDirPath,BASE_PATH): 
    proxyDict = {}
    absolutePath=proxyDirPath
    proxyList = []
    try:
      proxyList = os.listdir(absolutePath)
    except Exception as e:
      log.warning("代理文件夹不存在"+absolutePath)
      return {}
    for proxyName in proxyList:
      try:
        if proxyName.find(".py")>0:
          module_path = PathUtil.joinPath(proxyDirPath, proxyName)
          log.debug(module_path)
          proxyDict = ProxyLoader.load_proxy_dict(module_path,proxyDict)
      except Exception as e:
        log.error(proxyDirPath+"  "+proxyName+"代理加载失败"+str(e))
    print("Load ModelDict Success")
    return proxyDict


  def load_proxy_dict(file_path,proxyDict:dict):
    try:
        file_name = os.path.basename(file_path)
        file_name = os.path.splitext(file_name)[0]
        spec = importlib.util.spec_from_file_location(file_name, file_path)

        module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(module)

        proxyDict[file_name] = module

    except Exception as e:
      log.error(f"加载代理 {file_path} 失败: {str(e)}")

    return proxyDict




