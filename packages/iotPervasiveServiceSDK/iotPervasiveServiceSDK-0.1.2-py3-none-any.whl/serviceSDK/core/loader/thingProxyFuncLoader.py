
readFunc = None
writerFunc = None

def setFunc(thingModelClass):
    global readFunc
    global writerFunc
    readFunc = thingModelClass.readThingModel
    writerFunc = thingModelClass.setThingModel
