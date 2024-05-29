$(function() {
    $('#ClearTerminal').click(function(){
     
       $.ajax({
           type:'POST',
        url: '/ClearTerminal/0',
         success:function(response){ 
             getSysData();
         }
     }); 
     })
});

$(function() {
    $('#ExperimentStart').click(function(){
      
       $.ajax({
        type:'POST',
        url: '/Experiment/1/0',
         success:function(response){ 
             getSysData();
         }
    }); 

    })
});

$(function() {
    $('#ExperimentStop').click(function(){
     
       $.ajax({
           type:'POST',
        url: '/Experiment/0/0',
         success:function(response){ 
             getSysData();
         }
     }); 
     })
});

$(function() {
    $('#ExperimentReset').click(function(){
     
       $.ajax({
           type:'POST',
        url: '/ExperimentReset',
         success:function(response){ 
             getSysData();
         }
     }); 
     })
});

$(function() {
    $('#ODRegulate').click(function(){
       
       var targetURL = '/SetOutputOn/OD/2/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#Zigzag').click(function(){
       
       var targetURL = '/SetOutputOn/Zigzag/2/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#LEDASet').click(function(){
      var value = $('#LEDAInput').val();
      var targetURL = '/SetOutputTarget/LEDA/0/' + value;
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#LEDASwitch').click(function(){
       
       var targetURL = '/SetOutputOn/LEDA/2/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#LEDBSet').click(function(){
      var value = $('#LEDBInput').val();
      var targetURL = '/SetOutputTarget/LEDB/0/' + value;
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#LEDBSwitch').click(function(){
       
       var targetURL = '/SetOutputOn/LEDB/2/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#LEDCSet').click(function(){
      var value = $('#LEDCInput').val();
      var targetURL = '/SetOutputTarget/LEDC/0/' + value;
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#LEDCSwitch').click(function(){
       
       var targetURL = '/SetOutputOn/LEDC/2/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});   

$(function() {
    $('#LEDDSet').click(function(){
      var value = $('#LEDDInput').val();
      var targetURL = '/SetOutputTarget/LEDD/0/' + value;
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#LEDDSwitch').click(function(){
       
       var targetURL = '/SetOutputOn/LEDD/2/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#LEDESet').click(function(){
      var value = $('#LEDEInput').val();
      var targetURL = '/SetOutputTarget/LEDE/0/' + value;
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#LEDESwitch').click(function(){
       
       var targetURL = '/SetOutputOn/LEDE/2/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#LEDFSet').click(function(){
      var value = $('#LEDFInput').val();
      var targetURL = '/SetOutputTarget/LEDF/0/' + value;
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#LEDFSwitch').click(function(){
       
       var targetURL = '/SetOutputOn/LEDF/2/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#LEDGSet').click(function(){
      var value = $('#LEDGInput').val();
      var targetURL = '/SetOutputTarget/LEDG/0/' + value;
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#LEDGSwitch').click(function(){
       
       var targetURL = '/SetOutputOn/LEDG/2/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
$('#LEDHSet').click(function(){
  var value = $('#LEDHInput').val();
  var targetURL = '/SetOutputTarget/LEDH/0/' + value;
   $.ajax({
       type:'POST',
       url: targetURL,
       success:function(response){ 
       getSysData();
     }
 }); 
 })
});

$(function() {
$('#LEDHSwitch').click(function(){
   
   var targetURL = '/SetOutputOn/LEDH/2/0';
   $.ajax({
       type:'POST',
       url: targetURL,
       success:function(response){ 
       getSysData();
     }
 }); 
 })
});

$(function() {
$('#LEDISet').click(function(){
  var value = $('#LEDIInput').val();
  var targetURL = '/SetOutputTarget/LEDI/0/' + value;
   $.ajax({
       type:'POST',
       url: targetURL,
       success:function(response){ 
       getSysData();
     }
 }); 
 })
});

$(function() {
$('#LEDISwitch').click(function(){
   
   var targetURL = '/SetOutputOn/LEDI/2/0';
   $.ajax({
       type:'POST',
       url: targetURL,
       success:function(response){ 
       getSysData();
     }
 }); 
 })
});

$(function() {
$('#LEDVSet').click(function(){
  var value = $('#LEDVInput').val();
  var targetURL = '/SetOutputTarget/LEDV/0/' + value;
   $.ajax({
       type:'POST',
       url: targetURL,
       success:function(response){ 
       getSysData();
     }
 }); 
 })
});

$(function() {
$('#LEDVSwitch').click(function(){
   
   var targetURL = '/SetOutputOn/LEDV/2/0';
   $.ajax({
       type:'POST',
       url: targetURL,
       success:function(response){ 
       getSysData();
     }
 }); 
 })
});

$(function() {
    $('#UVSet').click(function(){
      var value = $('#UVInput').val();
      var targetURL = '/SetOutputTarget/UV/0/' + value;
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#UVSwitch').click(function(){
       
       var targetURL = '/SetOutputOn/UV/2/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#LASER650Set').click(function(){
      var value = $('#LASER650Input').val();
      var targetURL = '/SetOutputTarget/LASER650/0/' + value;
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#LASER650Switch').click(function(){
       
       var targetURL = '/SetOutputOn/LASER650/2/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#GetSpectrum').click(function(){
      var value = $('#SpectrumGain').val();
      var targetURL = '/GetSpectrum/' + value + '/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});
    
$(function() {
    $('#ODSet').click(function(){
      var value = $('#ODInput').val();
      var targetURL = '/SetOutputTarget/OD/0/' + value;
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#OD0Set').click(function(){
      var value = $('#OD0Input').val();
      var value2 = $('#OD0Actual').val();
      var targetURL = '/CalibrateOD/OD0/0/' + value + '/' + value2;
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#VolumeSet').click(function(){
      var value = $('#VolumeInput').val();
      var targetURL = '/SetOutputTarget/Volume/0/' + value;
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#ODMeasure').click(function(){
      
      var targetURL = '/MeasureOD/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#TempMeasure').click(function(){
      
      var targetURL = '/MeasureTemp/External/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#TempMeasure2').click(function(){
      
      var targetURL = '/MeasureTemp/Internal/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#TempMeasure3').click(function(){
      
      var targetURL = '/MeasureTemp/IR/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#ThermostatSet').click(function(){
      var value = $('#ThermostatInput').val();
      var targetURL = '/SetOutputTarget/Thermostat/0/' + value;
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#ThermostatSwitch').click(function(){
       
       var targetURL = '/SetOutputOn/Thermostat/2/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#Pump1Set').click(function(){
      var value = $('#Pump1Input').val();
      var targetURL = '/SetOutputTarget/Pump1/0/' + value;
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#Pump1Switch').click(function(){
       
       var targetURL = '/SetOutputOn/Pump1/2/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#Pump1Direction').click(function(){
       
       var targetURL = '/Direction/Pump1/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#Pump2Set').click(function(){
      var value = $('#Pump2Input').val();
      var targetURL = '/SetOutputTarget/Pump2/0/' + value;
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#Pump2Switch').click(function(){
       
       var targetURL = '/SetOutputOn/Pump2/2/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#Pump2Direction').click(function(){
       
       var targetURL = '/Direction/Pump2/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#Pump3Set').click(function(){
      var value = $('#Pump3Input').val();
      var targetURL = '/SetOutputTarget/Pump3/0/' + value;
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#Pump3Switch').click(function(){
       
       var targetURL = '/SetOutputOn/Pump3/2/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#Pump3Direction').click(function(){
       
       var targetURL = '/Direction/Pump3/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#Pump4Set').click(function(){
      var value = $('#Pump4Input').val();
      var targetURL = '/SetOutputTarget/Pump4/0/' + value;
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#Pump4Switch').click(function(){
       
       var targetURL = '/SetOutputOn/Pump4/2/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#Pump4Direction').click(function(){
       
       var targetURL = '/Direction/Pump4/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#StirSet').click(function(){
      var value = $('#StirInput').val();
      var targetURL = '/SetOutputTarget/Stir/0/' + value;
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#StirSwitch').click(function(){
       
       var targetURL = '/SetOutputOn/Stir/2/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#LightSwitch').click(function(){
       var v1 = $('#LightExcite1').val();

       var targetURL = '/SetLightActuation/' + v1;
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#CustomSwitch').click(function(){
       var v1 = $('#CustomProgram1').val();
       var v2 = $('#CustomInput').val();
       var targetURL = '/SetCustom/' + v1 + '/' + v2;
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#FP1Switch').click(function(){
      var v1 = $('#FPExcite1').val();
      var v2 = $('#FPBase1').val();
      var v3 = $('#FPEmit1A').val();
      var v4 = $('#FPEmit1B').val();
      var v5 = $('#FPGain1').val();
      var targetURL = '/SetFPMeasurement/FP1/' + v1 + '/'+ v2 + '/'+ v3 + '/'+ v4 + '/'+ v5 ;
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#FP2Switch').click(function(){
      var v1 = $('#FPExcite2').val();
      var v2 = $('#FPBase2').val();
      var v3 = $('#FPEmit2A').val();
      var v4 = $('#FPEmit2B').val();
      var v5 = $('#FPGain2').val();
      var targetURL = '/SetFPMeasurement/FP2/' + v1 + '/'+ v2 + '/'+ v3 + '/'+ v4 + '/'+ v5;
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#FP3Switch').click(function(){
      var v1 = $('#FPExcite3').val();
      var v2 = $('#FPBase3').val();
      var v3 = $('#FPEmit3A').val();
      var v4 = $('#FPEmit3B').val();
      var v5 = $('#FPGain3').val();
      var targetURL = '/SetFPMeasurement/FP3/' + v1 + '/'+ v2 + '/'+ v3 + '/'+ v4 + '/'+ v5;
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#MeasureFP').click(function(){
      
      var targetURL = '/MeasureFP/0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#Device0').click(function(){
      var targetURL = '/changeDevice/M0';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#Device1').click(function(){
      var targetURL = '/changeDevice/M1';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});


$(function() {
    $('#Device2').click(function(){
      var targetURL = '/changeDevice/M2';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#Device3').click(function(){
      var targetURL = '/changeDevice/M3';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#Device4').click(function(){
      var targetURL = '/changeDevice/M4';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#Device5').click(function(){
      var targetURL = '/changeDevice/M5';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#Device6').click(function(){
      var targetURL = '/changeDevice/M6';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#Device7').click(function(){
      var targetURL = '/changeDevice/M7';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#ScanDevices').click(function(){
      var targetURL = '/scanDevices/all';
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});

$(function() {
    $('#CharacteriseDevice').click(function(){
      var v1 = $('#CHProgram').val();
      var targetURL = '/CharacteriseDevice/0/'+ v1;
       $.ajax({
           type:'POST',
           url: targetURL,
           success:function(response){ 
           getSysData();
         }
     }); 
     })
});