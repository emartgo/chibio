from .sys import sysItems, sysData
from .setup import *

from datetime import datetime 

def SetFPMeasurement(item,Excite,Base,Emit1,Emit2,Gain):
    #Sets up the fluorescent protein measurement in terms of gain, and which LED / measurement bands to use.
    FP=str(item)
    Excite=str(Excite)
    Base=str(Base)
    Emit1=str(Emit1)
    Emit2=str(Emit2)
    Gain=str(Gain)
    M=sysItems['UIDevice']
    
    if sysData[M][FP]['ON']==1:
        sysData[M][FP]['ON']=0
        return ('', 204)
    else: 
        sysData[M][FP]['ON']=1
        sysData[M][FP]['LED']=Excite
        sysData[M][FP]['BaseBand']=Base
        sysData[M][FP]['Emit1Band']=Emit1
        sysData[M][FP]['Emit2Band']=Emit2
        sysData[M][FP]['Gain']=Gain
        return ('', 204) 
    
def SetOutputTarget(M,item, value):
    #General function used to set the output level of a particular item, ensuring it is within an acceptable range.
    global sysData
    item = str(item)
    value = float(value)
    M=str(M)
    if (M=="0"):
        M=sysItems['UIDevice']
    print(str(datetime.now()) + " Set item: " + str(item) + " to value " + str(value) + " on " + str(M))
    if (value<sysData[M][item]['min']):
        value=sysData[M][item]['min']
    if (value>sysData[M][item]['max']):
        value=sysData[M][item]['max']
        
    sysData[M][item]['target']=value
    
    if(sysData[M][item]['ON']==1 and not(item=='OD' or item=='Thermostat')): #Checking to see if our item is already running, in which case
        SetOutputOn(M,item,0) #we turn it off and on again to restart at new rate.
        SetOutputOn(M,item,1)
    return ('', 204)    

