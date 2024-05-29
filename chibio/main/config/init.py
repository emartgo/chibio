from .setup import *
from .arduino import SMBus

def initialise(M):
    #Function that initialises all parameters / clears stored values for a given device.
    #If you want to record/add values to sysData, recommend adding an initialisation line in here.
    global sysData
    global sysItems
    global sysDevices

    for LED in ['LEDA','LEDB','LEDC','LEDD','LEDE','LEDF','LEDG','LEDH','LEDI','LEDV']:
        sysData[M][LED]['target']=sysData[M][LED]['default']
        sysData[M][LED]['ON']=0
    
    sysData[M]['UV']['target']=sysData[M]['UV']['default']
    sysData[M]['UV']['ON']=0
    
    sysData[M]['LASER650']['target']=sysData[M]['LASER650']['default']
    sysData[M]['LASER650']['ON']=0
    
    FP='FP1'
    sysData[M][FP]['ON']=0
    sysData[M][FP]['LED']="LEDB"
    sysData[M][FP]['Base']=0
    sysData[M][FP]['Emit1']=0
    sysData[M][FP]['Emit2']=0
    sysData[M][FP]['BaseBand']="CLEAR"
    sysData[M][FP]['Emit1Band']="nm510"
    sysData[M][FP]['Emit2Band']="nm550"
    sysData[M][FP]['Gain']="x10"
    sysData[M][FP]['BaseRecord']=[]
    sysData[M][FP]['Emit1Record']=[]
    sysData[M][FP]['Emit2Record']=[]
    FP='FP2'
    sysData[M][FP]['ON']=0
    sysData[M][FP]['LED']="LEDD"
    sysData[M][FP]['Base']=0
    sysData[M][FP]['Emit1']=0
    sysData[M][FP]['Emit2']=0
    sysData[M][FP]['BaseBand']="CLEAR"
    sysData[M][FP]['Emit1Band']="nm583"
    sysData[M][FP]['Emit2Band']="nm620"
    sysData[M][FP]['BaseRecord']=[]
    sysData[M][FP]['Emit1Record']=[]
    sysData[M][FP]['Emit2Record']=[]
    sysData[M][FP]['Gain']="x10"
    FP='FP3'
    sysData[M][FP]['ON']=0
    sysData[M][FP]['LED']="LEDE"
    sysData[M][FP]['Base']=0
    sysData[M][FP]['Emit1']=0
    sysData[M][FP]['Emit2']=0
    sysData[M][FP]['BaseBand']="CLEAR"
    sysData[M][FP]['Emit1Band']="nm620"
    sysData[M][FP]['Emit2Band']="nm670"
    sysData[M][FP]['BaseRecord']=[]
    sysData[M][FP]['Emit1Record']=[]
    sysData[M][FP]['Emit2Record']=[]
    sysData[M][FP]['Gain']="x10"
 
    for PUMP in ['Pump1','Pump2','Pump3','Pump4']:
        sysData[M][PUMP]['default']=0.0;
        sysData[M][PUMP]['target']=sysData[M][PUMP]['default']
        sysData[M][PUMP]['ON']=0
        sysData[M][PUMP]['direction']=1.0
        sysDevices[M][PUMP]['threadCount']=0
        sysDevices[M][PUMP]['active']=0
        
    sysData[M]['Heat']['default']=0;
    sysData[M]['Heat']['target']=sysData[M]['Heat']['default']
    sysData[M]['Heat']['ON']=0

    sysData[M]['Thermostat']['default']=37.0;
    sysData[M]['Thermostat']['target']=sysData[M]['Thermostat']['default']
    sysData[M]['Thermostat']['ON']=0
    sysData[M]['Thermostat']['Integral']=0
    sysData[M]['Thermostat']['last']=-1

    sysData[M]['Stir']['target']=sysData[M]['Stir']['default']
    sysData[M]['Stir']['ON']=0
    
    sysData[M]['Light']['target']=sysData[M]['Light']['default']
    sysData[M]['Light']['ON']=0
    sysData[M]['Light']['Excite']='LEDD'
    
    sysData[M]['Custom']['Status']=sysData[M]['Custom']['default']
    sysData[M]['Custom']['ON']=0
    sysData[M]['Custom']['Program']='C1'
    
    sysData[M]['Custom']['param1']=0.0
    sysData[M]['Custom']['param2']=0.0
    sysData[M]['Custom']['param3']=0.0
    
    sysData[M]['OD']['current']=0.0
    sysData[M]['OD']['target']=sysData[M]['OD']['default'];
    sysData[M]['OD0']['target']=65000.0
    sysData[M]['OD0']['raw']=65000.0
    sysData[M]['OD']['device']='LASER650'

    sysData[M]['Volume']['target']=20.0
    
    clearTerminal(M)
    addTerminal(M,'System Initialised')
  
    sysData[M]['Experiment']['ON']=0
    sysData[M]['Experiment']['cycles']=0
    sysData[M]['Experiment']['threadCount']=0
    sysData[M]['Experiment']['startTime']=' Waiting '
    sysData[M]['Experiment']['startTimeRaw']=0
    sysData[M]['OD']['ON']=0
    sysData[M]['OD']['Measuring']=0
    sysData[M]['OD']['Integral']=0.0
    sysData[M]['OD']['Integral2']=0.0
    sysData[M]['Zigzag']['ON']=0
    sysData[M]['Zigzag']['target']=0.0
    sysData[M]['Zigzag']['SwitchPoint']=0
    sysData[M]['GrowthRate']['current']=sysData[M]['GrowthRate']['default']

    sysDevices[M]['Thermostat']['threadCount']=0

    channels=['nm410','nm440','nm470','nm510','nm550','nm583','nm620', 'nm670','CLEAR','NIR','DARK','ExtGPIO', 'ExtINT' , 'FLICKER']
    for channel in channels:
        sysData[M]['AS7341']['channels'][channel]=0
        sysData[M]['AS7341']['spectrum'][channel]=0
    DACS=['ADC0', 'ADC1', 'ADC2', 'ADC3', 'ADC4', 'ADC5']
    for DAC in DACS:
        sysData[M]['AS7341']['current'][DAC]=0

    sysData[M]['ThermometerInternal']['current']=0.0
    sysData[M]['ThermometerExternal']['current']=0.0
    sysData[M]['ThermometerIR']['current']=0.0
 
    sysData[M]['time']['record']=[]
    sysData[M]['OD']['record']=[]
    sysData[M]['OD']['targetrecord']=[]
    sysData[M]['Pump1']['record']=[]
    sysData[M]['Pump2']['record']=[]
    sysData[M]['Pump3']['record']=[]
    sysData[M]['Pump4']['record']=[]
    sysData[M]['Heat']['record']=[]
    sysData[M]['Light']['record']=[]
    sysData[M]['ThermometerInternal']['record']=[]
    sysData[M]['ThermometerExternal']['record']=[]
    sysData[M]['ThermometerIR']['record']=[]
    sysData[M]['Thermostat']['record']=[]
	
    sysData[M]['GrowthRate']['record']=[]

    sysDevices[M]['ThermometerInternal']['device']=I2C.get_i2c_device(0x18,2) #Get Thermometer on Bus 2!!!
    sysDevices[M]['ThermometerExternal']['device']=I2C.get_i2c_device(0x1b,2) #Get Thermometer on Bus 2!!!
    sysDevices[M]['DAC']['device']=I2C.get_i2c_device(0x48,2) #Get DAC on Bus 2!!!
    sysDevices[M]['AS7341']['device']=I2C.get_i2c_device(0x39,2) #Get OD Chip on Bus 2!!!!!
    sysDevices[M]['Pumps']['device']=I2C.get_i2c_device(0x61,2) #Get OD Chip on Bus 2!!!!!
    sysDevices[M]['Pumps']['startup']=0
    sysDevices[M]['Pumps']['frequency']=0x1e #200Hz PWM frequency
    sysDevices[M]['PWM']['device']=I2C.get_i2c_device(0x60,2) #Get OD Chip on Bus 2!!!!!
    sysDevices[M]['PWM']['startup']=0
    sysDevices[M]['PWM']['frequency']=0x03# 0x14 = 300hz, 0x03 is 1526 Hz PWM frequency for fan/LEDs, maximum possible. Potentially dial this down if you are getting audible ringing in the device! 
    #There is a tradeoff between large frequencies which can make capacitors in the 6V power regulation oscillate audibly, and small frequencies which result in the number of LED "ON" cycles varying during measurements.
    sysDevices[M]['ThermometerIR']['device']=SMBus(bus=2) #Set up SMBus thermometer
    sysDevices[M]['ThermometerIR']['address']=0x5a 
    
    # This section of commented code is used for testing I2C communication integrity.
    # sysData[M]['present']=1
    # getData=I2CCom(M,'ThermometerInternal',1,16,0x05,0,0)
    # i=0
    # while (1==1):
    #     i=i+1
    #     if (i%1000==1):
    #         print(str(i))
    #     sysDevices[M]['ThermometerInternal']['device'].readU8(int(0x05))
    # getData=I2CCom(M,which,1,16,0x05,0,0)
    
    scanDevices(M)
    if(sysData[M]['present']==1):
        turnEverythingOff(M)

        V1_Present=0
        V2_Present=0
        # Now we will detect LED version FIrst checking for version 2
        out=GetLight(M,['nm583'],10,10) #Measure with maximum gain (10) and for short period.
        Baseline=out[0]
        SetOutputOn(M,'LEDH',1) #Turn on LEDH at default level - should only be present in version 2
        out=GetLight(M,['nm583'],10,10)
        NewLevel=out[0]
        SetOutputOn(M,'LEDH',0) #Turn off LEDH at default level - should only be present in version 2
        if (NewLevel>Baseline*3+20):
            V2_Present = 1
            
        #print(str(datetime.now()) + ' Baseline: ' + str(Baseline) + ' New Level: ' + str(NewLevel))

         # Now we will detect for Version 1
        out=GetLight(M,['nm583'],10,10) #Measure with maximum gain (10) and for short period.
        Baseline=out[0]
        SetOutputOn(M,'LEDG',1) #Turn on LEDG at default level - should only be present in version 1
        out=GetLight(M,['nm583'],10,10)
        NewLevel=out[0]
        SetOutputOn(M,'LEDG',0) #Turn off LEDG at default level - should only be present in version 1
        #print(str(datetime.now()) + ' Baseline: ' + str(Baseline) + ' New Level: ' + str(NewLevel))

        if (NewLevel>Baseline*3+20):
            V1_Present = 1        
        if (V1_Present==1 and V2_Present==0):
            sysData[M]['Version']['LED']=1
        elif (V1_Present==0 and V2_Present==1):
            sysData[M]['Version']['LED']=2
        else:
            sysData[M]['Version']['LED']=1 #We have messed up somehow in this case and stuff isn't going to work well
            print(str(datetime.now()) + " ERROR on " + str(M) +', this device has an unknown LED version. Defaulting to version 1.')

        print(str(datetime.now()) + " Initialised " + str(M) +', LED Version: ' + str(sysData[M]['Version']['LED']) + ', Device ID: ' + sysData[M]['DeviceID'])

