from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Union
from ipag_core import ipag

from ipag_cred2.define import ConversionGain, Cred2ClientProtocol ,  Cred2Temperatures, cred2_config, CropData
from ipag_cred2.setup import  CropVar, CropMaxVar


class CropState(ipag.StateModel):
    cmin: CropVar = 0
    """ Index of the left column """
    cmax: CropMaxVar = cred2_config.width-1 
    """ Index  of the right column """
    rmin: CropVar = 0 
    """ Index of the lower row """
    rmax: CropMaxVar = cred2_config.height-1
    """ Index of the upper row """
    enabled: bool = False 
    """ True if crop is enabled """

    @property
    def x0(self):
        return self.cmin 
    @property 
    def y0(self):
        return self.rmin 
    @property
    def width(self):
        return self.cmax - self.cmin + 1 
    @property
    def height(self):
        return self.rmax - self.rmin + 1

    def update(self, cred2: Cred2ClientProtocol):
        crop_enabled, crop_data = cred2.get_cropping()
        self.cmin = crop_data.col1 
        self.cmax = crop_data.col2
        self.rmin = crop_data.row1
        self.rmax = crop_data.row2 
        self.enabled = crop_enabled
   
class Cred2ExposureState(ipag.StateModel):
    fps: float = math.nan
    tint: float = math.nan
    conversion_gain: ConversionGain = ConversionGain.LOW 
    def update(self,  cred2: Cred2ClientProtocol):
        self.fps= cred2.get_fps()
        self.tint = cred2.get_tint()
        self.conversion_gain = cred2.get_conversion_gain()
    

class Cred2DetState(Cred2ExposureState):
    """ A model representing the CRED2 detector state """
    badpixel: bool = False 
    bias: bool = False 
    crop: CropState = CropState(enabled=False) 
    
    def update(self, cred2: Cred2ClientProtocol):
        Cred2ExposureState.update(self, cred2) 
        self.badpixel = cred2.is_badpixel_enabled()
        self.bias = cred2.is_bias_enabled() 
        self.crop.update(cred2)
    
 
class Cred2CameraState(ipag.StateModel):
    """ A model representing CRED-2 camera caracteristics """
    max_fps: float = math.nan 
    min_fps: float = math.nan 
    max_tint: float = math.nan 
    min_tint: float = math.nan 
    width: int = cred2_config.height 
    height: int = cred2_config.width
    
    def update(self, cred2: Cred2ClientProtocol):
        self.max_fps = cred2.get_max_fps()
        self.min_fps = cred2.get_min_fps()

        self.min_tint = cred2.get_min_tint() 
        self.max_tint = cred2.get_max_tint() 
        self.width, self.height = cred2.get_fullframe_sizes()
    

class Cred2HouseKeepingState(ipag.StateModel):
    temperatures: Cred2Temperatures = Cred2Temperatures()
    sensor_setpoint_temperature: float = math.nan 
    led: bool = False  
    
    def update(self, cred2: Cred2ClientProtocol)->None:
        self.temperatures = cred2.get_temperatures()
        self.sensor_setpoint_temperature = cred2.get_sensor_setpoint_temperature()
        self.led = cred2.is_led_on()


class Cred2State(ipag.StateModel):
    det: Cred2DetState = Cred2DetState()
    house_keeping: Cred2HouseKeepingState = Cred2HouseKeepingState()
    camera: Cred2CameraState = Cred2CameraState()

    def update(self, cred2: Cred2ClientProtocol)->None:
        self.det.update(cred2)
        self.house_keeping.update(cred2)
        self.camera.update(cred2)


if __name__ == "__main__":
    from ipag_core import ipag 
    from ipag_cred2.sim import Cred2Sim
    m = ipag.new_metadata()
    c2 = Cred2Sim()
    s = Cred2State( )
    s.update( c2 ) 
    # s.populate_metadata( m) 
    print( s) 
    # Cred2DetState( fps=100, tint=0.002).populate_metadata( m, "DET")
    # print(repr(m))
    # s =  Cred2DetState( )
    # s.update_from_metadata( m, "DET")
    # print(s)
    
    # m = ipag.new_metadata()
    # from ipag_core.metadata import auto_populate_metadata, auto_update_from_metadata
    
    # auto_populate_metadata( m , mtio, s, prefix="TOTO" ) 
    # print(repr(m))
    # m['TOTO CROP CROP'] = '(0,31, 0, 32)'
    # m['TOTO CROP CROP USED'] = True 
    # ss = Cred2DetState()
    # auto_update_from_metadata( ss, mtio, m, prefix="TOTO") 
    # print("YO", ss) 
    


    # from ipag_cred2.sim import Cred2Sim 
    # from dataclasses import asdict 
    # import yaml
    # c = Cred2Sim() 
    # state = Cred2State()
    # state.update(c)
    # print( yaml.dump( state.model_dump() ) )
    # print(  Cred2State(  **yaml.load(  yaml.dump(state.model_dump()), yaml.CLoader) ))
    
