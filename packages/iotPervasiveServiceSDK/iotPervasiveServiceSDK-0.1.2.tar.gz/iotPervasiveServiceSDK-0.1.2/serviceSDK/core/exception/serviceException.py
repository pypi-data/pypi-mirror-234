class ServiceException(Exception):
    def __init__(self, msg):
        self.message = f"service exception: {msg}"
        super().__init__(self.message)


    def __str__(self):
        return repr(self.message)


# 加载服务时异常
class LoadingServiceException(ServiceException):
    def __init__(self, msg):
        self.message = f"An error occurred loading the service: {msg}"
        super().__init__(self.message)
    def __str__(self):
        return repr(self.message)
 

# 调用服务时异常
class InvokeServiceException(ServiceException):
    def __init__(self, msg):
        self.message = f"Invoke Service Exception: {msg}"
        super().__init__(self.message)
    
    def __str__(self):
        return repr(self.message)


# 没有找到路径异常
class LoadPathNotfoundException(LoadingServiceException):
    def __init__(self, path):
        self.message = f"The path '{path}' does not exist"
        super().__init__(self.message)

    def __str__(self):
        return repr(self.message)
    
# 服务不存在异常  
class ServiceNotExistException(InvokeServiceException):
    def __init__(self, serviceId):
        self.message = f"There is no service with serviceId = {serviceId}"
        super().__init__(self.message)

    def __str__(self):
        return repr(self.message)
    
    
# 能力不存在异常  
class CapabilityNotExistException(InvokeServiceException):
    def __init__(self, capabilityId,serviceId):
        self.message = f"There is no capability with capabilityId = {capabilityId},serviceId = {serviceId}"
        super().__init__(self.message)

    def __str__(self):
        return repr(self.message)

# 事件不存在异常  
class EventNotExistException(InvokeServiceException):
    def __init__(self, eventId,serviceId):
        self.message = f"There is no event with eventId = {eventId},serviceId = {serviceId}"
        super().__init__(self.message)

    def __str__(self):
        return repr(self.message)

# 代理不存在异常  
class ProxyNotExistException(InvokeServiceException):
    def __init__(self, proxy):
        self.message = f"There is no proxy with  proxy = {proxy}"
        super().__init__(self.message)

    def __str__(self):
        return repr(self.message)

