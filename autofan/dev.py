import RPi.GPIO as GPIO
import logging
logging.basicConfig(level=logging.ERROR) 
logging.debug(GPIO.getmode())
if GPIO.getmode()==GPIO.BCM:
    raise Exception('GPIO mode shoule be GPIO.BOARD or None')
class Fan():
    def __init__(self,footID,freq=50):
        logging.debug(GPIO.getmode())
        GPIO.setup(footID,GPIO.OUT)
        self.__footID=footID
        self.__freq=freq
        self.__pwm=GPIO.PWM(footID,freq)
        self.__pwm.start(0)
        self.__speed=Speed()
    @property
    def freq(self):
        return self.__freq
    @freq.setter
    def freq(self,value):
        if isinstance(value,(int,float)) and value >0:
            self.__freq=value
            self.__pwm.ChangeFrequency(value)
        else:
            raise Exception('freq require a <int> or <float> value')
    @property
    def speed(self):
        return self.__speed.value
    @speed.setter
    def speed(self,value):
        self.__speed.value=value
        self.__pwm.ChangeDutyCycle(self.speed)
    
    def offsetSpeed(self,fact):
        self.speed+=fact

    def __delete__(self):
        logging.debug(GPIO.getmode())
        self.__pwm.stop()
        GPIO.cleanup(self.__footID)

class Speed():
    def __init__(self,speed=0):
        self.__speed=speed

    @property
    def value(self):
        return self.__speed
    @value.setter
    def value(self,value):
        logging.debug('+'+str(value)+'+')
        if isinstance(value,(int,float)) and (value >=0 or value<=100):
            self.__speed=value
        else:
            raise Exception('reference of class <Speed> : function <speed.setter> need Attribute int given %s' %str(type(value)))

    def add(self,fact=1):
        if self.value == None:
            self.value=0
        self.value+=fact
        if self.value>100:
            self.value=100
        return self.value

    def reduce(self,fact=1):
        if self.value == None:
            self.value=0
        self.value-=fact
        if self.value<0:
            self.value=0
        return self.value

if __name__=='__main__':
    speed=Speed()
    logging.debug(speed.value)
    assert speed.value==0
    speed.add()
    assert speed.value==1
    speed.add(2)
    assert speed.value==3
    speed.reduce(2)
    assert speed.value==1
    speed.reduce()
    assert speed.value==0

    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    fan=Fan(11)
    fan.offsetSpeed(50)
    input('running')
