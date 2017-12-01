import dev,runStruct
import collections,time,math
from tempData import TempData
class ALG():
    def __init__(self,dataSource):
        self.__data=dataSource
        self.__lastCaculateTime=0
    @property
    def data():
        return self.__data
    @data.setter
    def data(self,value):
        if isinstance(value,TempData):
            self.__data=TempData
        else:
            raise AttributeException('object of calss <ALG>:function <data.setter> need type <TempData> given %' %type(alg))
    def caculate(self,traceDur=5,traceDeep=(3,-1),precision=0.001,nagtiveDebuff=0.7):
        if traceDeep[1]>=0 and traceDeep[1]<traceDeep[0]:
            traceDeep=(traceDeep[0],traceDeep[1])
        curTimeStamp=time.time()
        data=[] #temp/s
        doCal=False
        preTime=None
        preTemp=None
        i=-1
        lenData=len(self.__data)
        if lenData>0:
            while self.__lastCaculateTime<self.__data[i].logTime:
                if curTimeStamp-self.__data[i].logTime>=traceDur:
                    doCal=True
                    break
                temp=self.__data[i]
                if preTime and preTemp:
                    data.insert(0,(preTemp-temp.temp)/(preTime-temp.logTime))
                preTime,preTemp=temp.logTime,temp.temp
                i-=1
                if abs(i)>lenData or (traceDeep[1]>=0 and traceDeep[1]<abs(i)):
                    break
        if len(data)>=traceDeep[0]:
            self.__lastCaculateTime=curTimeStamp
            avg=sum(data)/len(data)
            ret=math.atan(avg)/(math.pi/2)
            if abs(ret)<precision:
                return 0
            if ret>=0:
                return ret
            else:
                return ret*nagtiveDebuff
        else:
            return 0
        
        

class FanManager(runStruct.LoopInside):
    def __init__(self,fan=None,*,bootTemp=50,pwOffTemp=45,ceilTemp=80,bootSpeed=50,sens=30,alg=ALG(TempData(50))):
        super().__init__()
        self.fan=fan
        self.__alg=alg
        self.__bootTemp=bootTemp
        self.__pwOffTemp=pwOffTemp
        self.__ceilTemp=ceilTemp
        self.__bootSpeed=bootSpeed
        self.__sens=sens
    @property
    def ceilTemp(self):
        return self.__ceilTemp
    @ceilTemp.setter
    def ceilTemp(self,value):
        if not isinstance(value,(int,float)):
            raise Exception('function ceilTemp need one argument as <int> or <float>')
        self.__ceilTemp=value
    @property
    def bootSpeed(self):
        return self.__bootSpeed
    @bootSpeed.setter
    def bootSpeed(self,value):
        if not isinstance(value,(int,float)):
            raise Exception('function bootSpeed need one argument as <int> or <float>')
        self.__bootSpeed=value
    @property
    def alg(self):
        return self.__alg
    @alg.setter
    def alg(self,alg):
        if isinstance(alg,ALG):
            self.__alg=alg
        else:
            raise AttributeException('object of calss <FanManager>:function <setALG> need type <ALG> given %' %type(alg))
    @property
    def sens(self):
        return self.__sens
    @sens.setter
    def sens(self,value):
        assert isinstance(value,(int,float))
        self.__sens=value
    @property
    def bootTemp(self):
        return self.__bootTemp
    @bootTemp.setter
    def bootTemp(self,value):
        assert isinstance(value,(int,float))
        self.__bootTemp=value
    @property
    def pwOffTemp(self):
        return self.__pwOffTemp
    @pwOffTemp.setter
    def pwOffTemp(self,value):
        assert isinstance(value,(int,float))
        self.__pwOffTemp=value
    @property
    def fan(self):
        return self.__fan
    @fan.setter
    def fan(self,fan=None):
        if isinstance(fan,dev.Fan) or fan==None:
            self.__fan=fan
        else:
            raise AttributeException('object of calss <FanManager>:function <setFan> need type <Fan> given %' %type(fan))
    def speedCaculate(self):
        tempData=TempData()
        if tempData:
            lastTemp=tempData[-1].temp
            if self.bootTemp<lastTemp:
                if self.fan.speed<self.bootSpeed:
                    self.fan.speed=self.bootSpeed
                else:
                    offset=self.alg.caculate()*self.__sens
                    self.fan.offsetSpeed(offset)
                if lastTemp>self.ceilTemp:
                    self.fan.speed=100
            if self.pwOffTemp>lastTemp:
                self.fan.speed=0

    def autoSpeed(self,interval=3):
        if self.loop.isStarted:
            raise Exception('TempData is updateing dont call keepingUpdate again')
        self.loop.sleepTime=interval
        self.loop.funcAppend(self.speedCaculate)
        self.loop.start()

    def __delete__(self):
        del self.__fan
    
if __name__=='__main__':
    def testALG():
        tempData=TempData()
        alg=ALG(tempData)
        def printCal():
            print(alg.caculate())
        tempData.loop.funcAppend(printCal)
        tempData.keepingUpdate()
    def testManager():
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BOARD)
        fan=dev.Fan(11)
        fM=FanManager(fan,bootTemp=30,pwOffTemp=25)
        fM.autoSpeed()
        tempData=TempData()
        tempData.keepingUpdate()

    testManager()

