from threading import Thread, Lock
from datetime import datetime, date
from .arduino.mockgpio import *
from .sys import sysItems, sysData, sysDevices
from .watchdog import toggleWatchdog
from .controls import Thermostat, PumpModulation
import os
import random
import time
import math
import time

lock=Lock()
GPIO = MockGPIO()

def I2CCom(M,device,rw,hl,data1,data2,SMBUSFLAG):
    #Function used to manage I2C bus communications for ALL devices.
    M=str(M) #Turbidostat to write to
    device=str(device) #Name of device to be written to
    rw=int(rw) #1 if read, 0 if write
    hl=int(hl) #8 or 16
    SMBUSFLAG=int(SMBUSFLAG) # If this flag is set to 1 it means we are communuicating with an SMBUs device.
    data1=int(data1) #First data/register 
    if hl<20:
        data2=int(data2) #First data/register 
    global sysItems
    global sysData
    
    global sysDevices
    if(sysData[M]['present']==0): #Something stupid has happened in software if this is the case!
        print(str(datetime.now()) + ' Trying to communicate with absent device - bug in software!. Disabling hardware and software!')
        sysItems['Watchdog']['ON']=0 #Basically this will crash all the electronics and the software. 
        out=0
        tries=-1
        os._exit(4)
    
    #cID=str(M)+str(device)+'d'+str(data1)+'d'+str(data2)  # This is an ID string for the communication that we are trying to send - not used at present
    #Any time a thread gets to this point it will wait until the lock is free. Then, only one thread at a time will advance. 
    lock.acquire()

    #We now connect the multiplexer to the appropriate device to allow digital communications.
    tries=0
    while(tries!=-1):
        try:
            sysItems['Multiplexer']['device'].write8(int(0x00),int(sysItems['Multiplexer'][M],2)) #We have established connection to correct device. 
            check=(sysItems['Multiplexer']['device'].readRaw8()) #We check that the Multiplexer is indeed connected to the correct channel.
            if(check==int(sysItems['Multiplexer'][M],2)):
                tries=-1
            else:
                tries=tries+1
                time.sleep(0.02)
                print(str(datetime.now()) + ' Multiplexer didnt switch ' + str(tries) + " times on " + str(M))
        except: #If there is an error in the above.
            tries=tries+1
            time.sleep(0.02)
            print(str(datetime.now()) + ' Failed Multiplexer Comms ' + str(tries) + " times")
            if (tries>2):
                try:
                    sysItems['Multiplexer']['device'].write8(int(0x00),int(0x00)) #Disconnect multiplexer. 
                    print(str(datetime.now()) + 'Disconnected multiplexer on ' + str(M) + ', trying to connect again.')
                except:
                    print(str(datetime.now()) + 'Failed to recover multiplexer on device ' + str(M))
            if (tries==5 or tries==10 or tries==15):
                toggleWatchdog()  #Flip the watchdog pin to ensure it is working.
                GPIO.output('P8_15', GPIO.LOW) #Flip the Multiplexer RESET pin. Note this reset function works on Control Board V1.2 and later.
                time.sleep(0.1)
                GPIO.output('P8_15', GPIO.HIGH)
                time.sleep(0.1)
                print(str(datetime.now()) + 'Did multiplexer hard-reset on ' + str(M))
                
        if tries>20: #If it has failed a number of times then likely something is seriously wrong, so we crash the software.
            sysItems['Watchdog']['ON']=0 #Basically this will crash all the electronics and the software. 
            out=0
            print(str(datetime.now()) + 'Failed to communicate to Multiplexer 20 times. Disabling hardware and software!')
            tries=-1
            os._exit(4)
    
    time.sleep(0.0005)
    out=0;
    tries=0
    
    while(tries!=-1): #We now do appropriate read/write on the bus.
        try:
            if SMBUSFLAG==0:
                if rw==1:
                    if hl==8:
                        out=int(sysDevices[M][device]['device'].readU8(data1))
                    elif(hl==16):
                        out=int(sysDevices[M][device]['device'].readU16(data1,data2))
                else:
                    if hl==8:
                        sysDevices[M][device]['device'].write8(data1,data2)
                        out=1
                    elif(hl==16):
                        sysDevices[M][device]['device'].write16(data1,data2)
                        out=1
                    
            elif SMBUSFLAG==1:
                out=sysDevices[M][device]['device'].read_word_data(sysDevices[M][device]['address'],data1)
            tries=-1
        except: #If the above fails then we can try again (a limited number of times)
            tries=tries+1
            
            if (device!="ThermometerInternal"):
                print(str(datetime.now()) + ' Failed ' + str(device) + ' comms ' + str(tries) + " times on device " + str(M) )
                time.sleep(0.02)
            if (device=='AS7341'):
                print(str(datetime.now()) + ' Failed  AS7341 in I2CCom while trying to send ' + str(data1)  + " and " + str(data2))
                out=-1
                tries=-1

        if (tries>2 and device=="ThermometerInternal"): #We don't allow the internal thermometer to fail, since this is what we are using to see if devices are plugged in at all.
            out=0
            sysData[M]['present']=0
            tries=-1
        if tries>10: #In this case something else has gone wrong, so we panic.
            sysItems['Watchdog']['ON']=0 #Basically this will crash all the electronics and the software. 
            out=0
            sysData[M]['present']=0
            print(str(datetime.now()) + 'Failed to communicate to a device 10 times. Disabling hardware and software!')
            tries=-1
            os._exit(4)
                
    time.sleep(0.0005)
    
    try:
        sysItems['Multiplexer']['device'].write8(int(0x00),int(0x00)) #Disconnect multiplexer with each iteration. 
    except:
        print(str(datetime.now()) + 'Failed to disconnect multiplexer on device ' + str(M))


    
    lock.release() #Bus lock is released so next command can occur.
    
    return(out)

