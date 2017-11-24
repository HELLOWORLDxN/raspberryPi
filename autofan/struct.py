import threading
class Loop(threading.Thread):
    def __init__(self):
        self.__funcList=None
        self.__resumeEvt=threading.Event()
        self.__resumeEvt.set()
        self.__runningFlg=True
    @property
    def sleepTime(self):
        pass
    def funcAppend(self,func):
        pass
    def funcPop(self,func,index=None):
        pass
    def pause(self)::
        self.__resumeEvt.clear()
    def resume(self):
        self.__resumeEvt.set()
    def stop(self):
        self.resume()
        self.__stop
