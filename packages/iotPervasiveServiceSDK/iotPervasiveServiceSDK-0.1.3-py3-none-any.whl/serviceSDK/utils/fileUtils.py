import requests
import os
import shutil
from ..utils import logutil

log = logutil.get_logger(__name__)

'''
 删除路径及其中文件
'''
def removePath(path:str):
    shutil.rmtree(path)
    
    
'''
 下载文件
 url:文件链接
 path:目标路径（包含文件名）
'''
def downloadFile(url:str,path:str):
    # 确认路径存在    
    fileFolderPath = os.path.dirname(path)
    
    # 删除已存在的文件     
    try:
        removePath(path)
    except:
        pass
    create_path(fileFolderPath)
    # 下载
    res = requests.get(url)
    with open(path,"wb") as code:
        code.write(res.content)

'''
  创建路径
'''
def create_path(path):
    try:
        os.makedirs(path, exist_ok=True)
        log.info(f"Path '{path}' created.")
    except OSError as error:
        log.error(f"creating path '{path}': {error}")