def setPWM(M,device,channels,fraction,ConsecutiveFails):
    #Sets up the PWM chip (either the one in the reactor or on the pump board)
    global sysItems
    global sysDevices
    
    if sysDevices[M][device]['startup']==0: #The following boots up the respective PWM device to the correct frequency. Potentially there is a bug here; if the device loses power after this code is run for the first time it may revert to default PWM frequency.
        I2CCom(M,device,0,8,0x00,0x10,0) #Turns off device. Also disables all-call functionality at bit 0 so it won't respond to address 0x70
        I2CCom(M,device,0,8,0x04,0xe6,0) #Sets SubADDR3 of the PWM chips to be 0x73 instead of 0x74 to avoid any potential collision with the multiplexer @ 0x74
        I2CCom(M,device,0,8,0xfe,sysDevices[M][device]['frequency'],0) #Sets frequency of PWM oscillator. 
        sysDevices[M][device]['startup']=1
    
    I2CCom(M,device,0,8,0x00,0x00,0) #Turns device on 
    
        
    
    timeOn=int(fraction*4095.99)
    I2CCom(M,device,0,8,channels['ONL'],0x00,0)
    I2CCom(M,device,0,8,channels['ONH'],0x00,0)
    
    OffVals=bin(timeOn)[2:].zfill(12)
    HighVals='0000' + OffVals[0:4]
    LowVals=OffVals[4:12]
    
    I2CCom(M,device,0,8,channels['OFFL'],int(LowVals,2),0)
    I2CCom(M,device,0,8,channels['OFFH'],int(HighVals,2),0)
    
    if (device=='Pumps'):
        I2CCom(M,device,0,8,channels['ONL'],0x00,0)
        I2CCom(M,device,0,8,channels['ONH'],0x00,0)
        I2CCom(M,device,0,8,channels['OFFL'],int(LowVals,2),0)
        I2CCom(M,device,0,8,channels['OFFH'],int(HighVals,2),0)
    else:
        CheckLow=I2CCom(M,device,1,8,channels['OFFL'],-1,0)
        CheckHigh=I2CCom(M,device,1,8,channels['OFFH'],-1,0)
        CheckLowON=I2CCom(M,device,1,8,channels['ONL'],-1,0)
        CheckHighON=I2CCom(M,device,1,8,channels['ONH'],-1,0)
    
        if(CheckLow!=(int(LowVals,2)) or CheckHigh!=(int(HighVals,2)) or CheckHighON!=int(0x00) or CheckLowON!=int(0x00)): #We check to make sure it has been set to appropriate values.
            ConsecutiveFails=ConsecutiveFails+1
            print(str(datetime.now()) + ' Failed transmission test on ' + str(device) + ' ' + str(ConsecutiveFails) + ' times consecutively on device '  + str(M) )
            if ConsecutiveFails>10:
                sysItems['Watchdog']['ON']=0 #Basically this will crash all the electronics and the software. 
                print(str(datetime.now()) + 'Failed to communicate to PWM 10 times. Disabling hardware and software!')
                os._exit(4)
            else:
                time.sleep(0.1)
                sysItems['FailCount']=sysItems['FailCount']+1
                setPWM(M,device,channels,fraction,ConsecutiveFails)
    
