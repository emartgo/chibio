from .sys import *
from .setup import *
from .controls import *
import csv
import simplejson

def SetCustom(Program,Status):
    #Turns a custom program on/off.
	
    global sysData
    M=sysItems['UIDevice']
    item="Custom"
    if sysData[M][item]['ON']==1:
        sysData[M][item]['ON']=0
    else:
        sysData[M][item]['Program']=str(Program)
        sysData[M][item]['Status']=float(Status)
        sysData[M][item]['ON']=1
        sysData[M][item]['param1']=0.0 #Thus parameters get reset each time you restart your program.
        sysData[M][item]['param2']=0.0
        sysData[M][item]['param3']=0.0
    return('',204)
		
        
def CustomProgram(M):
    #Runs a custom program, some examples are included. You can remove/edit this function as you see fit.
    #Note that the custom programs (as set up at present) use an external .csv file with input parameters. THis is done to allow these parameters to easily be varied on the fly. 
    global sysData
    M=str(M)
    program=sysData[M]['Custom']['Program']
    #Subsequent few lines reads in external parameters from a file if you are using any.
    fname='InputParameters_' + str(M)+'.csv'
	
    with open(fname, 'rb') as f:
        reader = csv.reader(f)
        listin = list(reader)
    Params=listin[0]
    addTerminal(M,'Running Program = ' + str(program) + ' on device ' + str(M))
	
	
    if (program=="C1"): #Optogenetic Integral Control Program
        integral=0.0 #Integral in integral controller
        green=0.0 #Intensity of Green actuation 
        red=0.0 #Intensity of red actuation.
        GFPNow=sysData[M]['FP1']['Emit1']
        GFPTarget=sysData[M]['Custom']['Status'] #This is the controller setpoint.
        error=GFPTarget-GFPNow
        if error>0.0075:
            green=1.0
            red=0.0
            sysData[M]['Custom']['param3']=0.0 
        elif error<-0.0075:
            green=0.0
            red=1.0
            sysData[M]['Custom']['param3']=0.0
        else:
            red=1.0
            balance=float(Params[0]) #our guess at green light level to get 50% expression.
            KI=float(Params[1])
            KP=float(Params[2])
            integral=sysData[M]['Custom']['param3']+error*KI
            green=balance+KP*error+integral
            sysData[M]['Custom']['param3']=integral
        

        GreenThread=Thread(target = CustomLEDCycle, args=(M,'LEDD',green))
        GreenThread.setDaemon(True)
        GreenThread.start();
        RedThread=Thread(target = CustomLEDCycle, args=(M,'LEDF',red))
        RedThread.setDaemon(True)
        RedThread.start();
        sysData[M]['Custom']['param1']=green
        sysData[M]['Custom']['param2']=red
        addTerminal(M,'Program = ' + str(program) + ' green= ' + str(green)+ ' red= ' + str(red) + ' integral= ' + str(integral))
	
    elif (program=="C2"): #UV Integral Control Program
        integral=0.0 #Integral in integral controller
        UV=0.0 #Intensity of Green actuation 
        GrowthRate=sysData[M]['GrowthRate']['current']
        GrowthTarget=sysData[M]['Custom']['Status'] #This is the controller setpoint.
        error=GrowthTarget-GrowthRate
        KP=float(Params[0]) #Past data suggest value of ~0.005
        KI=float(Params[1]) #Past data suggest value of ~2e-5
        integral=sysData[M]['Custom']['param2']+error*KI
        if(integral>0):
            integral=0.0
        sysData[M]['Custom']['param2']=integral
        UV=-1.0*(KP*error+integral)
        sysData[M]['Custom']['param1']=UV
        SetOutputTarget(M,'UV',UV)
        SetOutputOn(M,'UV',1)
        addTerminal(M,'Program = ' + str(program) + ' UV= ' + str(UV)+  ' integral= ' + str(integral))
        
    elif (program=="C3"): #UV Integral Control Program Mk 2
        integral=sysData[M]['Custom']['param2'] #Integral in integral controller
        integral2=sysData[M]['Custom']['param3'] #Second integral controller
        UV=0.0 #Intensity of UV
        GrowthRate=sysData[M]['GrowthRate']['current']
        GrowthTarget=sysData[M]['Custom']['Status'] #This is the controller setpoint.
        error=GrowthTarget-GrowthRate
        KP=float(Params[0]) #Past data suggest value of ~0.005
        KI=float(Params[1]) #Past data suggest value of ~2e-5
        KI2=float(Params[2])
        integral=sysData[M]['Custom']['param2']+error*KI
        if(integral>0):
            integral=0.0
            
        if(abs(error)<0.3): #This is a second high-gain integrator which only gets cranking along when we are close to the target.
            integral2=sysData[M]['Custom']['param3']+error*KI2
        if(integral2>0):
            integral2=0.0
            
        sysData[M]['Custom']['param2']=integral
        sysData[M]['Custom']['param3']=integral2
        UV=-1.0*(KP*error+integral+integral2)
        m=50.0
        UV=(1.0/m)*(math.exp(m*UV)-1.0) #Basically this is to force the UV level to increase exponentially!
        sysData[M]['Custom']['param1']=UV
        SetOutputTarget(M,'UV',UV)
        SetOutputOn(M,'UV',1)
        addTerminal(M,'Program = ' + str(program) + ' UV= ' + str(UV)+  ' integral= ' + str(integral))
    elif (program=="C4"): #UV Integral Control Program Mk 4
        rategain=float(Params[0]) 
        timept=sysData[M]['Custom']['Status'] #This is the timestep as we follow in minutes
        
        UV=0.001*math.exp(timept*rategain) #So we just exponentialy increase UV over time!
        sysData[M]['Custom']['param1']=UV
        SetOutputTarget(M,'UV',UV)
        SetOutputOn(M,'UV',1)
        
        timept=timept+1
        sysData[M]['Custom']['Status']=timept
            
    elif (program=="C5"): #UV Dosing program
        timept=int(sysData[M]['Custom']['Status']) #This is the timestep as we follow in minutes
        sysData[M]['Custom']['Status']=timept+1 #Increment time as we have entered the loop another time!
        
        Pump2Ontime=sysData[M]['Experiment']['cycleTime']*1.05*abs(sysData[M]['Pump2']['target'])*sysData[M]['Pump2']['ON']+0.5 #The amount of time Pump2 is going to be on for following RegulateOD above.
        time.sleep(Pump2Ontime) #Pause here is to prevent output pumping happening at the same time as stirring.
        
        timelength=300 #Time between doses in minutes
        if(timept%timelength==2): #So this happens every 5 hours!
            iters=(timept//timelength)
            Dose0=float(Params[0])
            Dose=Dose0*(2.0**float(iters)) #UV Dose, in terms of amount of time UV shoudl be left on at 1.0 intensity.
            print(str(datetime.now()) + ' Gave dose ' + str(Dose) + " at iteration " + str(iters) + " on device " + str(M))
            
            if (Dose<30.0):  
                powerlvl=Dose/30.0
                SetOutputTarget(M,'UV',powerlvl)
                Dose=30.0
            else:    
                SetOutputTarget(M,'UV',1.0) #Ensure UV is on at aopropriate intensity
                
            SetOutputOn(M,'UV',1) #Activate UV
            time.sleep(Dose) #Wait for dose to be administered
            SetOutputOn(M,'UV',0) #Deactivate UV
            
    elif (program=="C6"): #UV Dosing program 2 - constant value!
        timept=int(sysData[M]['Custom']['Status']) #This is the timestep as we follow in minutes
        sysData[M]['Custom']['Status']=timept+1 #Increment time as we have entered the loop another time!
        
        Pump2Ontime=sysData[M]['Experiment']['cycleTime']*1.05*abs(sysData[M]['Pump2']['target'])*sysData[M]['Pump2']['ON']+0.5 #The amount of time Pump2 is going to be on for following RegulateOD above.
        time.sleep(Pump2Ontime) #Pause here is to prevent output pumping happening at the same time as stirring.
    
        timelength=300 #Time between doses in minutes
        if(timept%timelength==2): #So this happens every 5 hours!
            iters=(timept//timelength)
            if iters>3:
                iters=3
                
            Dose0=float(Params[0])
            Dose=Dose0*(2.0**float(iters)) #UV Dose, in terms of amount of time UV shoudl be left on at 1.0 intensity.
            print(str(datetime.now()) + ' Gave dose ' + str(Dose) + " at iteration " + str(iters) + " on device " + str(M))
              
            if (Dose<30.0):  
                powerlvl=Dose/30.0
                SetOutputTarget(M,'UV',powerlvl)
                Dose=30.0
            else:    
                SetOutputTarget(M,'UV',1.0) #Ensure UV is on at aopropriate intensity
            
            SetOutputOn(M,'UV',1) #Activate UV
            time.sleep(Dose) #Wait for dose to be administered
            SetOutputOn(M,'UV',0) #Deactivate UV
                
                
    
    return

def CustomLEDCycle(M,LED,Value):
    #This function cycles LEDs for a fraction of 30 seconds during an experiment.
    global sysData
    M=str(M)
    if (Value>1.0):
        Value=1.0
        
    if (Value>0.0):
        SetOutputOn(M,LED,1)
        time.sleep(Value*30.0) #Sleep whatever fraction of 30 seconds we are interested in
        SetOutputOn(M,LED,0)
        
    return  

def CharacteriseDevice(M,Program): 
    # THis umbrella function is used to run the actual characteriseation function in a thread to prevent GUnicorn worker timeout.
    Program=str(Program)
    if (Program=='C1'):
        cthread=Thread(target = CharacteriseDevice2, args=(M))
        cthread.setDaemon(True)
        cthread.start()
    
    return('',204)
        
        
        
def CharacteriseDevice2(M):
    global sysData
    global sysItems
    print('In1')
    M=str(M)
    if (M=="0"):
        M=sysItems['UIDevice']
        
    result= { 'LEDA' : {'nm410' : [],'nm440' : [],'nm470' : [],'nm510' : [],'nm550' : [],'nm583' : [],'nm620' : [],'nm670' : [],'CLEAR' : []},
        'LEDB' : {'nm410' : [],'nm440' : [],'nm470' : [],'nm510' : [],'nm550' : [],'nm583' : [],'nm620' : [],'nm670' : [],'CLEAR' : []},
        'LEDC' : {'nm410' : [],'nm440' : [],'nm470' : [],'nm510' : [],'nm550' : [],'nm583' : [],'nm620' : [],'nm670' : [],'CLEAR' : []},
        'LEDD' : {'nm410' : [],'nm440' : [],'nm470' : [],'nm510' : [],'nm550' : [],'nm583' : [],'nm620' : [],'nm670' : [],'CLEAR' : []},
        'LEDE' : {'nm410' : [],'nm440' : [],'nm470' : [],'nm510' : [],'nm550' : [],'nm583' : [],'nm620' : [],'nm670' : [],'CLEAR' : []},
        'LEDF' : {'nm410' : [],'nm440' : [],'nm470' : [],'nm510' : [],'nm550' : [],'nm583' : [],'nm620' : [],'nm670' : [],'CLEAR' : []},
        'LEDG' : {'nm410' : [],'nm440' : [],'nm470' : [],'nm510' : [],'nm550' : [],'nm583' : [],'nm620' : [],'nm670' : [],'CLEAR' : []},
        'LASER650' : {'nm410' : [],'nm440' : [],'nm470' : [],'nm510' : [],'nm550' : [],'nm583' : [],'nm620' : [],'nm670' : [],'CLEAR' : []},
        }
        
        
    print('Got in!')   
    bands=['nm410' ,'nm440','nm470','nm510','nm550','nm583','nm620','nm670','CLEAR']    
    powerlevels=[0,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    items= ['LEDA','LEDB','LEDC','LEDD','LEDE','LEDF','LEDG','LASER650']
    gains=['x4','x4','x4','x4','x4','x4','x4','x1']
    gi=-1
    for item in items:
        gi=gi+1
        for power in powerlevels:
            SetOutputTarget(M,item,power)
            SetOutputOn(M,item,1)
            GetSpectrum(M,gains[gi])
            SetOutputOn(M,item,0)
            print(item + ' ' + str(power))
            for band in bands:
                result[item][band].append(int(sysData[M]['AS7341']['spectrum'][band]))
            addTerminal(M,'Measured Item = ' + str(item) + ' at power ' + str(power))
            time.sleep(0.05)
                
    
    filename = 'characterisation_data_' + M + '.txt'
    f = open(filename,'w')
    simplejson.dump(result,f)
    f.close()
    return