# Funciones para cargar datos JSON
from django.conf import settings
import json
import copy
import os

def load_sysdata():
    file_path = os.path.join(settings.BASE_DIR, 'main', 'config', 'json', 'sysdata.json')
    with open(file_path, 'r') as file:
        data = json.load(file)
    for M in ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7']:
        data[M] = copy.deepcopy(data['M0'])
    return data

def load_sysdevices():
    file_path = os.path.join(settings.BASE_DIR, 'main', 'config', 'json', 'sysdevices.json')
    with open(file_path, 'r') as file:
        data = json.load(file)
    for M in ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7']:
        data[M] = copy.deepcopy(data['M0'])
    return data

def load_sysitems():
    file_path = os.path.join(settings.BASE_DIR, 'main', 'config', 'json', 'sysitems.json')
    with open(file_path, 'r') as file:
        return json.load(file)

# Variables globales para almacenar los datos
sysData = load_sysdata()
sysDevices = load_sysdevices()
sysItems = load_sysitems()