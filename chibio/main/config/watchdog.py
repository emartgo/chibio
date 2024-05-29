from .sys import sysItems
import time
from datetime import datetime
from threading import Thread
from .arduino import GPIO

def runWatchdog():  
    #Watchdog timing function which continually runs in a thread.
    global sysItems;
    if (sysItems['Watchdog']['ON']==1):
        #sysItems['Watchdog']['thread']
        toggleWatchdog();
        time.sleep(0.15)
        sysItems['Watchdog']['thread']=Thread(target = runWatchdog, args=())
        sysItems['Watchdog']['thread'].setDaemon(True)
        sysItems['Watchdog']['thread'].start();

def toggleWatchdog():
    #Toggle the watchdog
    global sysItems;
    GPIO.output(sysItems['Watchdog']['pin'], GPIO.HIGH)
    time.sleep(0.05)
    GPIO.output(sysItems['Watchdog']['pin'], GPIO.LOW)
    
GPIO.setup(sysItems['Watchdog']['pin'], GPIO.OUT)
print(str(datetime.now()) + ' Starting watchdog')
sysItems['Watchdog']['thread']=Thread(target = runWatchdog, args=())
sysItems['Watchdog']['thread'].setDaemon(True)
sysItems['Watchdog']['thread'].start(); 
GPIO.setup('P8_15', GPIO.OUT) #This output connects to the RESET pin on the I2C Multiplexer.
GPIO.output('P8_15', GPIO.HIGH)
GPIO.setup('P8_17', GPIO.OUT) #This output connects to D input of the D-Latch 
GPIO.output('P8_17', GPIO.HIGH)