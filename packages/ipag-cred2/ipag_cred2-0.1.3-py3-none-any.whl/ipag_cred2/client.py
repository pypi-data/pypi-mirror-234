"""
Created on Fri Nov 27 19:49:19 2020

@author: f_p_0
"""
from __future__ import annotations
from typing import Any, Callable
import numpy as np
from ipag_cred2.define import (
        Cred2Config, cred2_config,  
        Cred2State, 
        ConversionGain,
        Cred2Error, 
        MAX_FPS, 
        Cred2ClientProtocol, 
        Cred2Temperatures,
        CropData,
    )

from ipag_core import ipag 


from ipag_cred2 import config as mod_conf
if mod_conf.flisdk_path:
    import sys 
    sys.path.append( mod_conf.flisdk_path )
del mod_conf

try:
    import FliSdk_V2 as FliSdk
except ModuleNotFoundError as _er:
    raise ModuleNotFoundError( 
        """Cannot locate FliSdk_V2 module. Please add fli sdk directory to sys.path before loading ipag_cred2.client """) from _er 


class Cred2Client(Cred2ClientProtocol):
    log = ipag.get_logger('cred2')
    context = None 
    state: Cred2State = Cred2State.OFF 

    def __init__(self, config: Cred2Config  = cred2_config):
        self.config = config
        self.cameraModel = ""
    
    def connect(self)->None:
        self.context = FliSdk.Init()
    
    def disconnect(self)->None:
        FliSdk.Exit(self.context)   

    def __del__(self):
        try:
           self.disconnect()
        except Exception:
            pass 
    
    def _get_value(self, method: Callable, name: str, *args):
        res, value = method(self.context, *args)
        if not res:
            raise Cred2Error(f"Cannot get {name}")
        return value
    
    def _get_values(self, method: Callable, name: str, *args):
        res, *values = method(self.context, *args)
        if not res:
            raise Cred2Error(f"Cannot get {name}") 
        return values
    
    def _set_value(self, method: Callable, name: str, value: Any, *moreargs ):
        res = method(self.context, value, *moreargs)
        if not res:
            raise Cred2Error(f"cannot set {name}")
        self.log.debug( f"value {name} set to {value} with {method}")

    def _command(self, method: Callable, name: str, *args):
        res = method(self.context, *args)
        if not res:
            raise Cred2Error(f"Cannot {name}")
        self.log.debug( f"command {name} sent with {method} and args {args}")

    def switchoff(self)->None:
        self.log.info('switch OFF CRED-2')
        self.set_acquisition_state(False)
        self.state = Cred2State.OFF

    def switchon(self)->None:
        self.log.info('Switching on ON CRED-2 ...')
        if self.context is None:
            self.connect()

        FliSdk.DetectGrabbers(self.context)
        listOfCameras = FliSdk.DetectCameras(self.context)

        if not listOfCameras:
            self.log.error('No camera detected, exit.')
            self.state = Cred2State.OFF
        else:
            FliSdk.SetCamera(self.context, listOfCameras[0])
            self.log.info('Camera Detected: %s', listOfCameras[0])
            self.state = Cred2State.ON 
            self.log.info( 'CRED-2 is now on' )
        FliSdk.Update(self.context)
    
    def shutdown(self)->None:
        self.log.warning('shuting down cred-2')
        res = FliSdk.FliCred.ShutDown(self.context)
        self.state = Cred2State.OFF 

    def is_on(self)->bool:
        return self.state == Cred2State.ON

    def get_fps(self)->float:
        """ return the current camera fps """ 
        return self._get_value( FliSdk.FliSerialCamera.GetFps, "fps")
    
    def set_fps(self, fps: float)->None:
        if 0 < fps <= MAX_FPS:
            self._set_value( FliSdk.FliSerialCamera.SetFps, "fps", fps)
        else:
            raise ValueError( f'wrong fps value: {fps} must be >0 and <{MAX_FPS}' )

    def get_max_fps(self)->float: 
        return self._get_value( FliSdk.FliSerialCamera.GetFpsMax, 'max_fps')
            
    def get_min_fps(self)->float:
        return self._get_value( FliSdk.FliCredTwo.GetMinFps, "min fps")
        
    def get_min_tint(self)->float:
        return 0.0
        
        
    def get_max_tint(self)->float:
        return self._get_value( FliSdk.FliCredTwo.GetMaxTintItr, "max_tint")
    
    def get_tint(self)->float:
        return self._get_value( FliSdk.FliCredTwo.GetTint, "tint")
    get_tint_current = get_tint # API issue 

    def set_tint(self, tint: float)->None:
        self._set_value( FliSdk.FliCredTwo.SetTint, "tint", tint)
        self.log.info(f'set tint to: {tint}')        

    def get_conversion_gain(self)->ConversionGain:
        return ConversionGain( self._get_value( FliSdk.FliCredTwo.GetConversionGain, "conversion_gain")) 
     
    def set_conversion_gain(self, gain:ConversionGain)->None:        
        self._set_value( FliSdk.FliCredTwo.SetConversionGain, "conversion_gain", ConversionGain(gain).value)
       
    def get_temperatures(self)->Cred2Temperatures:
        # TODO check is this is correct no res returned ? 
        return Cred2Temperatures(*self._get_values(FliSdk.FliCredTwo.GetAllTemp, 'all temperatures'))
 
    def get_sensor_setpoint_temperature(self)->float:
        return self._get_value( FliSdk.FliCredTwo.GetTempSnakeSetPoint, "temperature_sensor_setpoint")
    
    def set_sensor_setpoint_temperature(self, temp: float)->None:
        self._set_value( FliSdk.FliCredTwo.SetTempSnakeSetPoint, "temperature_sensor_setpoint", temp)

    def is_led_on(self)->bool:
        led_state = self._get_value( 
            FliSdk.FliSerialCamera.SendCommand, "led", 'led' 
        )
        return "on" in led_state
    
    def switch_led_on(self):
        self._get_value( FliSdk.FliSerialCamera.SendCommand, 'led on',  'set led on')
    
    def switch_led_off(self):
        self._get_value( FliSdk.FliSerialCamera.SendCommand, 'led off', 'set led off')
    
    def get_buffer_size(self)->int:
        return FliSdk.GetImagesCapacity(self.context)
    
    def get_buffer_filling(self)->int:
        return FliSdk.GetBufferFilling(self.context)
        
        
    def is_grabber_enabled(self)->bool:
        return  FliSdk.IsGrabNEnabled(self.context)
        
    
    def enable_grabber(self, nframe:int)->None:
        FliSdk.EnableGrabN(self.context, nframe)
    
    def disable_grabber(self):
        FliSdk.DisableGrabN(self.context)

            
    def _set_crop_data(self, enable, cropData):
        if not FliSdk.IsCroppingDataValid(self.context, cropData):
            msg = f'Cannot crop {cropData.row1}  {cropData.row2} {cropData.col1} {cropData.col2}'
            raise ValueError(msg)
        self._set_value( FliSdk.SetCroppingState, "crop data", enable, cropData)

    def reset_cropping(self):
        """ reset camera to full frame """
        cropData = FliSdk.CroppingData()
        cropData.col2 = self.config.width -1
        cropData.col1 = 0
        cropData.row2 = self.config.height -1
        cropData.row1 = 0
        return self._set_crop_data(False, cropData)
 

    def set_cropping(self,  col_min:int , col_max: int, row_min:int, row_max:int)->None:
        cropData = FliSdk.CroppingData()
        cropData.col2 = ((col_max+1) // 32) * 32 -1  #447
        cropData.col1 = (col_min // 32) * 32         #160  
        cropData.row2 = ((row_max+1) // 32) * 32 -1  #415
        cropData.row1 = (row_min // 32) * 32         #128
        self._set_crop_data(True, cropData)
    
    def is_cropped(self)->bool:
        state, _ = self.get_cropping() 
        return state 
    
    def get_cropping(self)->tuple[bool,CropData]:
        state, fcrop = self._get_values( FliSdk.GetCroppingState, 'cropping_state')
        return state, CropData( fcrop.col1, fcrop.col2, fcrop.row1, fcrop.row2)

    def is_grabber_finished(self)->bool:
        return FliSdk.IsGrabNFinished(self.context)
    
    def start_aquisition(self)->None:
        self._command( FliSdk.Start , "start Acquisition")
        self.log.info('acquisition started')
    
    def stop_aquisition(self)->None:
        self._command( FliSdk.Stop, "stop Acquisition")
        self.log.info('acquisition stoped')

    def is_acquisition_running(self):
        # TODO: Check return of IsStarted should'nt it be res,flag ? 
        return FliSdk.IsStarted(self.context)
        
    def save_images_buffer(self, filename: str, start_index: int, end_index:int):
        self._command( FliSdk.SaveBuffer, filename, start_index, end_index)
        
    def is_badpixel_enabled(self)->bool:
        return self._get_value( FliSdk.FliCredTwo.GetBadPixelState, "badpixel_state")
    
    def enable_badpixel(self) -> None:
        self._set_value( FliSdk.FliCredTwo.EnableBadPixel, "badpixel_state", True )
    
    def disable_badpixel(self) -> None:
        self._set_value( FliSdk.FliCredTwo.EnableBadPixel, "badpixel_state", False )

    def build_bias(self):
        self._command( FliSdk.FliCred.BuildBias, "build_bias")
    
    def is_bias_enabled(self)->bool:
        return self._get_value( FliSdk.FliCred.GetBiasState, "bias_state")

    def enable_bias(self)->None:
        self._set_value(FliSdk.FliSerialCamera.EnableBias, "bias_state", True)

    def disable_bias(self)->None:
        self._set_value(FliSdk.FliSerialCamera.EnableBias, "bias_state", False)

    def get_image_buffer(self, start_index, end_index):
        if end_index < start_index:
            indexes =  list(range(start_index, self.get_buffer_size()+1 ))
            indexes += list(range(0, end_index)) 
        else:
            indexes = range( start_index, end_index+1)
        img_array = np.array([ FliSdk.GetRawImageAsNumpyArray(self.context, i) for i in indexes])
        return img_array

    def get_single_image(self, index: int, mustProcess: bool = False):
        if mustProcess:
            return FliSdk.GetProcessedImageRGBANumpyArray(self.context, index)
        
        return FliSdk.GetRawImageAsNumpyArray(self.context, index)

    def upload_frames(self, frame_data):
        # TODO: check Is expected a numpy array ? What is the 100 ?  
        FliSdk.LoadBufferRaw(self.context, frame_data, 100)

    def upload_raw_file(self, file_name: str)->None:
        try:
            cropData = FliSdk.CroppingData(0,0,self.width, self.height)
            FliSdk.LoadBufferFromFile(self.context, file_name, cropData)
        except Exception:
            pass
    upload_raw_file_on_cred2 = upload_raw_file

    def get_sizes(self)-> tuple[float, float]:
        cropEnabled, cropData = self.get_cropping()
        
        if cropEnabled:
            col1 = cropData.col1
            col2 = cropData.col2
            row1 = cropData.row1
            row2 = cropData.row2
            
            width = col2 - col1 +1
            height = row2 - row1 +1
        else:
            width = self.config.width
            height = self.config.height 
        return width, height

    def get_fullframe_sizes(self) -> tuple[float, float]:
        return self.config.width, self.config.height




if __name__ == "__main__":
    Cred2Client( )

