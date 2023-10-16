import os

'''
路径拼接 
'''
def joinPath(path1:str, path2:str):
  return os.path.normpath(os.path.join(path1, path2))