# from machine import Timer

# 最小间隔时间
MIN_INTERVAL_TIME = 50
import sched
import threading
import time
from ..utils import logutil

log = logutil.get_logger(__name__)
'''
任务基类，所有定时任务都需要继承此类
==注意== 此类所有时间单位均为ms ; 1s = 1000ms
'''
class ScheduleBase:
  #下次执行时间
  nextRunTime = 0
  #间隔时间
  intervalTime = 1000

  log = None

  def __init__(self,intervalTime=1000) -> None:
    self.intervalTime =intervalTime<50 and 50 or intervalTime
    self.log = logutil.get_logger(__name__)

  def setIntervalTime(self,intervalTime):
    self.intervalTime=intervalTime

  def tryHandleInterrupt(self):
    try:
      self.handleInterrupt()
    except Exception as e:
      log.error(str(e))


  def handleInterrupt(self):
    print("please rewrite the handleInterrupt")

'''
定时任务类
'''
class ScheduleService:
  tasks = []
  divisor = 1000
  scheduler = None
  task = None


  def __init__(self,tasks):
    self.tasks = tasks

    # 创建调度器
    self.scheduler = sched.scheduler(time.time, time.sleep)
    task = threading.Thread(target=self.task_thread)
    task.start()

    # #intervalTime使用最大公约数来决定轮巡间隔
    # intervalTime = len(tasks)>0 and tasks[0].intervalTime or 1
    # for task in tasks:
    #   intervalTime = gcd(task.intervalTime,intervalTime)
    # # 限幅  如果执行的间隔时间小于50毫秒则等于50毫秒
    # self.intervalTime =intervalTime<50 and 50 or intervalTime
    # print("ScheduleService Init Success intervalTime")


  # def handleInterrupt(self,timer):
  #   for task in self.tasks:
  #     task.nextRunTime = task.nextRunTime - self.intervalTime
  #     if(task.nextRunTime<=0):
  #       task.handleInterrupt()
  #       task.nextRunTime = task.intervalTime

  def handleInterrupt(self,schedule:ScheduleBase):
    schedule.tryHandleInterrupt()

    self.scheduler.enter(schedule.intervalTime/self.divisor, 1, self.handleInterrupt, (schedule,))

  
  # 创建并启动线程
  def task_thread(self):
      # 开始执行任务  
      for task in self.tasks:
        self.scheduler.enter(3, 1, self.handleInterrupt, (task,))
      self.scheduler.run()