def addTerminal(M,strIn):
    #Responsible for adding a new line to the terminal in the UI.
    global sysData
    now=datetime.now()
    timeString=now.strftime("%Y-%m-%d %H:%M:%S ")
    sysData[M]['Terminal']['text']=timeString + ' - ' +  str(strIn) + '</br>' + sysData[M]['Terminal']['text']

def clearTerminal(M):
    #Deletes everything from the terminal.
    global sysData
    M=str(M)
    if (M=="0"):
        M=sysItems['UIDevice']
        
    sysData[M]['Terminal']['text']=''
    addTerminal(M,'Terminal Cleared')
    return ('', 204)

def scanDevices(which):
    #Scans to decide which devices are plugged in/on. Does this by trying to communicate with their internal thermometers (if this communication failes, software assumes device is not present)
    global sysData
    which=str(which)
    
    if which=="all":
        for M in ['M0','M1','M2','M3','M4','M5','M6','M7']:
            sysData[M]['present']=1
            I2CCom(M,'ThermometerInternal',1,16,0x05,0,0) #We arbitrarily poll the thermometer to see if anything is plugged in! 
            sysData[M]['DeviceID']=GetID(M)
    else: 
        
        sysData[which]['present']=1
        I2CCom(which,'ThermometerInternal',1,16,0x05,0,0)
        sysData[which]['DeviceID']=GetID(which)

    return ('', 204)

def changeDevice(M):
    #Function responsible for changin which device is selected in the UI.
    global sysData
    global sysItems
    M=str(M)
    if sysData[M]['present']==1:
        for Mb in ['M0','M1','M2','M3','M4','M5','M6','M7']:
            sysData[Mb]['UIDevice']=M
        
        sysItems['UIDevice']=M

    return ('', 204)

def GetID(M):
    #Gets the CHi.Bio reactor's ID, which is basically just the unique ID of the infrared thermometer.
    global sysData
    M=str(M)
    ID=''
    if sysData[M]['present']==1:
        pt1=str(I2CCom(M,'ThermometerIR',1,0,0x3C,0,1))
        pt2=str(I2CCom(M,'ThermometerIR',1,0,0x3D,0,1))
        pt3=str(I2CCom(M,'ThermometerIR',1,0,0x3E,0,1))
        pt4=str(I2CCom(M,'ThermometerIR',1,0,0x3F,0,1))
        ID = pt1+pt2+pt3+pt4
        
    return ID