def PumpModulation(M,item):
    #Responsible for turning pumps on/off with an appropriate duty cycle. They are turned on for a fraction of each ~1minute cycle to achieve low pump rates.
    global sysData
    global sysItems
    global sysDevices
    
    sysDevices[M][item]['threadCount']=(sysDevices[M][item]['threadCount']+1)%100 #Index of the particular thread running.
    currentThread=sysDevices[M][item]['threadCount']
    
    while (sysDevices[M][item]['active']==1): #Idea is we will wait here if a previous thread on this pump is already running. Potentially all this 'active' business could be removed from this fuction.
        time.sleep(0.02)
        
    if (abs(sysData[M][item]['target']*sysData[M][item]['ON'])!=1 and currentThread==sysDevices[M][item]['threadCount']): #In all cases we turn things off to begin
        sysDevices[M][item]['active']=1
        setPWM(M,'Pumps',sysItems[item]['In1'],0.0*float(sysData[M][item]['ON']),0)
        setPWM(M,'Pumps',sysItems[item]['In2'],0.0*float(sysData[M][item]['ON']),0)
        setPWM(M,'Pumps',sysItems[item]['In1'],0.0*float(sysData[M][item]['ON']),0)
        setPWM(M,'Pumps',sysItems[item]['In2'],0.0*float(sysData[M][item]['ON']),0)
        sysDevices[M][item]['active']=0
    if (sysData[M][item]['ON']==0):
        return
    
    Time1=datetime.now()
    cycletime=sysData[M]['Experiment']['cycleTime']*1.05 #We make this marginally longer than the experiment cycle time to avoid too much chaos when you come back around to pumping again.
    
    Ontime=cycletime*abs(sysData[M][item]['target'])
    
    # Decided to remove the below section in order to prevent media buildup in the device if you are pumping in very rapidly. This check means that media is removed, then added. Removing this code means these happen simultaneously.
    #if (item=="Pump1" and abs(sysData[M][item]['target'])<0.3): #Ensuring we run Pump1 after Pump2.
    #    waittime=cycletime*abs(sysData[M]['Pump2']['target']) #We want to wait until the output pump has stopped, otherwise you are very inefficient with your media since it will be pumping out the fresh media fromthe top of the test tube right when it enters.
    #    time.sleep(waittime+1.0)  
        
    
    if (sysData[M][item]['target']>0 and currentThread==sysDevices[M][item]['threadCount']): #Turning on pumps in forward direction
        sysDevices[M][item]['active']=1
        setPWM(M,'Pumps',sysItems[item]['In1'],1.0*float(sysData[M][item]['ON']),0)
        setPWM(M,'Pumps',sysItems[item]['In2'],0.0*float(sysData[M][item]['ON']),0)
        sysDevices[M][item]['active']=0
    elif (sysData[M][item]['target']<0 and currentThread==sysDevices[M][item]['threadCount']): #Or backward direction.
        sysDevices[M][item]['active']=1
        setPWM(M,'Pumps',sysItems[item]['In1'],0.0*float(sysData[M][item]['ON']),0)
        setPWM(M,'Pumps',sysItems[item]['In2'],1.0*float(sysData[M][item]['ON']),0)
        sysDevices[M][item]['active']=0
  
    time.sleep(Ontime)
    
    if(abs(sysData[M][item]['target'])!=1 and currentThread==sysDevices[M][item]['threadCount']): #Turning off pumps at appropriate time.
        sysDevices[M][item]['active']=1
        setPWM(M,'Pumps',sysItems[item]['In1'],0.0*float(sysData[M][item]['ON']),0)
        setPWM(M,'Pumps',sysItems[item]['In2'],0.0*float(sysData[M][item]['ON']),0)
        setPWM(M,'Pumps',sysItems[item]['In1'],0.0*float(sysData[M][item]['ON']),0)
        setPWM(M,'Pumps',sysItems[item]['In2'],0.0*float(sysData[M][item]['ON']),0)
        sysDevices[M][item]['active']=0
    
    Time2=datetime.now()
    elapsedTime=Time2-Time1
    elapsedTimeSeconds=round(elapsedTime.total_seconds(),2)
    Offtime=cycletime-elapsedTimeSeconds
    if (Offtime>0.0):
        time.sleep(Offtime)   
    
    
    if (sysData[M][item]['ON']==1 and sysDevices[M][item]['threadCount']==currentThread): #If pumps need to keep going, this starts a new pump thread.
        sysDevices[M][item]['thread']=Thread(target = PumpModulation, args=(M,item))
        sysDevices[M][item]['thread'].setDaemon(True)
        sysDevices[M][item]['thread'].start();
    
def MeasureTemp(M,which): 
    #Used to measure temperature from each thermometer.
    global sysData
    global sysItems
   
    if (M=="0"):
        M=sysItems['UIDevice']
    M=str(M)
    which='Thermometer' + str(which)
    if (which=='ThermometerInternal' or which=='ThermometerExternal'):
        getData=I2CCom(M,which,1,16,0x05,0,0)
        getDataBinary=bin(getData)
        tempData=getDataBinary[6:]
        temperature=float(int(tempData,2))/16.0
    elif(which=='ThermometerIR'):
        getData=I2CCom(M,which,1,0,0x07,0,1)
        temperature = (getData*0.02) - 273.15

    if sysData[M]['present']==0:
        temperature=0.0
    if temperature>100.0:#It seems sometimes the IR thermometer returns a value of 1000 due to an error. This prevents that.
        temperature=sysData[M][which]['current']
    sysData[M][which]['current']=temperature
    return ('', 204)        

