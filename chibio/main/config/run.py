from .setup import *
from .controls import *

def runExperiment(M,placeholder):
    #Primary function for running an automated experiment.
    M=str(M)
   
    global sysData
    global sysItems
    global sysDevices
    
    sysData[M]['Experiment']['threadCount']=(sysData[M]['Experiment']['threadCount']+1)%100
    currentThread=sysData[M]['Experiment']['threadCount']
        
    # Get time running in seconds
    now=datetime.now()
    elapsedTime=now-sysData[M]['Experiment']['startTimeRaw']
    elapsedTimeSeconds=round(elapsedTime.total_seconds(),2)
    sysData[M]['Experiment']['cycles']=sysData[M]['Experiment']['cycles']+1
    addTerminal(M,'Cycle ' + str(sysData[M]['Experiment']['cycles']) + ' Started')
    CycleTime=sysData[M]['Experiment']['cycleTime']

    SetOutputOn(M,'Stir',0) #Turning stirring off
    time.sleep(5.0) #Wait for liquid to settle.
    if (sysData[M]['Experiment']['ON']==0):
        turnEverythingOff(M)
        sysData[M]['Experiment']['cycles']=sysData[M]['Experiment']['cycles']-1 # Cycle didn't finish, don't count it.
        addTerminal(M,'Experiment Stopped')
        return
    
    sysData[M]['OD']['Measuring']=1 #Begin measuring - this flag is just to indicate that a measurement is currently being taken.
    
    #We now meausre OD 4 times and take the average to reduce noise when in auto mode!
    ODV=0.0
    for i in [0, 1, 2, 3]:
        MeasureOD(M)
        ODV=ODV+sysData[M]['OD']['current']
        time.sleep(0.25)
    sysData[M]['OD']['current']=ODV/4.0
    
    MeasureTemp(M,'Internal') #Measuring all temperatures
    MeasureTemp(M,'External')
    MeasureTemp(M,'IR')
    MeasureFP(M) #And now fluorescent protein concentrations. 
	
    if (sysData[M]['Experiment']['ON']==0): #We do another check post-measurement to see whether we need to end the experiment.
        turnEverythingOff(M)
        sysData[M]['Experiment']['cycles']=sysData[M]['Experiment']['cycles']-1 # Cycle didn't finish, don't count it.
        addTerminal(M,'Experiment Stopped')
        return
    #Temporary Biofilm Section - the below makes the device all spectral data for all LEDs each cycle.
    
    # bands=['nm410' ,'nm440','nm470','nm510','nm550','nm583','nm620','nm670','CLEAR','NIR']    
    # items= ['LEDA','LEDB','LEDC','LEDD','LEDE','LEDF','LEDG','LASER650']
    # gains=['x10','x10','x10','x10','x10','x10','x10','x1']
    # gi=-1
    # for item in items:
    #     gi=gi+1
    #     SetOutputOn(M,item,1)
    #     GetSpectrum(M,gains[gi])
    #     SetOutputOn(M,item,0)
    #     for band in bands:
    #         sysData[M]['biofilm'][item][band]=int(sysData[M]['AS7341']['spectrum'][band])

    sysData[M]['OD']['Measuring']=0
    if (sysData[M]['OD']['ON']==1):
        RegulateOD(M) #Function that calculates new target pump rates, and sets pumps to desired rates. 
    
    LightActuation(M,1) 
    
    if (sysData[M]['Custom']['ON']==1): #Check if we have enabled custom programs
        CustomThread=Thread(target = CustomProgram, args=(M,)) #We run this in a thread in case we are doing something slow, we dont want to hang up the main l00p. The comma after M is to cast the args as a tuple to prevent it iterating over the thread M
        CustomThread.setDaemon(True)
        CustomThread.start();

    
    Pump2Ontime=sysData[M]['Experiment']['cycleTime']*1.05*abs(sysData[M]['Pump2']['target'])*sysData[M]['Pump2']['ON']+0.5 #The amount of time Pump2 is going to be on for following RegulateOD above.
    time.sleep(Pump2Ontime) #Pause here is to prevent output pumping happening at the same time as stirring.
    
    SetOutputOn(M,'Stir',1) #Start stirring again.

    if(sysData[M]['Experiment']['cycles']%10==9): #Dont want terminal getting unruly, so clear it each 10 rotations.
        clearTerminal(M)
    
    #######Below stores all the results for plotting later
    sysData[M]['time']['record'].append(elapsedTimeSeconds)
    sysData[M]['OD']['record'].append(sysData[M]['OD']['current'])
    sysData[M]['OD']['targetrecord'].append( sysData[M]['OD']['target']*sysData[M]['OD']['ON'])
    sysData[M]['Thermostat']['record'].append(sysData[M]['Thermostat']['target']*float(sysData[M]['Thermostat']['ON']))
    sysData[M]['Light']['record'].append(float(sysData[M]['Light']['ON']))
    sysData[M]['ThermometerInternal']['record'].append(sysData[M]['ThermometerInternal']['current'])
    sysData[M]['ThermometerExternal']['record'].append(sysData[M]['ThermometerExternal']['current'])
    sysData[M]['ThermometerIR']['record'].append(sysData[M]['ThermometerIR']['current'])
    sysData[M]['Pump1']['record'].append(sysData[M]['Pump1']['target']*float(sysData[M]['Pump1']['ON']))
    sysData[M]['Pump2']['record'].append(sysData[M]['Pump2']['target']*float(sysData[M]['Pump2']['ON']))
    sysData[M]['Pump3']['record'].append(sysData[M]['Pump3']['target']*float(sysData[M]['Pump3']['ON']))
    sysData[M]['Pump4']['record'].append(sysData[M]['Pump4']['target']*float(sysData[M]['Pump4']['ON']))
    sysData[M]['GrowthRate']['record'].append(sysData[M]['GrowthRate']['current']*float(sysData[M]['Zigzag']['ON']))
    for FP in ['FP1','FP2','FP3']:
        if sysData[M][FP]['ON']==1:
            sysData[M][FP]['BaseRecord'].append(sysData[M][FP]['Base'])
            sysData[M][FP]['Emit1Record'].append(sysData[M][FP]['Emit1'])
            if (sysData[M][FP]['Emit2Band']!= "OFF"):
                sysData[M][FP]['Emit2Record'].append(sysData[M][FP]['Emit2'])
            else:
                sysData[M][FP]['Emit2Record'].append(0.0)
        else:
            sysData[M][FP]['BaseRecord'].append(0.0)
            sysData[M][FP]['Emit1Record'].append(0.0)
            sysData[M][FP]['Emit2Record'].append(0.0)
    
    #We  downsample our records such that the size of the data vectors being plot in the web interface does not get unruly. 
    if (len(sysData[M]['time']['record'])>200):
        downsample(M)

    #### Writing Results to data file
    csvData(M) #This command writes system data to a CSV file for future keeping.
    #And intermittently write the setup parameters to a data file. 
    if(sysData[M]['Experiment']['cycles']%10==1): #We only write whole configuration file each 10 cycles since it is not really that important. 
        TempStartTime=sysData[M]['Experiment']['startTimeRaw']
        sysData[M]['Experiment']['startTimeRaw']=0 #We had to set this to zero during the write operation since the system does not like writing data in such a format.
        
        filename = sysData[M]['Experiment']['startTime'] + '_' + M + '.txt'
        filename=filename.replace(":","_")
        f = open(filename,'w')
        simplejson.dump(sysData[M],f)
        f.close()
        sysData[M]['Experiment']['startTimeRaw']=TempStartTime
    ##### Written

    if (sysData[M]['Experiment']['ON']==0):
        turnEverythingOff(M)
        addTerminal(M,'Experiment Stopped')
        return
    
    nowend=datetime.now()
    elapsedTime2=nowend-now
    elapsedTimeSeconds2=round(elapsedTime2.total_seconds(),2)
    sleeptime=CycleTime-elapsedTimeSeconds2
    if (sleeptime<0):
        sleeptime=0
        addTerminal(M,'Experiment Cycle Time is too short!!!')    
        
    time.sleep(sleeptime)
    LightActuation(M,0) #Turn light actuation off if it is running.
    addTerminal(M,'Cycle ' + str(sysData[M]['Experiment']['cycles']) + ' Complete')

    #Now we run this function again if the automated experiment is still going.
    if (sysData[M]['Experiment']['ON'] and sysData[M]['Experiment']['threadCount']==currentThread):
        sysDevices[M]['Experiment']=Thread(target = runExperiment, args=(M,'placeholder'))
        sysDevices[M]['Experiment'].setDaemon(True)
        sysDevices[M]['Experiment'].start();
        
    else: 
        turnEverythingOff(M)
        addTerminal(M,'Experiment Stopped')