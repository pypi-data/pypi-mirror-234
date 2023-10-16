
#字典深拷贝 注意字典中不能有Object
def dictCopy(oldDict):
  newDick = {}
  list = oldDict.items()
  for k,v in list:
    if isinstance(v,dict):
      newDick[k] = dictCopy(v)
    else:
      newDick[k] = v 
  return newDick