def SetOutput(M,item):
    #Here we actually do the digital communications required to set a given output. This function is called by SetOutputOn above as required.
    global sysData
    global sysItems
    global sysDevices
    M=str(M)
    #We go through each different item and set it going as appropriate.
    if(item=='Stir'): 
        #Stirring is initiated at a high speed for a couple of seconds to prevent the stir motor from stalling (e.g. if it is started at an initial power of 0.3)
        if (sysData[M][item]['target']*float(sysData[M][item]['ON'])>0):
            setPWM(M,'PWM',sysItems[item],1.0*float(sysData[M][item]['ON']),0) # This line is to just get stirring started briefly.
            time.sleep(1.5)

            if (sysData[M][item]['target']>0.4 and sysData[M][item]['ON']==1):
                setPWM(M,'PWM',sysItems[item],0.5*float(sysData[M][item]['ON']),0) # This line is to just get stirring started briefly.
                time.sleep(0.75)
            
            if (sysData[M][item]['target']>0.8 and sysData[M][item]['ON']==1):
                setPWM(M,'PWM',sysItems[item],0.7*float(sysData[M][item]['ON']),0) # This line is to just get stirring started briefly.
                time.sleep(0.75)

        setPWM(M,'PWM',sysItems[item],sysData[M][item]['target']*float(sysData[M][item]['ON']),0)
        
        
    elif(item=='Heat'):
        setPWM(M,'PWM',sysItems[item],sysData[M][item]['target']*float(sysData[M][item]['ON']),0)
    elif(item=='UV'):
        setPWM(M,'PWM',sysItems[item],sysData[M][item]['target']*float(sysData[M][item]['ON']),0)
    elif (item=='Thermostat'):
        sysDevices[M][item]['thread']=Thread(target = Thermostat, args=(M,item))
        sysDevices[M][item]['thread'].setDaemon(True)
        sysDevices[M][item]['thread'].start();
        
    elif (item=='Pump1' or item=='Pump2' or item=='Pump3' or item=='Pump4'): 
        if (sysData[M][item]['target']==0):
            sysData[M][item]['ON']=0
        sysDevices[M][item]['thread']=Thread(target = PumpModulation, args=(M,item))
        
        sysDevices[M][item]['thread'].setDaemon(True)
        sysDevices[M][item]['thread'].start();

    elif (item=='OD'):
        SetOutputOn(M,'Pump1',0)
        SetOutputOn(M,'Pump2',0) #We turn pumps off when we switch OD state
    elif (item=='Zigzag'):
        sysData[M]['Zigzag']['target']=5.0
        sysData[M]['Zigzag']['SwitchPoint']=sysData[M]['Experiment']['cycles']
    
    elif (item=='LEDA' or item=='LEDC' or item=='LEDD' or item=='LEDE' or item=='LEDF' or item=='LEDG' or item == 'LEDH'): 
        setPWM(M,'PWM',sysItems[item],sysData[M][item]['target']*float(sysData[M][item]['ON']),0)
    elif (item=='LEDB' or item == 'LEDI'): #We must handle these differently in case they are simultaneously being used to mix with LEDV
        if (sysData[M]['LEDV']['target']*float(sysData[M]['LEDV']['ON'])>0): #If LEDV is on, we need to make up the difference in these other LEDs.
            # First determine what is the intensity for this LED required to maintain current LEDV level. Note we have alreayd checked that LEDV is on.
            if (item=='LEDB'):
                LEDV_Intensity = sysData[M]['LEDV']['target']*sysData[M]['LEDV']['ScaleFactor'] 
            elif (item == 'LEDI'):
                LEDV_Intensity = sysData[M]['LEDV']['target']
            
            NewIntensity = sysData[M][item]['target']*float(sysData[M][item]['ON']) + LEDV_Intensity #Add on whatever extra intensity is required to maintain LEDV level.
            if (NewIntensity>1.0):
                NewIntensity=1.0
                
            setPWM(M,'PWM',sysItems[item],NewIntensity,0)

        else:
            setPWM(M,'PWM',sysItems[item],sysData[M][item]['target']*float(sysData[M][item]['ON']),0)
    elif (item=='LEDV'): #This is the virtual white LED which is made by combinng LEDB and LEDI
        LEDB_Intensity = sysData[M]['LEDV']['target']*float(sysData[M]['LEDV']['ON'])*sysData[M]['LEDV']['ScaleFactor'] #This is the intensity of the blue we want mixed into our white light
        LEDB_Intensity = LEDB_Intensity + sysData[M]['LEDB']['target']*float(sysData[M]['LEDB']['ON']) #This adds the intensity of the blue we already have on

        LEDI_Intensity = sysData[M]['LEDV']['target']*float(sysData[M]['LEDV']['ON']) #This is the intensity of the Lime, similar to above.
        LEDI_Intensity = LEDI_Intensity + sysData[M]['LEDI']['target']*float(sysData[M]['LEDI']['ON']) 

        if (LEDB_Intensity>1.0): #If we are exceeding the maximum intensity, we are going to force a saturation.
            LEDB_Intensity=1.0
        if (LEDI_Intensity>1.0):
            LEDI_Intensity=1.0

        setPWM(M,'PWM',sysItems['LEDB'],LEDB_Intensity,0)
        setPWM(M,'PWM',sysItems['LEDI'],LEDI_Intensity,0)
        
    elif(item == 'LASER650'): #This is if we are setting the Laser
        
        value=sysData[M][item]['target']*float(sysData[M][item]['ON']) 
        if (value==0):
            value=0
        else:
            value=(value+0.00)/1.00
            sf=0.303 #This factor is scaling down the maximum voltage being fed to the laser, preventing its photodiode current (and hence optical power) being too large.
            value=value*sf
        binaryValue=bin(int(value*4095.9)) #Bit of a dodgy method for ensuring we get an integer in [0,4095]
        toWrite=str(binaryValue[2:].zfill(16))
        toWrite1=int(toWrite[0:8],2)
        toWrite2=int(toWrite[8:16],2)
        I2CCom(M,'DAC',0,8,toWrite1,toWrite2,0)

