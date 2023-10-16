import requests
import os
from .. import config
from ..core.loader.serversLoader import ServiceLoader
from ..core import applicationContext
from ..pojo import serviceBean
from ..utils import fileUtils
import sys
from ..utils.tarGzUtils import TarGzUtils
from ..utils import logutil
from ..core import applicationContext
from ..core.exception.serviceException import ServiceNotExistException
from ..utils import pathUtils as PathUtil

SERVICE_TARGZ_FILE_NAME = "serviceImpl.tar.gz"

log = logutil.get_logger(__name__)
'''
泛在服务平台服务管理
'''

'''
删除指定服务
'''
def deleteService(id:str)->bool:
    
    # 获取服务信息    
    service:serviceBean = applicationContext.serviceDict.get(id,None)
    # 服务不存在则 
    if (service == None):
        return True
    # 服务路径拼接    
    servicePath =  PathUtil.joinPath(config.BASE_PATH,get_service_path(config.SERVICE_PATH,service.filePath))
    # 删除服务    
    fileUtils.removePath(servicePath)
    # 重新加载服务列表    
    applicationContext.serviceDict=ServiceLoader.LoadServiceDict(config.SERVICE_RELATIVE_PATH,config.BASE_PATH)
    # 检查是否删除
    service:serviceBean = applicationContext.serviceDict.get(id,None)
    if (service == None):
        return True
    else:
        return False





'''
* 增加/更新服务
'''
def updateService(id:str):
    downloadService(id)
    applicationContext.serviceDict=ServiceLoader.LoadServiceDict(config.SERVICE_RELATIVE_PATH,config.BASE_PATH)
    



'''
* 服务下载
'''
def downloadService(id:str):
    # 获取服务文件信息
    try :
        getUrl = config.BASE_URL+"/serviceImpl/"+id+"/getFolderPath"
        log.info(getUrl)
        res = requests.get(getUrl)
    except Exception as e:
        raise Exception('rest get serviceImplInfo error ')
    if(res.status_code!=200):
        raise Exception('rest get error,status_code = '+ str(res.status_code))
    serviceFilePath = res.json()["data"]
    log.info(serviceFilePath)
    # 拼接服务路径   判断服务是否存在 存在则采用原路径
    existingService = applicationContext.serviceDict.get(id.split("::")[0],None)
    if existingService!=None:
        deleteService(id.split("::")[0])
    servicePath = PathUtil.joinPath(config.SERVICE_PATH,"service"+''.join([('0'+hex(ord(os.urandom(1)))[2:])[-2:] for x in range(8)]))
    log.info("servicePath"+servicePath)
    serviceTargzPath =  PathUtil.joinPath(servicePath,SERVICE_TARGZ_FILE_NAME)
    # 下载压缩包    
    downloadServiceFile(serviceFilePath,serviceTargzPath)
    # 解压文件
    tarFile = TarGzUtils(serviceTargzPath) 
    try:
        tarFile.extractAndDeleteToDir(servicePath)
    except Exception as e:
        log.error(str(e))
    
    
'''
 下载服务文件
'''
def downloadServiceFile(filePath:str,servicePath:str):
    downloadUrl=config.BASE_URL+"/file/folder?urlPath="+filePath+"&type=tar.gz"
    log.info("url:"+downloadUrl)
    log.info("service:"+servicePath)
    try:
        fileUtils.downloadFile(downloadUrl,servicePath)
    except Exception as e:
        raise Exception('下载时出现异常: url:'+downloadUrl+",filePath:"+servicePath+ "err:" +str(e))


def get_service_path(base_path, config_path):
    base_dir = os.path.basename(base_path)
    rel_path = os.path.relpath(config_path, base_path)
    service_path = os.path.join(base_dir, rel_path.split(os.sep)[0])
    return service_path