def Thermostat(M,item):
    #Function that implements thermostat temperature control using MPC algorithm.
    global sysData
    global sysItems
    global sysDevices
    ON=sysData[M][item]['ON']
    sysDevices[M][item]['threadCount']=(sysDevices[M][item]['threadCount']+1)%100
    currentThread=sysDevices[M][item]['threadCount']
    
    if (ON==0):
        SetOutputOn(M,'Heat',0)
        return
    
    MeasureTemp(M,'IR') #Measures temperature - note that this may be happening DURING stirring.

    CurrentTemp=sysData[M]['ThermometerIR']['current']
    TargetTemp=sysData[M]['Thermostat']['target']
    LastTemp=sysData[M]['Thermostat']['last']
    
    #MPC Controller Component
    MediaTemp=sysData[M]['ThermometerExternal']['current']
    MPC=0
    if (MediaTemp>0.0):
        Tdiff=CurrentTemp-MediaTemp
        Pumping=sysData[M]['Pump1']['target']*float(sysData[M]['Pump1']['ON'])*float(sysData[M]['OD']['ON'])
        Gain=2.5
        MPC=Gain*Tdiff*Pumping
        
        
    #PI Controller Component
    e=TargetTemp-CurrentTemp
    dt=sysData[M]['Thermostat']['cycleTime']
    I=sysData[M]['Thermostat']['Integral']
    if (abs(e)<2.0):
        I=I+0.0005*dt*e
        P=0.25*e
    else:
        P=0.5*e;
    
    if (abs(TargetTemp-LastTemp)>2.0): #This resets integrator if we make a big jump in set point.
        I=0.0
    elif(I<0.0):
        I=0.0
    elif (I>1.0):
        I=1.0
    
    sysData[M]['Thermostat']['Integral']=I

    U=P+I+MPC
    
    if(U>1.0):
        U=1.0
        sysData[M]['Heat']['target']=U
        sysData[M]['Heat']['ON']=1
    elif(U<0):  
        U=0
        sysData[M]['Heat']['target']=U
        sysData[M]['Heat']['ON']=0
    else:
        sysData[M]['Heat']['target']=U
        sysData[M]['Heat']['ON']=1
    
    sysData[M]['Thermostat']['last']=sysData[M]['Thermostat']['target']
   
    SetOutput(M,'Heat')
    
    time.sleep(dt)  
        
    
    if (sysData[M][item]['ON']==1 and sysDevices[M][item]['threadCount']==currentThread):
        sysDevices[M][item]['thread']=Thread(target = Thermostat, args=(M,item))
        sysDevices[M][item]['thread'].setDaemon(True)
        sysDevices[M][item]['thread'].start();
    else:
        sysData[M]['Heat']['ON']=0
        sysData[M]['Heat']['target']=0
        SetOutput(M,'Heat')

def direction(M,item):
    #Flips direction of a pump.
    global sysData
    M=str(M)
    if (M=="0"):
        M=sysItems['UIDevice']
    sysData[M][item]['target']=-1.0*sysData[M][item]['target']
    if (sysData[M]['OD']['ON']==1):
            sysData[M][item]['direction']=-1.0*sysData[M][item]['direction']

    return ('', 204)  

def GetSpectrum(M,Gain):
    #Measures entire spectrum, i.e. every different photodiode, which requires 2 measurement shots. 
    Gain=int(Gain[1:])
    global sysData
    global sysItems
    M=str(M)   
    if (M=="0"):
        M=sysItems['UIDevice']
    out=GetLight(M,['nm410','nm440','nm470','nm510','nm550','nm583'],Gain,255)
    out2=GetLight(M,['nm620', 'nm670','CLEAR','NIR','DARK'],Gain,255)
    sysData[M]['AS7341']['spectrum']['nm410']=out[0]
    sysData[M]['AS7341']['spectrum']['nm440']=out[1]
    sysData[M]['AS7341']['spectrum']['nm470']=out[2]
    sysData[M]['AS7341']['spectrum']['nm510']=out[3]
    sysData[M]['AS7341']['spectrum']['nm550']=out[4]
    sysData[M]['AS7341']['spectrum']['nm583']=out[5]
    sysData[M]['AS7341']['spectrum']['nm620']=out2[0]
    sysData[M]['AS7341']['spectrum']['nm670']=out2[1]
    sysData[M]['AS7341']['spectrum']['CLEAR']=out2[2]
    sysData[M]['AS7341']['spectrum']['NIR']=out2[3]
    
        
    return ('', 204)   

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

