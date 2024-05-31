# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('template', views.template, name='template'),
    path('getSysdata/', views.getSysdata, name='getSysdata'),
    # DEVICES FUNCTIONS
    path('scanDevices/<str:which>/', views.scanDevices_view, name='scanDevices'),
    path('changeDevice/<str:wich>/', views.changeDevice_view, name='changeDevice'),
    path('CharacteriseDevice/<str:M>/<str:Program>', views.CharacteriseDevice_view, name='CharacteriseDevice'),
    # -------------------------------------------------------------------------------------------------
    # TERMINAL FUNCTIONS
    path('clearTerminal/<str:M>', views.clearTerminal_view, name='clearTerminal'),
    # -------------------------------------------------------------------------------------------------
    # FP MEASUREMENT FUNCTIONS
    path('SetFPMeasurement/<str:item>/<str:Excite>/<str:Base>/<str:Emit1>/<str:Emit2>/<str:Gain>/',
             views.SetFPMeasurement_view, name='SetFPMeasurement'),
    path('MeasureFP/<str:M>', views.MeasureFP_view, name='MeasureFP'),
    # -------------------------------------------------------------------------------------------------
    # SETUP FUNCTIONS
    path('SetOutputOn/<str:item>/<str:force>/<str:M>', views.SetOutputOn_view, name='SetOutputOn'),
    path('SetOutputTarget/<str:item>/<str:M>/<str:value>', views.SetOutputTarget_view, name='SetOutputTarget'),
    # -------------------------------------------------------------------------------------------------
    # DIRECTIONS
    path('Direction/<str:item>/<str:M>', views.Direction_view, name='Direction'),
    # -------------------------------------------------------------------------------------------------
    # SPECTRUM FUNCTIONS
    path('GetSpectrum/<str:Gain>/<str:M>', views.GetSpectrum_view, name='GetSpectrum'),
    # -------------------------------------------------------------------------------------------------
    # CUSTOM FUNCTIONS
    path('SetCustom/<str:Program>/<str:Status>', views.SetCustom_view, name='SetCustom'),
    # -------------------------------------------------------------------------------------------------
    # LIGHT ACTUATION FUNCTIONS
    path('SetLightActuation/<str:Excite>', views.SetLightActuation_view, name='SetLightActuation'),
    # -------------------------------------------------------------------------------------------------
    # OD FUNCTIONS
    path('CalibrateOD/<str:item>/<str:M>/<str:value>/<str:value2>', views.CalibrateOD_view, name='CalibrateOD'),
    path('MeasureOD/<str:M>', views.MeasureOD_view, name='MeasureOD'),
    # -------------------------------------------------------------------------------------------------
    # TEMPERATURE FUNCTIONS
    path('MeasureTemp/<str:which>/<str:M>', views.MeasureTemp_view, name='MeasureTemp'),
    # -------------------------------------------------------------------------------------------------
    path('ExperimentReset/', views.ExperimentReset_view, name='ExperimentReset'),
    path('Experiment/<str:value>/<str:M>', views.ExperimentStartStop_view, name='Experiment'),
]