def initialiseAll():
    # Initialisation function which runs at when software is started for the first time.
    sysItems['Multiplexer']['device']=I2C.get_i2c_device(0x74,2) 
    sysItems['FailCount']=0
    time.sleep(2.0) #This wait is to allow the watchdog circuit to boot.
    print(str(datetime.now()) + ' Initialising devices')

    for M in ['M0','M1','M2','M3','M4','M5','M6','M7']:
        initialise(M)
    scanDevices("all")

def ExperimentReset():
    #Resets parameters/values of a given experiment.
    initialise(sysItems['UIDevice'])
    return ('', 204)  

def ExperimentStartStop(M,value):
    #Stops or starts an experiment. 
    global sysData
    global sysDevices
    global sysItems
    M=str(M)
    if (M=="0"):
        M=sysItems['UIDevice']
       
    value=int(value)
    #Turning it on involves keeping current pump directions,
    if (value and (sysData[M]['Experiment']['ON']==0)):
        
        sysData[M]['Experiment']['ON']=1
        addTerminal(M,'Experiment Started')
        
        if (sysData[M]['Experiment']['cycles']==0):
            now=datetime.now()
            timeString=now.strftime("%Y-%m-%d %H:%M:%S")
            sysData[M]['Experiment']['startTime']=timeString
            sysData[M]['Experiment']['startTimeRaw']=now
        
        sysData[M]['Pump1']['direction']=1.0 #Sets pumps to go forward.
        sysData[M]['Pump2']['direction']=1.0

        turnEverythingOff(M)
        
        SetOutputOn(M,'Thermostat',1)
        sysDevices[M]['Experiment']=Thread(target = runExperiment, args=(M,'placeholder'))
        sysDevices[M]['Experiment'].setDaemon(True)
        sysDevices[M]['Experiment'].start();
        
    else:
        sysData[M]['Experiment']['ON']=0
        sysData[M]['OD']['ON']=0
        addTerminal(M,'Experiment Stopping at end of cycle')
        SetOutputOn(M,'Pump1',0)
        SetOutputOn(M,'Pump2',0)
        SetOutputOn(M,'Stir',0)
        SetOutputOn(M,'Thermostat',0)
        
    return ('', 204)