def GetTransmission(M,item,wavelengths,Gain,ISteps):
    #Gets light transmission through sample by turning on light, measuring, turning off light.
    global sysData
    M=str(M)
    SetOutputOn(M,item,1)
    output=GetLight(M,wavelengths,Gain,ISteps)
    SetOutputOn(M,item,0)
    return output

def SetLightActuation(Excite):
    #Basic function used to set which LED is used for optogenetics.
    global sysData
    M=sysItems['UIDevice']
    item="Light"
    if sysData[M][item]['ON']==1:
        sysData[M][item]['ON']=0
        SetOutputOn(M,sysData[M][item]['Excite'],0) #In case the current LED is on we need to make sure it turns off
        return ('', 204)
    else:
        sysData[M][item]['Excite']=str(Excite)
        sysData[M][item]['ON']=1
        return('',204)
        
def LightActuation(M,toggle):
    #Another optogenetic function, turning LEDs on/off during experiment as appropriate.
    global sysData
    M=str(M)
    toggle=int(toggle)
    LEDChoice=sysData[M]['Light']['Excite']
    if (toggle==1 and sysData[M]['Light']['ON']==1):
        SetOutputOn(M,LEDChoice,1)
    else:
        SetOutputOn(M,LEDChoice,0)
    return 0

def CalibrateOD(M,item,value,value2):
    #Used to calculate calibration value for OD measurements.
    global sysData
    item = str(item)
    ODRaw = float(value)
    ODActual = float(value2)
    M=str(M)
    if (M=="0"):
        M=sysItems['UIDevice']
        
    device=sysData[M]['OD']['device']
    if (device=='LASER650'):
        a=sysData[M]['OD0']['LASERa']#Retrieve the calibration factors for OD.
        b=sysData[M]['OD0']['LASERb'] 
        if (ODActual<0):
            ODActual=0
            print(str(datetime.now()) + "You put a negative OD into calibration! Setting it to 0")
        
        raw=((ODActual/a +  (b/(2*a))**2)**0.5) - (b/(2*a)) #THis is performing the inverse function of the quadratic OD calibration.
        OD0=(10.0**raw)*ODRaw
        if (OD0<sysData[M][item]['min']):
            OD0=sysData[M][item]['min']
            print(str(datetime.now()) + 'OD calibration value seems too low?!')

        if (OD0>sysData[M][item]['max']):
            OD0=sysData[M][item]['max']
            print(str(datetime.now()) + 'OD calibration value seems too high?!')

    
        sysData[M][item]['target']=OD0
        print(str(datetime.now()) + "Calibrated OD")
    elif (device=='LEDF'):
        a=sysData[M]['OD0']['LEDFa']#Retrieve the calibration factors for OD.
        
        if (ODActual<0):
            ODActual=0
            print("You put a negative OD into calibration! Setting it to 0")
        if (M=='M0'):
            CF=1299.0
        elif (M=='M1'):
            CF=1206.0
        elif (M=='M2'):
            CF=1660.0
        elif (M=='M3'):
            CF=1494.0
            
        #raw=(ODActual)/a  #THis is performing the inverse function of the linear OD calibration.
        #OD0=ODRaw - raw*CF
        OD0=ODRaw/ODActual
        print(OD0)
    
        if (OD0<sysData[M][item]['min']):
            OD0=sysData[M][item]['min']
            print('OD calibration value seems too low?!')
        if (OD0>sysData[M][item]['max']):
            OD0=sysData[M][item]['max']
            print('OD calibration value seems too high?!')
    
        sysData[M][item]['target']=OD0
        print("Calibrated OD")
    elif (device=='LEDA'):
        a=sysData[M]['OD0']['LEDAa']#Retrieve the calibration factors for OD.
        
        if (ODActual<0):
            ODActual=0
            print("You put a negative OD into calibration! Setting it to 0")
        if (M=='M0'):
            CF=422
        elif (M=='M1'):
            CF=379
        elif (M=='M2'):
            CF=574
        elif (M=='M3'):
            CF=522
            
        #raw=(ODActual)/a  #THis is performing the inverse function of the linear OD calibration.
        #OD0=ODRaw - raw*CF
        OD0=ODRaw/ODActual
        print(OD0)
    
        if (OD0<sysData[M][item]['min']):
            OD0=sysData[M][item]['min']
            print('OD calibration value seems too low?!')
        if (OD0>sysData[M][item]['max']):
            OD0=sysData[M][item]['max']
            print('OD calibration value seems too high?!')
    
        sysData[M][item]['target']=OD0
        print("Calibrated OD")
        
    return ('', 204) 

