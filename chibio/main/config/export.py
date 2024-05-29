from .sys import sysData,lock
import numpy as np
import csv
import os

def csvData(M):
    #Used to format current data and write a new row to CSV file output. Note if you want to record any additional parameters/measurements then they need to be added to this function.
    global sysData
    M=str(M)

    fieldnames = ['exp_time','od_measured','od_setpoint','od_zero_setpoint','thermostat_setpoint','heating_rate',
                  'internal_air_temp','external_air_temp','media_temp','opt_gen_act_int','pump_1_rate','pump_2_rate',
                  'pump_3_rate','pump_4_rate','media_vol','stirring_rate','LED_395nm_setpoint','LED_457nm_setpoint',
                  'LED_500nm_setpoint','LED_523nm_setpoint','LED_595nm_setpoint','LED_623nm_setpoint',
                  'LED_6500K_setpoint','laser_setpoint','LED_UV_int','FP1_base','FP1_emit1','FP1_emit2','FP2_base',
                  'FP2_emit1','FP2_emit2','FP3_base','FP3_emit1','FP3_emit2','custom_prog_param1','custom_prog_param2',
                  'custom_prog_param3','custom_prog_status','zigzag_target','growth_rate']

    row=[sysData[M]['time']['record'][-1],
        sysData[M]['OD']['record'][-1],
        sysData[M]['OD']['targetrecord'][-1],
        sysData[M]['OD0']['target'],
        sysData[M]['Thermostat']['record'][-1],
        sysData[M]['Heat']['target']*float(sysData[M]['Heat']['ON']),
        sysData[M]['ThermometerInternal']['record'][-1],
        sysData[M]['ThermometerExternal']['record'][-1],
        sysData[M]['ThermometerIR']['record'][-1],
        sysData[M]['Light']['record'][-1],
        sysData[M]['Pump1']['record'][-1],
        sysData[M]['Pump2']['record'][-1],
        sysData[M]['Pump3']['record'][-1],
        sysData[M]['Pump4']['record'][-1],
        sysData[M]['Volume']['target'],
        sysData[M]['Stir']['target']*sysData[M]['Stir']['ON'],]
    for LED in ['LEDA','LEDB','LEDC','LEDD','LEDE','LEDF','LEDG','LEDH','LEDI','LEDV','LASER650']:
        row=row+[sysData[M][LED]['target']]
    row=row+[sysData[M]['UV']['target']*sysData[M]['UV']['ON']]
    for FP in ['FP1','FP2','FP3']:
        if sysData[M][FP]['ON']==1:
            row=row+[sysData[M][FP]['Base']]
            row=row+[sysData[M][FP]['Emit1']]
            row=row+[sysData[M][FP]['Emit2']]
        else:
            row=row+([0.0, 0.0, 0.0])
    
    row=row+[sysData[M]['Custom']['param1']*float(sysData[M]['Custom']['ON'])]
    row=row+[sysData[M]['Custom']['param2']*float(sysData[M]['Custom']['ON'])]
    row=row+[sysData[M]['Custom']['param3']*float(sysData[M]['Custom']['ON'])]
    row=row+[sysData[M]['Custom']['Status']*float(sysData[M]['Custom']['ON'])]
    row=row+[sysData[M]['Zigzag']['target']*float(sysData[M]['Zigzag']['ON'])]
    row=row+[sysData[M]['GrowthRate']['current']*sysData[M]['Zigzag']['ON']]
    
   
	#Following can be uncommented if you are recording ALL spectra for e.g. biofilm experiments
    #bands=['nm410' ,'nm440','nm470','nm510','nm550','nm583','nm620','nm670','CLEAR','NIR']    
    #items= ['LEDA','LEDB','LEDC','LEDD','LEDE','LEDF','LEDG','LASER650']
    #for item in items:
    #   for band in bands:
    #       row=row+[sysData[M]['biofilm'][item][band]]



    filename = sysData[M]['Experiment']['startTime'] + '_' + M + '_data' + '.csv'
    filename=filename.replace(":","_")

    lock.acquire() #We are avoiding writing to a file at the same time as we do digital communications, since it might potentially cause the computer to lag and consequently data transfer to fail.
    if os.path.isfile(filename) is False: #Only if we are starting a fresh file
        if (len(row) == len(fieldnames)):  #AND the fieldnames match up with what is being written.
            with open(filename, 'a') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(fieldnames)
        else:
            print('CSV_WRITER: mismatch between column num and header num')

    with open(filename, 'a') as csvFile: # Here we append the new data to our CSV file.
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()        
    lock.release() 
    
