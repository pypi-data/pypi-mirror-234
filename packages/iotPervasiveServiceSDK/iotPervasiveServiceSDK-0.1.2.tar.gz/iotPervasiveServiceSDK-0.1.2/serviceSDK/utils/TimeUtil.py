import time

# 同步并获取时间戳 （毫秒）
def getTimerMs():
  return getTimerS()*1000

# 同步并获取时间戳 （秒）
def getTimerS():
  return int(time.time())