def SetOutputOn(M,item,force):
    #General function used to switch an output on or off.
    global sysData
    item = str(item)
    
    force = int(force)
    M=str(M)
    if (M=="0"):
        M=sysItems['UIDevice']
    #The first statements are to force it on or off it the command is called in force mode (force implies it sets it to a given state, regardless of what it is currently in)
    if (force==1):
        sysData[M][item]['ON']=1
        SetOutput(M,item)
        return ('', 204)    
    
    elif(force==0):
        sysData[M][item]['ON']=0;
        SetOutput(M,item)
        return ('', 204)    
    
    #Elsewise this is doing a flip operation (i.e. changes to opposite state to that which it is currently in)
    if (sysData[M][item]['ON']==0):
        sysData[M][item]['ON']=1
        SetOutput(M,item)
        return ('', 204)    
    
    else:
        sysData[M][item]['ON']=0;
        SetOutput(M,item)
        return ('', 204)    

def turnEverythingOff(M):
    # Function which turns off all actuation/hardware.
    for LED in ['LEDA','LEDB','LEDC','LEDD','LEDE','LEDF','LEDG','LEDH','LEDI','LEDV']:
        sysData[M][LED]['ON']=0
        
    sysData[M]['LASER650']['ON']=0
    sysData[M]['Pump1']['ON']=0
    sysData[M]['Pump2']['ON']=0
    sysData[M]['Pump3']['ON']=0
    sysData[M]['Pump4']['ON']=0
    sysData[M]['Stir']['ON']=0
    sysData[M]['Heat']['ON']=0
    sysData[M]['UV']['ON']=0
    
    I2CCom(M,'DAC',0,8,int('00000000',2),int('00000000',2),0)#Sets all DAC Channels to zero!!! 
    setPWM(M,'PWM',sysItems['All'],0,0)
    setPWM(M,'Pumps',sysItems['All'],0,0)
    
    SetOutputOn(M,'Stir',0)
    SetOutputOn(M,'Thermostat',0)
    SetOutputOn(M,'Heat',0)
    SetOutputOn(M,'UV',0)
    SetOutputOn(M,'Pump1',0)
    SetOutputOn(M,'Pump2',0)
    SetOutputOn(M,'Pump3',0)
    SetOutputOn(M,'Pump4',0)

def AS7341SMUX(M,device,data1,data2):
    #Sets up the ADC multiplexer on the spectrometer, this is responsible for connecting photodiodes to amplifier/adc circuits within the device. 
    #The spectrometer has only got 6 ADCs but >6 photodiodes channels, hence you need to select a subset of photodiodes to measure with each shot. The relative gain does change slightly (1-2%) between ADCs.
    global sysItems
    global sysData
    global sysDevices
    M=str(M)
    Addresses=['0x00','0x01','0x02','0x03','0x04','0x05','0x06','0x07','0x08','0x0A','0x0B','0x0C','0x0D','0x0E','0x0F','0x10','0x11','0x12']
    for a in Addresses:
        A=sysItems['AS7341'][a]['A']
        B=sysItems['AS7341'][a]['B']
        if (A!='U'):
            As=sysData[M]['AS7341']['channels'][A]
        else:
            As=0
        if (B!='U'):
            Bs=sysData[M]['AS7341']['channels'][B]
        else:
            Bs=0
        Ab=str(bin(As))[2:].zfill(4)
        Bb=str(bin(Bs))[2:].zfill(4)
        C=Ab+Bb
        #time.sleep(0.001) #Added this to remove errors where beaglebone crashed!
        I2CCom(M,'AS7341',0,8,int(a,16),int(C,2),0) #Tells it we are going to now write SMUX configuration to RAM
        #sysDevices[M][device]['device'].write8(int(a,16),int(C,2))

