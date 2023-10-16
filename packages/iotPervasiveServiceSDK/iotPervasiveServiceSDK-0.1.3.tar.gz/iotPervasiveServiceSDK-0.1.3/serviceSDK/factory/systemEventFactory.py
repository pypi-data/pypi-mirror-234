from ..pojo.eventBean import EventBean

'''
* 创建一个系统事件
*
'''
def createSystemEvent(eventId:str,topic:str)->EventBean:
    event = EventBean()
    event.eventId = eventId
    event.attributes = {         
                    "host":"",
                    "topic":topic,
                    "username":"",
                    "password":""}
    return event
    