def downsample(M):
    #In order to prevent the UI getting too laggy, we downsample the stored data every few hours. Note that this doesnt downsample that which has already been written to CSV, so no data is ever lost.
    global sysData
    M=str(M)
    
    
    
    
    #We now generate a new time vector which is downsampled at half the rate of the previous one
    time=np.asarray(sysData[M]['time']['record'])
    newlength=int(round(len(time)/2,2)-1)
    tnew=np.linspace(time[0],time[-11],newlength)
    tnew=np.concatenate([tnew,time[-10:]])
    
    #In the following we make a new array, index, which has the indices at which we want to resample our existing data vectors.
    i=0
    index=np.zeros((len(tnew),),dtype=int)
    for timeval in tnew:
        idx = np.searchsorted(time, timeval, side="left")
        if idx > 0 and (idx == len(time) or np.abs(timeval - time[idx-1]) < np.abs(timeval - time[idx])):
            index[i]=idx-1
        else:
            index[i]=idx
        i=i+1
    
 
    sysData[M]['time']['record']=downsampleFunc(sysData[M]['time']['record'],index)
    sysData[M]['OD']['record']=downsampleFunc(sysData[M]['OD']['record'],index)
    sysData[M]['OD']['targetrecord']=downsampleFunc(sysData[M]['OD']['targetrecord'],index)
    sysData[M]['Thermostat']['record']=downsampleFunc(sysData[M]['Thermostat']['record'],index)
    sysData[M]['Light']['record']=downsampleFunc(sysData[M]['Light']['record'],index)
    sysData[M]['ThermometerInternal']['record']=downsampleFunc(sysData[M]['ThermometerInternal']['record'],index)
    sysData[M]['ThermometerExternal']['record']=downsampleFunc(sysData[M]['ThermometerExternal']['record'],index)
    sysData[M]['ThermometerIR']['record']=downsampleFunc(sysData[M]['ThermometerIR']['record'],index)
    sysData[M]['Pump1']['record']=downsampleFunc(sysData[M]['Pump1']['record'],index)
    sysData[M]['Pump2']['record']=downsampleFunc(sysData[M]['Pump2']['record'],index)
    sysData[M]['Pump3']['record']=downsampleFunc(sysData[M]['Pump3']['record'],index)
    sysData[M]['Pump4']['record']=downsampleFunc(sysData[M]['Pump4']['record'],index)
    sysData[M]['GrowthRate']['record']=downsampleFunc(sysData[M]['GrowthRate']['record'],index)
    
        
    for FP in ['FP1','FP2','FP3']:
        sysData[M][FP]['BaseRecord']=downsampleFunc(sysData[M][FP]['BaseRecord'],index)
        sysData[M][FP]['Emit1Record']=downsampleFunc(sysData[M][FP]['Emit1Record'],index)
        sysData[M][FP]['Emit2Record']=downsampleFunc(sysData[M][FP]['Emit2Record'],index)
        
def downsampleFunc(datain,index):
    #This function Is used to downsample the arrays, taking the points selected by the index vector.
    datain=list(datain)
    newdata=[]
    newdata=np.zeros((len(index),),dtype=float)

    i=0
    for loc in list(index):
        newdata[i]=datain[int(loc)]
        
        i=i+1
    return list(newdata)