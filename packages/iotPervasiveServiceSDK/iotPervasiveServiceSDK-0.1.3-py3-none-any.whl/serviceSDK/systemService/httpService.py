

#web服务
webserver = None


# web服务器初始化
def webServerInit():
  from ..router import httpRouter
  httpRouter.runWebServer()


