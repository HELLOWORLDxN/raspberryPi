import threading
import time,functools
import classTools,struct
@ClassTools.Singleton
class TempData(collections.deque):
    def __init__(self,*args,**dwgs):
        super().__init__(self,*args,**dwgs)
        self.__lock=threading.Lock()
        self.__lastUpdateAt=None
        self.__loop=struct.Loop()
    @property
    def loop(self):
        return self.__loop
    @property
    def safeLock(self):
        return self.__lock
    def safeAppend(self,value):
        with self.__lock:
            self.append(value)
    def safePeek(self,index):
        with self.__lock:
            return self[index]
    @perproty
    def lastUpdateAt(self):
        return self.__lastUpdateAt
    def update(self):
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            temp=f.read()
            if temp.isdigit():
                temp=int(temp)
            else:
                raise Exception('file:/sys/class/thermal/thermal_zone0/temp string is not digit')
            self.safeAppend(temp * 100**-3)
    def keepingUpdate(self):
        self.loop.funcAppend(self.update)
        self.loop.start()
        return self.loop