def MeasureOD(M):
    #Measures laser transmission and calculates calibrated OD from this.
    global sysData
    global sysItems
    M=str(M)
    if (M=="0"):
        M=sysItems['UIDevice']
    device=sysData[M]['OD']['device']
    if (device=='LASER650'):
        out=GetTransmission(M,'LASER650',['CLEAR'],1,255)
        sysData[M]['OD0']['raw']=float(out[0])
    
        a=sysData[M]['OD0']['LASERa']#Retrieve the calibration factors for OD.
        b=sysData[M]['OD0']['LASERb'] 
        if abs(sysData[M]['OD0']['raw']) > 0.001: # avoid devision by 0
            raw=math.log10(sysData[M]['OD0']['target']/sysData[M]['OD0']['raw'])
            sysData[M]['OD']['current']=raw*b + raw*raw*a
        else:
            sysData[M]['OD']['current']=0
            print(str(datetime.now()) + ' OD Measurement close to 0 on ' + str(device))
    elif (device=='LEDF'):
        out=GetTransmission(M,'LEDF',['CLEAR'],7,255)

        sysData[M]['OD0']['raw']=out[0]
        a=sysData[M]['OD0']['LEDFa']#Retrieve the calibration factors for OD.
        try:
            if (M=='M0'):
                CF=1299.0
            elif (M=='M1'):
                CF=1206.0
            elif (M=='M2'):
                CF=1660.0
            elif (M=='M3'):
                CF=1494.0
            #raw=out[0]/CF - sysData[M]['OD0']['target']/CF
            raw=out[0]/sysData[M]['OD0']['target']
            sysData[M]['OD']['current']=raw
        except:
            sysData[M]['OD']['current']=0;
            print(str(datetime.now()) + ' OD Measurement exception on ' + str(device))

    elif (device=='LEDA'):
        out=GetTransmission(M,'LEDA',['CLEAR'],7,255)

        sysData[M]['OD0']['raw']=out[0]
        a=sysData[M]['OD0']['LEDAa']#Retrieve the calibration factors for OD.
        try:
            if (M=='M0'):
                CF=422.0
            elif (M=='M1'):
                CF=379.0
            elif (M=='M2'):
                CF=574.0
            elif (M=='M3'):
                CF=522.0
            #raw=out[0]/CF - sysData[M]['OD0']['target']/CF
            raw=out[0]/sysData[M]['OD0']['target']
            #sysData[M]['OD']['current']=raw*a
            sysData[M]['OD']['current']=raw
        except:
            sysData[M]['OD']['current']=0;
            print(str(datetime.now()) + ' OD Measurement exception on ' + str(device))
    
    return ('', 204)  

def MeasureFP(M):
    #Responsible for measuring each of the active Fluorescent proteins.
    global sysData
    M=str(M)
    if (M=="0"):
        M=sysItems['UIDevice']
    for FP in ['FP1','FP2','FP3']:
        if sysData[M][FP]['ON']==1:
            Gain=int(sysData[M][FP]['Gain'][1:])
            out=GetTransmission(M,sysData[M][FP]['LED'],[sysData[M][FP]['BaseBand'],sysData[M][FP]['Emit1Band'],sysData[M][FP]['Emit2Band']],Gain,255)
            sysData[M][FP]['Base']=float(out[0])
            if (sysData[M][FP]['Base']>0):
                sysData[M][FP]['Emit1']=float(out[1])/sysData[M][FP]['Base']
                sysData[M][FP]['Emit2']=float(out[2])/sysData[M][FP]['Base']
            else:#This might happen if you try to measure in CLEAR whilst also having CLEAR as baseband! 
                sysData[M][FP]['Emit1']=float(out[1]) 
                sysData[M][FP]['Emit2']=float(out[2])

    return ('', 204)      
    
