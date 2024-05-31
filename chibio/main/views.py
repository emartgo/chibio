from django.shortcuts import render
from .config.sys import *
from django.http import JsonResponse

from .config.setup import *
from .config.controls import *
from .config.custom import *
from .config.init import *

initialiseAll()
print(str(datetime.now()) + ' Start Up Complete')

def index(request):
    #Function responsible for sending appropriate device's data to user interface. 
    outputdata=sysData[sysItems['UIDevice']]
    for M in ['M0','M1','M2','M3','M4','M5','M6','M7']:
            if sysData[M]['present']==1:
                outputdata['presentDevices'][M]=1
            else:
                outputdata['presentDevices'][M]=0

    return render(request, 'main/index.html', outputdata)

def getSysdata(request):
    outputdata = sysData[sysItems['UIDevice']]
    outputdata['presentDevices'] = {}
    for M in ['M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7']:
        if sysData[M]['present'] == 1:
            outputdata['presentDevices'][M] = 1
        else:
            outputdata['presentDevices'][M] = 0
    return JsonResponse(outputdata)

# DEVICES FUNCTIONS
# These functions are responsible for scanning devices and changing the selected device in the UI.
# -------------------------------------------------------------------------------------------------
def scanDevices_view(request, which):
    #Scans to decide which devices are plugged in/on. Does this by trying to communicate with their internal thermometers (if this communication failes, software assumes device is not present)
    try:
        scanDevices(which=which)
    except:
        return JsonResponse({'status': 'error'}, status=500)

    return JsonResponse({'status': 'success'}, status=204)

def changeDevice_view(request, which):
    #Function responsible for changin which device is selected in the UI.
    try:
        changeDevice(which=which)
    except:
        return JsonResponse({'status': 'error'}, status=500)

    return JsonResponse({'status': 'success'}, status=204)

def CharacteriseDevice_view(request, M,Program): 
    # THis umbrella function is used to run the actual characteriseation function in a thread to prevent GUnicorn worker timeout.
    try:
        CharacteriseDevice(M,Program)
    except:
        return JsonResponse({'status': 'error'}, status=500)
    
    return JsonResponse({'status': 'success'}, status=204)
# -------------------------------------------------------------------------------------------------

# TERMINAL FUNCTIONS
# These functions are responsible for clearing the terminal.
# -------------------------------------------------------------------------------------------------
def clearTerminal_view(request, M):
    #Deletes everything from the terminal.
    try:
        clearTerminal(M)
    except:
        return JsonResponse({'status': 'error'}, status=500)
    
    return JsonResponse({'status': 'success'}, status=204)
# -------------------------------------------------------------------------------------------------

# FLUORESCENT PROTEIN FUNCTIONS
# These functions are responsible for setting up the fluorescent protein measurement.
# -------------------------------------------------------------------------------------------------
def SetFPMeasurement_view(request, item,Excite,Base,Emit1,Emit2,Gain):
    #Sets up the fluorescent protein measurement in terms of gain, and which LED / measurement bands to use.
    try:
        SetFPMeasurement(item,Excite,Base,Emit1,Emit2,Gain)
    except:
        return JsonResponse({'status': 'error'}, status=500)
    
    return JsonResponse({'status': 'success'}, status=204)

def MeasureFP_view(request, M):
    #Responsible for measuring each of the active Fluorescent proteins.
    try:
        MeasureFP(M)
    except:
        return JsonResponse({'status': 'error'}, status=500)
    
    return JsonResponse({'status': 'success'}, status=204)
# -------------------------------------------------------------------------------------------------

# SETUP FUNCTIONS
# These functions are responsible for setting up the output target.
# -------------------------------------------------------------------------------------------------
def SetOutputOn_view(request, M,item,force):
    #General function used to switch an output on or off.
    try:
        SetOutputOn(M,item,force)
    except:
        return JsonResponse({'status': 'error'}, status=500)

    return JsonResponse({'status': 'success'}, status=204)
    