def AS7341Read(M,Gain,ISteps,reset):
    #Responsible for reading data from the spectrometer.
    global sysItems
    global sysData
    reset=int(reset)
    ISteps=int(ISteps)
    if ISteps>255:
        ISteps=255 #255 steps is approx 0.71 seconds.
    elif (ISteps<0):
        ISteps=0
    if Gain>10:
        Gain=10 #512x
    elif (Gain<0):
        Gain=0 #0.5x

    I2CCom(M,'AS7341',0,8,int(0xA9),int(0x04),0) #This sets us into BANK mode 0, for accesing registers 0x80+. The 4 means we have WTIMEx16
    if (reset==1):
        I2CCom(M,'AS7341',0,8,int(0x80),int(0x00),0) #Turns power down
        time.sleep(0.01)
        I2CCom(M,'AS7341',0,8,int(0x80),int(0x01),0) #Turns power on with spectral measurement disabled
    else:
        I2CCom(M,'AS7341',0,8,int(0x80),int(0x01),0)  #Turns power on with spectral measurement disabled

    I2CCom(M,'AS7341',0,8,int(0xAF),int(0x10),0) #Tells it we are going to now write SMUX configuration to RAM
    
    
    #I2CCom(M,'AS7341',0,100,int(0x00),int(0x00),0) #Forces AS7341SMUX to run since length is 100.
    AS7341SMUX(M,'AS7341',0,0)
    
    I2CCom(M,'AS7341',0,8,int(0x80),int(0x11),0)  #Runs SMUX command (i.e. cofigures SMUX with data from ram)
    time.sleep(0.001)
    I2CCom(M,'AS7341',0,8,int(0x81),ISteps,0)  #Sets number of integration steps of length 2.78ms Max ISteps is 255
    I2CCom(M,'AS7341',0,8,int(0x83),0xFF,0)  #Sets maxinum wait time of 0.7mS (multiplex by 16 due to WLONG)
    I2CCom(M,'AS7341',0,8,int(0xAA),Gain,0)  #Sets gain on ADCs. Maximum value of Gain is 10 and can take values from 0 to 10.
    #I2CCom(M,'AS7341',0,8,int(0xA9),int(0x14),0) #This sets us into BANK mode 1, for accessing 0x60 to 0x74. The 4 means we have WTIMEx16
    #I2CCom(M,'AS7341',0,8,int(0x70),int(0x00),0)  #Sets integration mode SPM (normal mode)
    #Above is default of 0x70!
    I2CCom(M,'AS7341',0,8,int(0x80),int(0x0B),0)  #Starts spectral measurement, with WEN (wait between measurements feature) enabled.
    time.sleep((ISteps+1)*0.0028 + 0.2) #Wait whilst integration is done and results are processed. 
    
    ASTATUS=int(I2CCom(M,'AS7341',1,8,0x94,0x00,0)) #Get measurement status, including saturation details.
    C0_L=int(I2CCom(M,'AS7341',1,8,0x95,0x00,0))
    C0_H=int(I2CCom(M,'AS7341',1,8,0x96,0x00,0))
    C1_L=int(I2CCom(M,'AS7341',1,8,0x97,0x00,0))
    C1_H=int(I2CCom(M,'AS7341',1,8,0x98,0x00,0))
    C2_L=int(I2CCom(M,'AS7341',1,8,0x99,0x00,0))
    C2_H=int(I2CCom(M,'AS7341',1,8,0x9A,0x00,0))
    C3_L=int(I2CCom(M,'AS7341',1,8,0x9B,0x00,0))
    C3_H=int(I2CCom(M,'AS7341',1,8,0x9C,0x00,0))
    C4_L=int(I2CCom(M,'AS7341',1,8,0x9D,0x00,0))
    C4_H=int(I2CCom(M,'AS7341',1,8,0x9E,0x00,0))
    C5_L=int(I2CCom(M,'AS7341',1,8,0x9F,0x00,0))
    C5_H=int(I2CCom(M,'AS7341',1,8,0xA0,0x00,0))

    I2CCom(M,'AS7341',0,8,int(0x80),int(0x01),0)  #Stops spectral measurement, leaves power on.

    #Status2=int(I2CCom(M,'AS7341',1,8,0xA3,0x00,0)) #Reads system status at end of spectral measursement. 
    #print(str(ASTATUS))
    #print(str(Status2))

    sysData[M]['AS7341']['current']['ADC0']=int(bin(C0_H)[2:].zfill(8)+bin(C0_L)[2:].zfill(8),2)
    sysData[M]['AS7341']['current']['ADC1']=int(bin(C1_H)[2:].zfill(8)+bin(C1_L)[2:].zfill(8),2)
    sysData[M]['AS7341']['current']['ADC2']=int(bin(C2_H)[2:].zfill(8)+bin(C2_L)[2:].zfill(8),2)
    sysData[M]['AS7341']['current']['ADC3']=int(bin(C3_H)[2:].zfill(8)+bin(C3_L)[2:].zfill(8),2)
    sysData[M]['AS7341']['current']['ADC4']=int(bin(C4_H)[2:].zfill(8)+bin(C4_L)[2:].zfill(8),2)
    sysData[M]['AS7341']['current']['ADC5']=int(bin(C5_H)[2:].zfill(8)+bin(C5_L)[2:].zfill(8),2)
    
    
    if (sysData[M]['AS7341']['current']['ADC0']==65535 or sysData[M]['AS7341']['current']['ADC1']==65535 or sysData[M]['AS7341']['current']['ADC2']==65535 or sysData[M]['AS7341']['current']['ADC3']==65535 or sysData[M]['AS7341']['current']['ADC4']==65535 or sysData[M]['AS7341']['current']['ADC5']==65535 ):
        print(str(datetime.now()) + ' Spectrometer measurement was saturated on device ' + str(M)) #Not sure if this saturation check above actually works correctly...
    return 0

