from bottle import Bottle, run, request, template
from ..core.serverInvoker import CapabilityInvoker
import json
from ..utils import TimeUtil
import threading

app = Bottle()

@app.route('/client/invocation/<deviceId>/<serviceId>/<capabilityId>', method='POST')
# web局域网服务调用
def _httpHandlerInvokerPost(deviceId, serviceId, capabilityId):
    print("======rest server invoke======")
    msgJson = request.json.get("param","")
    runSuccess = False
    res = None
    try:
        res = CapabilityInvoker.invokeCapability(
            serviceId, capabilityId, msgJson
        )
        runSuccess = True
    except Exception as e:
        runSuccess = False
        res = e.__str__()
    # 拼接msg
    msgDict = {
        "success": runSuccess,
        "data": res,
        "timestamp": TimeUtil.getTimerMs(),
    }
    print(msgDict)
    return template(json.dumps(msgDict, ensure_ascii=False), name=__name__);

def _runServer():
    run(app, host='localhost', port=1024, debug=True)

def runWebServer():
        # 创建一个新线程来运行 Bottle 服务
    server_thread = threading.Thread(target=_runServer)
    server_thread.start()
    

