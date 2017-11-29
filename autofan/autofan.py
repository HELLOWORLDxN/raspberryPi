import RPi.GPIO as GPIO
import signal,os,sys
from manager import FanManager
from dev import Fan
from tempData import TempData
pid=os.getpid()
pidFPath=os.path.join(sys.path[0],'autofan.pid')
with open(pidFPath,'w') as f:
    f.write(str(pid))
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
TempData().keepingUpdate()
fan=Fan(11)
myManager=FanManager(fan)
myManager.autoSpeed()
def stopAll(*args):
    myManager.loop.stop()
    TempData().loop.stop()
signal.signal(signal.SIGINT,stopAll)
TempData().loop.join()
myManager.loop.join()
del myManager
GPIO.cleanup()
with open(pidFPath,'w') as f:
    f.write(str(pid))