def MeasureTemp(M,which): 
    #Used to measure temperature from each thermometer.
    global sysData
    global sysItems
   
    if (M=="0"):
        M=sysItems['UIDevice']
    M=str(M)
    which='Thermometer' + str(which)
    if (which=='ThermometerInternal' or which=='ThermometerExternal'):
        getData=I2CCom(M,which,1,16,0x05,0,0)
        getDataBinary=bin(getData)
        tempData=getDataBinary[6:]
        temperature=float(int(tempData,2))/16.0
    elif(which=='ThermometerIR'):
        getData=I2CCom(M,which,1,0,0x07,0,1)
        temperature = (getData*0.02) - 273.15

    if sysData[M]['present']==0:
        temperature=0.0
    if temperature>100.0:#It seems sometimes the IR thermometer returns a value of 1000 due to an error. This prevents that.
        temperature=sysData[M][which]['current']
    sysData[M][which]['current']=temperature
    return ('', 204) 

def Zigzag(M):
    #This function dithers OD in a "zigzag" pattern, and estimates growthrate. This function is only called when ZigZag mode is active.
    global sysData
    global sysItems
    M=str(M)
    centre=sysData[M]['OD']['target']
    current=sysData[M]['OD']['current']
    zig=sysData[M]['Zigzag']['Zig']
    iteration=sysData[M]['Experiment']['cycles']
	
    try:
        last=sysData[M]['OD']['record'][-1]
    except: #This will happen if you activate Zigzag in first control iteration!
        last=current
    
    if (current<centre-zig and last<centre):
        if(sysData[M]['Zigzag']['target']!=5.0):
            sysData[M]['Zigzag']['SwitchPoint']=iteration
        sysData[M]['Zigzag']['target']=5.0 #an excessively high OD value.
    elif (current>centre+zig and last>centre+zig):
        sysData[M]['Zigzag']['target']=centre-zig*1.5
        sysData[M]['Zigzag']['SwitchPoint']=iteration

    sysData[M]['OD']['target']=sysData[M]['Zigzag']['target']
	
    #Subsequent section is for growth estimation.
	
    TimeSinceSwitch=iteration-sysData[M]['Zigzag']['SwitchPoint']
    if (iteration>6 and TimeSinceSwitch>5 and current > 0 and last > 0 and sysData[M]['Zigzag']['target']==5.0): #The reason we wait a few minutes after starting growth is that new media may still be introduced, it takes a while for the growth to get going.
        dGrowthRate=(math.log(current)-math.log(last))*60.0 #Converting to units of 1/hour
        sysData[M]['GrowthRate']['current']=sysData[M]['GrowthRate']['current']*0.95 + dGrowthRate*0.05 #We are essentially implementing an online growth rate estimator with learning rate 0.05

    return

