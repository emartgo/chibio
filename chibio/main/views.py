from django.shortcuts import render
from .config.sys import *
from django.http import JsonResponse

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
