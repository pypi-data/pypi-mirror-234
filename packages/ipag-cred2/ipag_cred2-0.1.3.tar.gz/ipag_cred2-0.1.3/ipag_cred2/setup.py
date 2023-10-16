from __future__ import annotations
from typing_extensions import Annotated
from logging import getLogger
from typing import ClassVar, NamedTuple, Optional, Type, Union
from pydantic import  AfterValidator, Field


from ipag_core import ipag  
from ipag_cred2.define import MAX_FPS, Cred2ClientProtocol , ConversionGain, CropData , cred2_config
log = ipag.get_logger()

    
CropVar = Annotated[int, AfterValidator( lambda x: (x//32)*32 )]
CropMaxVar = Annotated[int, AfterValidator( lambda x: ((x+1)//32)*32-1 )]

def _togle_cropping(cred2: Cred2ClientProtocol,  enable: bool, new_crop: CropData):
    current_state, crop_data = cred2.get_cropping()
    if enable:
        if crop_data != new_crop or not current_state:
            if cred2.is_grabber_enabled():
                cred2.disable_grabber()
                cred2.set_cropping( *new_crop)
                cred2.enable_grabber()
            else:
                cred2.set_cropping( *new_crop)
    else:
        if current_state:
            if cred2.is_grabber_enabled():
                cred2.disable_grabber()
                cred2.reset_cropping()
                cred2.enable_grabber()
            else:
                cred2.reset_cropping()


class CropSetup(ipag.UserModel):
    cmin: CropVar = 0
    """ Index of the left column """
    cmax: CropMaxVar = cred2_config.width-1 
    """ Index  of the right column """
    rmin: CropVar = 0 
    """ Index of the lower row """
    rmax: CropMaxVar = cred2_config.height-1
    """ Index of the upper row """
    enable: bool = True
    """ use of this crop if False camera is reseted to full frame """
    
    def crop_data(self):
        return CropData( self.cmin, self.cmax, self.rmin, self.rmax)

    def setup(self, cred2: Cred2ClientProtocol)->None:
        new_crop = self.crop_data() 
        _togle_cropping( cred2, self.enable, new_crop)
    
class CropPosSetup(ipag.UserModel):
    """ A Crop using window position and size """
    
    x0: CropVar = 0 
    """ Lower posotion of the crop """
    y0: CropVar = 0
    """ Upper position of the crope """
    width: CropVar = cred2_config.width
    """ Crop width """
    height: CropVar = cred2_config.height 
    """ Crop height """
    enable: bool = True
    """ use of this crop if False camera is reseted to full frame """
    
    def crop_data(self):
        return  CropData( self.x0, self.x0+self.width-1, self.y0, self.y0+self.height-1) 

    def setup(self, cred2: Cred2ClientProtocol)->None:
        new_crop = self.crop_data()
        new_crop = _togle_cropping( cred2, self.enable, new_crop)
    
    def update_from_cropdata(self, crop_data: CropData):
        self.x0 = crop_data.col1 
        self.width = crop_data.col2 - crop_data.col1 + 1 
        self.y0 = crop_data.row1
        self.height = crop_data.row2 - crop_data.row1 + 1
         

    def update(self, cred2: Cred2ClientProtocol)->None:
        self.enable, crop_data = cred2.get_cropping()
        self.update_from_cropdata( crop_data )


class Cred2ExposureSetup(ipag.UserModel):
    fps: float = Field(100.0, le=MAX_FPS) 
    """ number of Frame Per Seconds (Hz)"""
    
    tint: Optional[float] = None # if None -> 1/fps  
    """ Integration time. If None 1/fps is used """
    
    conversion_gain: ipag.types.valueof(ConversionGain) = ConversionGain.LOW.value
    """ Conversion gain as defined in :class:`ConversionGain` """
    
    def setup(self, cred2: Cred2ClientProtocol):
        """ Setup the detector """
        cred2.set_conversion_gain(self.conversion_gain)
        cred2.set_fps( self.fps )
        cred2.set_tint( 1.0/self.fps if self.tint is None else self.tint) 

    def update(self, cred2: Cred2ClientProtocol):
        self.conversion_gain = cred2.get_conversion_gain()
        self.fps = cred2.get_fps()
        self.tint = cred2.get_tint()


class Cred2DetSetup(Cred2ExposureSetup):
    """ Setup and State updater for all conserning Cred2 Sensor """

    crop: Union[None,  CropSetup, CropPosSetup] = CropSetup(enable=False)
    """ crop setup, either :
        - A valid Crop setup see, :class:`CropSetup', :class:`CropPosSetup`, :class:`FullFrameSetup`  
        - None: Leave cropping unchanged 
    """

    bias: Optional[bool] = None 
    """ If True, the built bias is used. If None bias state is unchaged """
     
    def setup(self, cred2: Cred2ClientProtocol):
        """ Setup the detector """
        
        if self.crop :
            self.crop.setup(cred2)
        Cred2ExposureSetup.setup(self, cred2) 

        if self.bias is not None:
            if self.bias: 
                cred2.enable_bias()
            else:
                cred2.disable_bias()
    
    def update(self, cred2: Cred2ClientProtocol):
        Cred2ExposureSetup.update( self, cred2) 
        if not self.crop:
            self.crop = CropSetup()
        self.crop.update(cred2)
        self.bias = cred2.is_bias_enabled() 

class Cred2HouseKeepingSetup(ipag.UserModel):
    """ Setup and State updater for all conserning Cred2 House Keeping """

    sensor_setpoint_temperature: Optional[float] = None 
    """ Set point sensor temperature in degree Celcius. If None, this is unchanged """
    
    led: Optional[bool] = None 
    """ set led on if true, false otherwise. If None led state is unchange """

    def setup(self, cred2: Cred2ClientProtocol):
        """ Setup camera house keeping """ 
        if self.sensor_setpoint_temperature is not None:
            cred2.set_sensor_setpoint_temperature(self.sensor_setpoint_temperature) 
        if self.led is not None:
            if self.led:
                cred2.switch_led_on()
            else:
                cred2.switch_led_off()

    def update(self, cred2: Cred2ClientProtocol):
        """ Update house keeping from camera client instance """
        self.sensor_setpoint_temperature = cred2.get_sensor_setpoint_temperature()
        self.led = cred2.is_led_on() 
        

class Cred2Setup(ipag.UserModel):
    """ A Full Setup class for the Cred2 camera 
    
    Organised by two groups: 
        - ``.det`` for everything conserning the sensor
        - ``.house_keeping`` for everything conserning camera house keeping 
            (setpoint temperature, led, ..)

    .. seealso::

        :class:`~Cred2FlatSetup`
    """ 
    
    switchon: bool = True
    """ Flag to switch the camera on if off """
    
    det: Cred2DetSetup = Cred2DetSetup()
    """ Detector setup """
    
    house_keeping: Cred2HouseKeepingSetup = Cred2HouseKeepingSetup()
    """ House keeping setup """

    # set classes here for conveniant user access 
    Det : ClassVar[type] = Cred2DetSetup
    HouseKeeping: ClassVar[type] = Cred2HouseKeepingSetup 
    
    
    def setup(self, cred2: Cred2ClientProtocol)->None:
        """ setup the camera """
        if self.switchon and not cred2.is_on():
            cred2.switchon()
        self.det.setup(cred2)
        self.house_keeping.setup(cred2)

    def update(self, cred2: Cred2ClientProtocol):
        self.det.update(cred2)
        self.house_keeping.update(cred2)

class Cred2FlatSetup(Cred2DetSetup, Cred2HouseKeepingSetup):
    """ A Full Setup class of the camera where all parameters are flattened 
    
    This setup model takes all parameters of :class:`~Cred2Det` and :class:`~Cred2HouseKeeping`
    .. seealso::

        :class:`~Cred2Setup`
    """
    switchon: bool = True

    def setup(self, cred2: Cred2ClientProtocol):
        if self.switchon and not cred2.is_on():
            cred2.switchon()
        Cred2DetSetup.setup( self, cred2)
        Cred2HouseKeepingSetup.setup(self, cred2)
    
    def update(self, cred2: Cred2ClientProtocol):
        Cred2DetSetup.update( self, cred2)
        Cred2HouseKeepingSetup.update(self, cred2)


if __name__ == "__main__":
    
    from ipag_cred2.sim import Cred2Sim 
    c = Cred2Sim()
    setup = Cred2Setup( det=dict(fps=200,  conversion_gain="medium", bias=True, crop=dict(cmin=0, cmax=31, rmin=32, rmax=63)) )
    
    setup.setup(c) 
    print ( setup.det  )
    
    print(setup) 
    setup.det.crop = {"enable":False}

    print(setup)
    # setup.setup(c)
