import gc
import os
import time
import tarfile

class TarGzUtils:
    def __init__(self, filePath):
        # 检查文件名是否以.tar.gz结尾
        if not filePath.endswith(".tar.gz"):
            raise ValueError("Invalid filename: {}".format(filePath))
        self.filePath = filePath
    
    def extractToDir(self, dirPath):
        try:
            with tarfile.open(self.filePath, "r:gz") as tar:
                tar.extractall(path=dirPath)
        except tarfile.TarError as e:
            raise Exception("解压异常 {}: {}".format(self.filePath, str(e)))
        pass
    
    def extractAndDeleteToDir(self, dir):
        try :
            # 解压并删除.tar.gz文件到指定目录
            self.extractToDir(dir)
        finally :
            # 删除原始文件
            os.remove(self.filePath) 
