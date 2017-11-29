import threading,time
import classTools
@classTools.threadSafe
class Loop(threading.Thread):
    def __init__(self,func=None,sleepTime=3):
        super(Loop,self).__init__()
        self.__funcList=[]
        if func:
            self.funcAppend(func)
        self.__sleepTime=sleepTime
        self.__resumeEvt=threading.Event()
        self.__resumeEvt.set()
        self.__runningFlg=True
        self.__isStarted=False
    @property
    def isStarted(self):
        return self.__isStarted
    def run(self):
        while self.__runningFlg:
            for f in self.__funcList:
                f()
            self.__resumeEvt.wait()
            time.sleep(self.sleepTime)
    @property
    def sleepTime(self):
        return self.__sleepTime
    @sleepTime.setter
    def sleepTime(self,value):
        assert isinstance(value,(int,float))
        self.__sleepTime=value
    def funcAppend(self,func):
        assert callable(func)
        self.__funcList.append(func)
    def funcPop(self,func):
        if func in self.__funcList:
            self.remove(func)
    def start(self):
        self.__isStarted=True
        super(Loop,self).start()
    def pause(self):
        self.__resumeEvt.clear()
    def resume(self):
        self.__resumeEvt.set()
    def stop(self):
        self.resume()
        self.__runningFlg=False

class LoopInside():
    def __init__(self):
        self.__loop=Loop()
    @property
    def loop(self):
        return self.__loop

if __name__=='__main__':
    def test():
        print(1)
    mThReEv=threading.Event()
    def loopOp(event,loop=None):
        char=event.char.upper()
        print(char)
        if char=='N':
            print('main loop resume')
            mThReEv.set()
            print('loop start')
            loop.start()
            print('loop start after')
        elif char=='P':
            loop.pause()
        elif char=='R':
            loop.resume()
        elif char=='S':
            loop.stop()

    import tkinter,functools
    tk=tkinter.Tk()
    entry=tkinter.Entry(tk)
    loop=Loop(test,1)
    entry.bind('<Key>',functools.partial(loopOp,loop=loop))
    entry.pack()
    tk.mainloop()
    print('tk start')
    mThReEv.wait()
    loop.join()
    print('after join')