def RegulateOD(M):
    #Function responsible for turbidostat functionality (OD control)
    global sysData
    global sysItems
    M=str(M)
    
    if (sysData[M]['Zigzag']['ON']==1):
        TargetOD=sysData[M]['OD']['target']
        Zigzag(M) #Function that calculates new target pump rates, and sets pumps to desired rates. 

    
    Pump1Current=abs(sysData[M]['Pump1']['target'])
    Pump2Current=abs(sysData[M]['Pump2']['target'])
    Pump1Direction=sysData[M]['Pump1']['direction']
    Pump2Direction=sysData[M]['Pump2']['direction']
    
    
    
    ODNow=sysData[M]['OD']['current']
    ODTarget=sysData[M]['OD']['target']
    if (ODTarget<=0): #There could be an error on the log operationif ODTarget is 0!
        ODTarget=0.000001
        
    errorTerm=ODTarget-ODNow
    Volume=sysData[M]['Volume']['target']
    
    PercentPerMin=4*60/Volume #Gain parameter to convert from pump rate to rate of OD reduction.

    if sysData[M]['Experiment']['cycles']<3:
        Pump1=0 #In first few cycles we do precisely no pumping.
    elif len(sysData[M]['time']['record']) < 2:
        Pump1=0 #In first few cycles we do precisely no pumping.
        addTerminal(M, "Warning: Tried to calculate time elapsed with fewer than two " +\
    				"timepoints recorded. If you see this message a lot, there may be " +\
    				"a more serious problem.")
    else:
        ODPast=sysData[M]['OD']['record'][-1]
        timeElapsed=((sysData[M]['time']['record'][-1])-(sysData[M]['time']['record'][-2]))/60.0 #Amount of time betwix measurements in minutes
        if (ODNow>0):
            try:
                NewGrowth = math.log((ODTarget)/(ODNow))/timeElapsed
            except:
                NewGrowth=0.0
        else:
            NewGrowth=0.0
            
        Pump1=-1.0*NewGrowth/PercentPerMin
        
        #Next Section is Integral Control
        ODerror=ODNow-ODTarget
        # Integrator 1 - resoponsible for short-term integration to overcome troubles if an input pump makes a poor seal.
        ODIntegral=sysData[M]['OD']['Integral']
        if ODerror<0.01:
            ODIntegral=0
        elif (abs(ODNow-ODPast)<0.05 and ODerror>0.025): #preventing massive accidental jumps causing trouble with this integral term.
            ODIntegral=ODIntegral+0.1*ODerror
        sysData[M]['OD']['Integral']=ODIntegral
        # Integrator 2 
        ODIntegral2=sysData[M]['OD']['Integral2']
        if (abs(ODerror)>0.1 and abs(ODNow-ODPast)<0.05):
            ODIntegral2=0
        elif (abs(ODNow-ODPast)<0.1):
            ODIntegral2=ODIntegral2+0.01*ODerror
            Pump1=Pump1*0.7 #This is essentially enforcing a smaller Proportional gain when we are near to OD setpoint.
        sysData[M]['OD']['Integral2']=ODIntegral2
        
        Pump1=Pump1+ODIntegral+ODIntegral2
        
        if (ODNow-ODPast)>0.04: #This is to counteract noisy jumps in OD measurements from causing mayhem in the regulation algorithm.
            Pump1=0.0

    #Make sure values are in appropriate range. We want to limit the maximum size of pump1 to prevent it from overflowing.
    if(Pump1>0.02):
        Pump1=0.02
    elif(Pump1<0):
        Pump1=0.0

    if(sysData[M]['Chemostat']['ON']==1):
        Pump1=float(sysData[M]['Chemostat']['p1'])

    #Set new Pump targets
    sysData[M]['Pump1']['target']=Pump1*Pump1Direction
    sysData[M]['Pump2']['target']=(Pump1*4+0.07)*Pump2Direction

    if(sysData[M]['Experiment']['cycles']%5==1): #Every so often we do a big output pump to make sure tubes are clear.
        sysData[M]['Pump2']['target']=0.25*sysData[M]['Pump2']['direction']
    
    
    
    
    if (sysData[M]['Experiment']['cycles']>15):
        #This section is to check if we have added any liquid recently, if not, then we dont run pump 2 since it won't be needed.
        pastpumping=abs(sysData[M]['Pump1']['target'])
        for pv in range(-10,-1):
            pastpumping=pastpumping+abs(sysData[M]['Pump1']['record'][pv])
        
        if pastpumping==0.0:
            sysData[M]['Pump2']['target']=0.0
            sysData[M]['Pump1']['target']=0.0 #This should be equal to 0 anyway.
        
        

    SetOutputOn(M,'Pump1',1)
    SetOutputOn(M,'Pump2',1)

        
    if (sysData[M]['Zigzag']['ON']==1): #If the zigzag growth estimation is running then we change OD setpoint appropriately.
        try:
            sysData[M]['OD']['target']=TargetOD
        except:
            print('Somehow you managed to activate Zigzag at a sub-optimal time')
            #Do nothing
 
    return

