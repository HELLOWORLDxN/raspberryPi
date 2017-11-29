import threading,collections
import time,functools,abc
import classTools,runStruct
class Temp():
    def __init__(self,temp,logTime):
        self.__temp=temp
        self.__logTime=logTime
    @property
    def logTime(self):
        return self.__logTime
    @property
    def temp(self):
        return self.__temp

@classTools.Singleton
class TempData(collections.deque,runStruct.LoopInside):
    def __init__(self,*args,**dwgs):
        collections.deque.__init__(self,*args,**dwgs)
        runStruct.LoopInside.__init__(self)
        self.__lock=threading.RLock()
    @property
    def safeLock(self):
        return self.__lock
    def safeAppend(self,value):
        with self.__lock:
            self.append(value)
    def safePeek(self,index):
        with self.__lock:
            return self[index]
    def update(self):
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            temp=f.read().strip()
            if temp.isdigit():
                temp=int(temp)
            else:
                raise Exception('file:/sys/class/thermal/thermal_zone0/temp string is not digit')
            self.safeAppend(Temp(temp * 10**-3,time.time()))
    def keepingUpdate(self,sleepTime=1):
        if self.loop.isStarted:
            raise Exception('TempData is updateing dont call keepingUpdate again')
        self.loop.sleepTime=sleepTime
        self.loop.funcAppend(self.update)
        self.loop.start()
        return self.loop

if __name__=='__main__' :
    tpData=TempData()
    tpData.x=1
    print(tpData.x)
    print(id(tpData))
    tpData=TempData()
    print(tpData.x)
    print(id(tpData))
    tpData.keepingUpdate()
    
