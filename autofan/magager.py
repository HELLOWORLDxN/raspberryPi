import fan.py
import collections
class ALG():
    def __init__(self,dataSource):
        self.data=dataSource
    @property
    def data():
        return self.__data
    @data.setter
    def data(self,value):
        if isinstance(value,TempData):
            self.__data=TempData
        else:
            raise AttributeException('object of calss <ALG>:function <data.setter> need type <TempData> given %' %type(alg)
    def setDataSource(self,dataSource):
        self.data=dataSource
    
    def caculate(self,traceCount,traceStep):
        pass

class FanManager():
    def __init__(self,fan=None,*,alg=ALG):
        self.fan=fan
        self.deltaBase=deltaBase

    def setALG(self,alg):
        if isinstance(alg,ALG):
            self.__alg=alg
        else:
            raise AttributeException('object of calss <FanManager>:function <setALG> need type <ALG> given %' %type(alg)

    @property
    def fan(self):
        return self.__fan
    @fan.setter
    def fan(self,fan=None):
        if isinstance(fan,Fan) or fan==None:
            self.__fan=fan
        else:
            raise AttributeException('object of calss <FanManager>:function <setFan> need type <Fan> given %' %type(fan)
        
    def autoSpeed():
        rate=self.alg.caculate()
        self.fan.offsetSpeed(rate)