def GetLight(M,wavelengths,Gain,ISteps):
    #Runs spectrometer measurement and puts data into appropriate structure.
    global sysData
    M=str(M)
    channels=['nm410','nm440','nm470','nm510','nm550','nm583','nm620', 'nm670','CLEAR','NIR','DARK','ExtGPIO', 'ExtINT' , 'FLICKER']
    for channel in channels:
        sysData[M]['AS7341']['channels'][channel]=0 #First we set all measurement ADC indexes to zero.
    index=1;
    for wavelength in wavelengths:
        if wavelength != "OFF":
            sysData[M]['AS7341']['channels'][wavelength]=index #Now assign ADCs to each of the channel where needed. 
        index=index+1

    success=0
    while success<2:
        try:
            AS7341Read(M,Gain,ISteps,success) 
            success=2
        except:
            print(str(datetime.now()) + 'AS7341 measurement failed on ' + str(M))
            success=success+1
            if success==2:
                print(str(datetime.now()) + 'AS7341 measurement failed twice on ' + str(M) + ', setting unity values')
                sysData[M]['AS7341']['current']['ADC0']=1
                DACS=['ADC1', 'ADC2', 'ADC3', 'ADC4', 'ADC5']
                for DAC in DACS:
                    sysData[M]['AS7341']['current'][DAC]=0

    output=[0.0,0.0,0.0,0.0,0.0,0.0]
    index=0
    DACS=['ADC0', 'ADC1', 'ADC2', 'ADC3', 'ADC4', 'ADC5']
    for wavelength in wavelengths:
        if wavelength != "OFF":
            output[index]=sysData[M]['AS7341']['current'][DACS[index]]
        index=index+1

    return output