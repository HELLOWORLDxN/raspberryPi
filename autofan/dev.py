import RPi.GPIO as GPIO
class Fan():
    def __init__(self,footID,freq=100)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(footID,GPIO.OUT)
        self.__pwm=GPIO.PWM(footID,freq)
        self.__pwm.start(0)
        self.__speed=Speed()
    
    @property
    def speed(self):
        return self.__speed.value
    @speed.setter:
    def speed(self,value):
        self.speed.value=value
        self.__pwm.ChangeDutyCycle(self.speed.value)
    
    def offsetSpeed(self,fact):
        self.speed+=fact

    def __del__(self):

class Speed():
    def __init__(self,speed=0):
        self.value=speed

    @property
    def value(self):
        if hassattr(self,'__speed'):
            return self.__speed
        else:
            return None
    @value.setter
    def value(self,value):
        if isinstance(value,int) and (value <0 or value>100):
            self.__speed=value
        else:
            raise AttributeException('reference of class <Speed> : function <speed.setter> need Attribute int given %s' %str(type(value)))

    def add(self,fact=1):
        if self.value = None:
            self.value=0
        self.speed+=fact
        if self.value>100:
            self.value=100
        return self.value

    def reduce(self,fact=1):
        if self.value = None:
            self.value=0
        self.value-=fact
        if self.value<0:
            self.value=0
        return self.value
