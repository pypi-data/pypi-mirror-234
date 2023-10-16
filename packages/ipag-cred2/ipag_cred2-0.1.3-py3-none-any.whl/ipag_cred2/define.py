from __future__ import annotations
from collections import namedtuple
from enum import Enum
from functools import partial, wraps
from typing import Any, Callable, NamedTuple
from typing_extensions import Protocol
from abc import abstractmethod 
from warnings import warn
from pydantic import BaseModel
import numpy as np 

from ipag_cred2 import config as mod_conf
from ipag_core.dev_tools import deprecated 


MAX_FPS = 600

class Cred2State(int, Enum):
    OFF = 0 
    ON  = 1 


class ConversionGain(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Cred2Config(BaseModel):
    width: float = mod_conf.width 
    """ Full frame width in pixels """
    height: float = mod_conf.height 
    """ Full frame height in pixel """
    camera_model: str = "CRED-2" 
    """ camera model name """

cred2_config = Cred2Config()
""" Default configuration for Cred2 """



class Cred2Error(RuntimeError):
    pass

class CropData(NamedTuple):
    col1: int 
    col2: int 
    row1: int 
    row2: int 

# as returned by client get_parameters method Should Be Removed !!!!! 
Cred2Params = namedtuple("Cred2Parameters",
["fps","max_fps", "min_tint","max_tint","tint",
 "conversion_gain","temperature_setpoint","led","badpixel_state",
 "bias_state","buffer_size","crop_state","x0","y0","width","height"]
)

class Cred2Temperatures(NamedTuple):
    motherboard:float = np.nan 
    frontend:float = np.nan 
    sensor:float = np.nan 
    peltier:float = np.nan 
    heatsink:float = np.nan 
    ANONIMOUS: float = np.nan




class Cred2ClientProtocol(Protocol):
    """ Define all Function of a Cred2 Client (real or simulated) 
    
    This class cannot be instancied by itself. Use instead ::

        from ipag_cred2.client import Cred2Client
        or 
        from ipag_cred2.sim import CredSim 

    """
    @abstractmethod
    def connect(self)->None:
        """ Connect client to FLi SDK """
        ... 

    @abstractmethod 
    def disconnect(self)->None:
        """ Disconnect this client from SDK """
        ...
    @abstractmethod
    def switchoff(self)->None:
        """ switch camera off """
        ...
    @abstractmethod
    def switchon(self)->None:
        """ switch camera on """
        ...
    @abstractmethod
    def shutdown(self) -> None:
        """ shutdown the camera """
        ...
    @abstractmethod
    def is_on(self) -> bool:
        """ return True is camera is on, False otherwise """ 
        ...
    @abstractmethod
    def get_fps(self)-> float:
        """ Return the current camera frame per seconds (fps) """
        ...
    @abstractmethod
    def set_fps(self, fps: float) -> None:
        """ Set the fps to the camera 

        Args:
            fps: number of frame per seconds
        
        """
        ...
    @abstractmethod
    def get_max_fps(self)-> float:
        """ Return the max frame rate supported by the camera """
        ...
    @abstractmethod
    def get_min_fps(self) -> float:
        """ Return the minimum fps allowd by the camera """
        ...
    @abstractmethod
    def get_min_tint(self)->float:
        """ Return the minimum integration time allowed by the camera """
        ...
    @abstractmethod
    def get_max_tint(self)->float:
        """ Return the maximum integration time allowed by the camera """
        ...
    @abstractmethod
    def get_tint(self) -> float:
        """ Get the current integration time """
        ...
    @abstractmethod
    def set_tint(self, tint: float) -> None:
        """ Set the integration time 

        Args:
            tint: Integration time in second 
        """
        ...
    @abstractmethod
    def get_conversion_gain(self) -> ConversionGain:
        """ Return the curent conversion gain """
        ...

    @abstractmethod
    def set_conversion_gain(self, gain: ConversionGain) -> None:
        """ Set conversion gain 
        
        Args:
            gain: A valid ConversionGain  ("low", "medium", "high")
        """
        ...


    @abstractmethod
    def get_temperatures(self) -> Cred2Temperatures:
        """ Gets all temperatures from the camera in a named tuple
            - motherboard
            - frontend
            - sensor
            - peltier
            - heatsink    
        """
        ...


    @abstractmethod
    def get_sensor_setpoint_temperature(self) -> float:
        """ Return the ensor setpoint temperatures """
        ...

    @abstractmethod
    def set_sensor_setpoint_temperature(self, value: float) -> None:
        """ Set the temperature setpoint value 
        
        Args:
            temp: Temperature setpoin in Celcius 
        """ 
        ...
        
    @abstractmethod
    def is_led_on(self) -> bool:
        """ Get current led state, True if led is on, False otherwise """
        ...
    
    @abstractmethod
    def switch_led_on(self)->None:
        """ switch the led one """
        ... 
        
    @abstractmethod
    def switch_led_off(self)->None:
        """ switch the led off """
        ... 
    
    @abstractmethod
    def get_buffer_size(self) -> int:
        """ Get the camera buffer size """
        ...
    
    @abstractmethod
    def get_buffer_filling(self) -> int:
        """ Get the camera buffer filling (e.g. Occupied buffer size) """
        ...
    
    @abstractmethod
    def enable_grabber(self, nframe: int)->None:
        """ Enable the grabber with a given number of frame 

        Args:
            nframe: number of frame 
        """
        ...

    @abstractmethod
    def disable_grabber(self)->None:
        """ Disable the grabber """ 
        ... 

    @abstractmethod
    def is_grabber_enabled(self)->bool:
        """ Get the grabber state, True if running, False otherwise """
        ...

    
    @abstractmethod
    def reset_cropping(self) -> bool:
        """ Reset camera to full frame """
        ...
    
    @abstractmethod
    def set_cropping(self,  col_min: 'int', col_max: 'int', row_min: 'int', row_max: 'int') -> None:
        """ Set the camera cropping 

        Args:
           col_min: vertical left value.
           col_max: vertical right value.
           row_min: horizontal upper value
           row_max: horizontal lower value
        """
        ...
    
    @abstractmethod
    def get_cropping(self)->tuple[bool, CropData]:
        """ Return cropping enable state and crop data """
        ...
     
    @abstractmethod
    def is_cropped(self)->bool:
        """ Return True if cropping is enabled """
        ...
    
    @abstractmethod
    def is_grabber_finished(self) -> bool:
        """ Return True if Grabber has finished is job False otherwise """
        ...
    
    @abstractmethod
    def start_aquisition(self) -> None:
        """ Start Camera frame  Aquisition """
        ...

    @abstractmethod
    def stop_aquisition(self) -> None:
        """ Stop camera acuisition """
        ...
    
    @abstractmethod
    def is_acquisition_running(self)->bool:
        """ return True if acquisition is started, else return False """
        ...

    @abstractmethod
    def save_images_buffer(self, filename: str, start_index: int, end_index: int):
        """ Save part of the buffer 

        Args:
            filename: file name (e.g. '.tiff' see valid Fli format)
            start_index: buffer index of first frame 
            end_index: buffer index of last frame 
        """
        ...
    
    @abstractmethod
    def enable_badpixel(self)->None:
        """ Enable the badpixel mapping """
        ...
    
    @abstractmethod
    def disable_badpixel(self)->None:
        """ Disable the badpixel mapping """
        ...
    
    @abstractmethod
    def is_badpixel_enabled(self) -> bool:
        """ Return True is bad pixel mapping is on, False otherwise """
        ...
    
    @abstractmethod
    def build_bias(self)->None:
        """ record camera Bias """
        ...
    
    @abstractmethod
    def is_bias_enabled(self)->bool:
        """ Return True if bias is in use """
        ...
    
    @abstractmethod
    def enable_bias(self)->None:
        """ Enable the use of a bias in camera """
        ...
    
    @abstractmethod
    def disable_bias(self)->None:
        """ Disable the use of a bias in camera """
        ...
       
    @abstractmethod
    def get_image_buffer(self, start_index, end_index)->np.ndarray:
        """ Extract in a numpy array buffer images 

        Args:
            start_index: buffer index of first frame 
            end_index: buffer index of last frame 
        
        Returns:
            array of uint16
        """
        ...
        
    @abstractmethod
    def get_single_image(self, index:int , mustProcess: bool =False)->np.ndarray:
        """ Get one single frame  or processed image from the buffer 

        Args:
            index: Buffer index number where the frame is
            mustProcess: If True Processed RGB images are returned 

        Returns:
            array of uint16 is not processed or ????? TODO: What does it returns  
        """
        ...
    
    @abstractmethod
    def get_parameters(self)->Cred2Params:
        """ Return parameters in a Cred2Params (named tuple object) 

        You may want to us a CredState object instead 
        """
        ...
    
    @abstractmethod
    def upload_frames(self, frame_data: np.ndarray)->None:
        """ Load frames inside the buffer """
        ...
    
    @abstractmethod
    def upload_raw_file(self, file_name: str)->None:
        """ Upload a file on the camera buffer """
        ...
    
    @abstractmethod
    def get_sizes(self)->tuple[float, float]:
        """ Return (width, heigh), the current images size according to cropping """
        ...  
    
    @abstractmethod
    def get_fullframe_sizes(self)->tuple[float, float]:
        """ Return (width, heigh) of a full frame image
        
        Use get_sizes() if you want to cropped sizes 
        """
        ...  
    
   
    # ---------------------------------------------------------
    #
    #                    Helpers METHODS 
    #
    # ----------------------------------------------------------
    def toggle_led(self, state: bool | None = None)->bool:
        """ Toggle the led on or off 

        Args:
            state (optional): True to switch led on, False off
                If None it change current state 
        Returns:
            new_state: bool 
        """
        return _toggler(state, self.is_led_on, self.switch_led_on, self.switch_led_off)

    def toggle_bias(self, state: bool | None = None)->bool:
        """ Toggle the usage of the bias 
        
        Args:
            state (optional): True to enable bias, False to disable
                If None it change current state 
        Returns:
            new_state: bool 
        """
        return _toggler(state, self.is_bias_enabled, self.enable_bias, self.disable_bias)

    def toggle_badpixel(self, state: bool | None = None)->bool:
        """ Toggle the usage of the badpixel mapping
        
        Args:
            state (optional): True to enable badpixel, False to disable
                If None it change current state 
        Returns:
            new_state: bool 
        """
        return _toggler(state, self.is_badpixel_enabled, self.enable_badpixel, self.disable_badpixel)

    


# ---------------------------------------------------------
#
#                     DEPRECATED METHODS 
#
# ----------------------------------------------------------

    """ All these Cred2Client methods are deprected and will be removed at some point"""

    @deprecated("use :func:`~set_sensor_setpoint_temperature` instead", "0.1" )
    def set_sensor_temperature(self, temp:float)->None:
        self.set_sensor_setpoint_temperature(temp) # API issue 
    

    @deprecated("use :func:`~set_sensor_setpoint_temperature` instead", "0.1" )
    def set_temperature(self, temp:float)->None:
        self.set_sensor_setpoint_temperature(temp) # API issue 
    

    @deprecated("use :func:`~switch_led_on` or :func:`~switch_led_off` instead", "0.1" )
    def set_led(self, status: bool)->bool:
        if status: 
            self.switch_led_on()
        else:
            self.switch_led_off()

    @deprecated("use :func:`~enable_grabber` or :func:`~disable_grabber` instead", "0.1")
    def set_grabber_state(self, enable: bool, nframe:int  = 0)->None:
        if enable:
            self.enable_grabber(nframe) 
        else:
            self.disable_grabber() 
    
    @deprecated("use :func:`~start_scquisition` or :func:`stop_aquisition` instead", "0.1")
    def set_acquisition_state(self, action):
        if action:
            self.start_aquisition()
        else:
            self.stop_aquisition()
    
    @deprecated("use :func:`~build_bias` instead", "0.1")
    def set_bias(self):
        return self.build_bias()

    @deprecated("use :func:`~is_bias_enabled` instead", "0.1")
    def get_bias(self):
        return self.is_bias_enabled()
    

    @deprecated("use :func:`~enable_bias` or :func:`~disable_bias`  instead", "0.1" )
    def use_bias(self, state: bool):
        if state:
            self.enable_bias()
        else:
            self.disable_bias()
        return state
    
    @deprecated("use :func:`~is_acquisition_running`  instead", "0.1" )
    def get_acquisition_state(self)->bool:
        return self.is_aquisition_started() 
    
    @deprecated("use :func:`~is_grabber_finished`  instead", "0.1" )
    def get_grabber_finished(self)->bool:
        return self.is_grabber_finished() 
    
    @deprecated("use :func:`~is_grabber_enabled`  instead", "0.1" )
    def get_grabber_state(self)->bool:
        return self.is_grabber_enabled() 

    @deprecated(" use :func:`~is_led_on`  instead", "0.1") 
    def get_led(self)->bool:
        return self.is_led_on() 
    
    @deprecated("use a Cred2FrameReader instead", "0.1" )
    def acquire_n_pictures(self, number_of_frame: int):
        # nasty import to avoid cycling references to be removed anyway
        from ipag_cred2.io import Cred2FrameReader
        return Cred2FrameReader(self, number_of_frame).read() 

    @deprecated("use :func:`~upload_raw_file` instead", "0.1") 
    def upload_raw_file_on_cred2(self, file_name:str):
        return self.upload_raw_file(file_name) 
    
    @deprecated("use a state object instead", "0.1")
    def get_parameters(self)->Cred2Params:
        cropEnabled, cropData = self.get_cropping()
        x0     = cropData.col1 + (cropData.col2+1 - cropData.col1) / 2
        y0     = cropData.row1 + (cropData.row2+1 - cropData.row1) / 2
        width  = cropData.col2+1 - cropData.col1
        height = cropData.row2+1 - cropData.row1
        
        return Cred2Params( fps= self.get_fps(), 
                            max_fps = self.get_max_fps(),
                            min_tint = self.get_min_tint(), 
                            max_tint = self.get_max_tint(), 
                            tint = self.get_tint(), 
                            conversion_gain = self.get_conversion_gain(), 
                            temperature_setpoint = self.get_sensor_setpoint_temperature(),
                            led = self.is_led_on(),
                            badpixel_state = self.is_badpixel_enabled(),
                            bias_state = self.is_bias_enabled(), 
                            buffer_size = self.get_buffer_size(), 
                            crop_state = cropEnabled, 
                            x0 = x0, 
                            y0 = y0, 
                            width = width, 
                            height = height
                    )






def _toggler(
         target_state: bool | None, 
         state_checker: Callable, 
         turn_on_func: Callable, 
         turn_off_func: Callable
    )->bool:
    if target_state is None:
        target_state = not state_checker()
    if target_state:
        turn_on_func()
    else:
        turn_off_func() 
    return target_state