def SetOutputTarget_view(request, M,item, value):
    #General function used to set the output level of a particular item, ensuring it is within an acceptable range.
    try:
        SetOutputTarget(M,item, value)
    except:
        return JsonResponse({'status': 'error'}, status=500)

    return JsonResponse({'status': 'success'}, status=204)  
# -------------------------------------------------------------------------------------------------

# DIRECTIONS
# These functions are responsible for changing the direction of a pump.
# -------------------------------------------------------------------------------------------------
def direction_view(request, M,item):
    #Flips direction of a pump.
    try:
        direction(M,item)
    except:
        return JsonResponse({'status': 'error'}, status=500)
    
    return JsonResponse({'status': 'success'}, status=204)
# -------------------------------------------------------------------------------------------------

# SPECTRUM FUNCTIONS
# These functions are responsible for getting the spectrum.
# -------------------------------------------------------------------------------------------------
def GetSpectrum_view(request, M,Gain):
    #Measures entire spectrum, i.e. every different photodiode, which requires 2 measurement shots. 
    try:
        GetSpectrum(M,Gain)
    except:
        return JsonResponse({'status': 'error'}, status=500)
    
    return JsonResponse({'status': 'success'}, status=204)
# -------------------------------------------------------------------------------------------------

# CUSTOM FUNCTIONS
# These functions are responsible for setting up custom programs.
# -------------------------------------------------------------------------------------------------
def SetCustom_view(request, Program,Status):
    #Turns a custom program on/off.
    try:
        SetCustom(Program,Status)
    except:
        return JsonResponse({'status': 'error'}, status=500)
    
    return JsonResponse({'status': 'success'}, status=204)
# -------------------------------------------------------------------------------------------------

# LIGHT ACTUATION FUNCTIONS
# These functions are responsible for setting up the light actuation.
# -------------------------------------------------------------------------------------------------
def SetLightActuation_view(request, Excite):
    #Basic function used to set which LED is used for optogenetics.
    try:
        SetLightActuation(Excite)
    except:
        return JsonResponse({'status': 'error'}, status=500)
    
    return JsonResponse({'status': 'success'}, status=204)
# -------------------------------------------------------------------------------------------------

# OD FUNCTIONS
# These functions are responsible for calibrating and measuring OD.
# -------------------------------------------------------------------------------------------------
def CalibrateOD_view(request, M,item,value,value2):
    #Used to calculate calibration value for OD measurements.
    try:
        CalibrateOD(M,item,value,value2)
    except:
        return JsonResponse({'status': 'error'}, status=500)
    
    return JsonResponse({'status': 'success'}, status=204)

def MeasureOD_view(request, M):
    #Measures laser transmission and calculates calibrated OD from this.
    try:
        MeasureOD(M)
    except:
        return JsonResponse({'status': 'error'}, status=500)
    
    return JsonResponse({'status': 'success'}, status=204)
# -------------------------------------------------------------------------------------------------

# TEMPERATURE FUNCTIONS
# These functions are responsible for measuring temperature.
# -------------------------------------------------------------------------------------------------
def MeasureTemp_view(request, M,which): 
    #Used to measure temperature from each thermometer.
    try:
        MeasureTemp(M,which)
    except:
        return JsonResponse({'status': 'error'}, status=500)
    
    return JsonResponse({'status': 'success'}, status=204)
# -------------------------------------------------------------------------------------------------

# EXPERIMENT FUNCTIONS
# These functions are responsible for setting up and running experiments.
# -------------------------------------------------------------------------------------------------
def ExperimentReset_view(request):
    #Resets parameters/values of a given experiment.
    try:
        ExperimentReset()
    except:
        return JsonResponse({'status': 'error'}, status=500)
    
    return JsonResponse({'status': 'success'}, status=204)

def ExperimentStartStop_view(request, M,value):
    #Stops or starts an experiment. 
    try:
        ExperimentStartStop(M,value)
    except:
        return JsonResponse({'status': 'error'}, status=500)
    
    return JsonResponse({'status': 'success'}, status=204)
# -------------------------------------------------------------------------------------------------

