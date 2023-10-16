from __future__ import annotations
from dataclasses import dataclass, field
import time
import numpy as np
from logging import getLogger 
from threading import Thread

from ipag_core.log import get_logger 
from ipag_cred2.define import (
        Cred2Config, cred2_config,  
        Cred2State, 
        ConversionGain, 
        MAX_FPS,  
        Cred2Temperatures, 
        Cred2ClientProtocol,
        CropData
    )

full_frame = CropData( 0, cred2_config.width-1, 0, cred2_config.height -1)


@dataclass
class SimParameters:
    """ Simulation parameters """
    fps: int = 100 
    max_fps: int = 1000# TODO Check value 
    min_fps: int = 0#
    min_tint: float = 0.0
    max_tint: float = 1.0
    tint: float = 1/100.
    
    conversion_gain: ConversionGain = ConversionGain.LOW 
    temperatures: Cred2Temperatures = Cred2Temperatures(50.0,20.0,-50.0,16.3,30.0, 0.0) # TODO: set better temp 
    setpoint_temperature: float = -15.0
    led_status: bool = False
    
    buffer_size: int = 1000 # TODO: What is the buffer size ?
    buffer_filling: int = 0 
    
    grabber_state: bool = False 
    nframe: int = 0
    
    crop: CropData = field(default=full_frame)
    cropping_state: bool = False 
    bad_pixel_state: bool = False 
    bias_state: bool = False 
    
    mean_flux: float = 100.0
    sigma_flux: float= 10.0
    
    aquisition_state: bool = False 
    aquisition_frame: int = 0 


class Grabber:
    """ A Grabber Simulator """
    def __init__(self, sim: SimParameters):
        self.sim = sim 
        # self.buffer = deque( [], sim.buffer_size) 
        self.buffer = RingBuffer( [] , sim.buffer_size) 
    
    def generate_frame(self, sim, shape):
        data = np.random.normal( sim.mean_flux, sim.sigma_flux, shape ).astype('uint16')
        data[ data>16383 ] = 16383 
        return data

 
    def next_frame(self):
        sim = self.sim
        if sim.cropping_state:
            shape =   sim.crop.row2-sim.crop.row1 +1 , sim.crop.col2-sim.crop.col1 +1
        else:
            shape = cred2_config.height, cred2_config.width
        data = self.generate_frame(sim, shape)
        
        self.buffer.append(data) 
        sim.buffer_filling += 1 
        sim.buffer_filling %= sim.buffer_size    

    def acquire(self):
        self.sim.aquisition_state = True 
        
        frame_number = 0
        while self.sim.aquisition_state and self.sim.grabber_state:
            if not self.sim.fps:
                break 
            if frame_number>= self.sim.nframe:
                break 
            self.next_frame() 
            frame_number+= 1
            time.sleep( max( 1.0/self.sim.fps , 1e-4) )

        self.sim.aquisition_state = False
    


class Cred2Sim(Cred2ClientProtocol):
    log = get_logger('cred2')
    state: Cred2State = Cred2State.OFF 

    def __init__(self, config: Cred2Config= cred2_config, Grabber=Grabber):
        self.config = config 
        self._sim = SimParameters() 
        self._acq_thread = None
        self._grabber = Grabber( self._sim)  
        self.Grabber = Grabber 
    
    def connect(self):
        ... 
    
    def disconnect(self):
        ...

    def switchoff(self):
        self.state = Cred2State.OFF
        self.log.info('SIM! switch OFF CRED-2')
    
    def switchon(self):
        self.state = Cred2State.ON
        self.log.info( 'SIM! CRED-2 is now on' )
    
    def shutdown(self)->None:
        """ Shutdown the camera """
        self.logger.warning('shuting down cred-2')
        self.state = Cred2State.OFF 
     
    def is_on(self)->bool:
        """ True is camera is on """
        return self.state == Cred2State.ON
    
    def get_fps(self):
        return self._sim.fps 

    def set_fps(self, fps: float)->None:
        if 0 < fps <= MAX_FPS:
            self._sim.fps = fps  
            self.log.info(f'set fps to: {fps}')
        else:
            self.log.error(f'wrong fps value: {fps} must be >0 and <{MAX_FPS}')

    def get_max_fps(self)->float:
        return self._sim.max_fps 

    def get_min_fps(self)->int:
        return self._sim.min_fps 

    def get_min_tint(self)->float:
        return self._sim.min_tint 
    
    def get_max_tint(self)->float:
        return self._sim.max_fps

    def get_tint(self)->float:
        return self._sim.tint 

    def set_tint(self, tint:float)->None:
        self._sim.tint = tint

    def get_conversion_gain(self)->ConversionGain:
        return self._sim.conversion_gain 
    
    def set_conversion_gain(self, gain:ConversionGain)->None:        
        gain = ConversionGain(gain)
        self._sim.conversion_gain = gain

    def get_temperatures(self)->Cred2Temperatures:
        return self._sim.temperatures

    def get_sensor_setpoint_temperature(self)->float:
        return self._sim.setpoint_temperature 
    
    def set_sensor_setpoint_temperature(self, value: float)->None:
        self._sim.setpoint_temperature = value

    def is_led_on(self)->bool:
        return self._sim.led_status
    
    def switch_led_on(self)->None:
        self._sim.led_status = True

    def switch_led_off(self)->None:
        self._sim.led_status = False 

    def get_buffer_size(self)->int:
        return self._sim.buffer_size

    def get_buffer_filling(self)->int:
        return self._sim.buffer_filling
    
    def is_grabber_enabled(self):
        return self._sim.grabber_state

    def enable_grabber(self, nframe:int)->None:
        self._sim.grabber_state = True
        self._sim.nframe = nframe 
        if self._grabber is None:
            self._grabber = self.Grabber(self._sim) 

    def disable_grabber(self)->None:
        self._sim.grabber_state = False 

    def reset_cropping(self)->bool:
        self._sim.crop = full_frame
        self._sim.cropping_state = False 
        return True 

    def set_cropping(self,  col_min:int , col_max: int, row_min:int, row_max:int)->None:
        col2 = ((col_max+1) // 32) * 32 -1         #447
        col1 = (col_min // 32) * 32                #160  
        row2 = ((row_max+1) // 32) * 32 -1         #415
        row1 = (row_min // 32) * 32     
        self._sim.crop = CropData( col1, col2, row1, row2)
        self._sim.cropping_state = True 
        
    def get_cropping(self)->tuple[bool, CropData]:
        return self._sim.cropping_state, self._sim.crop

    def is_cropped(self)->bool:
        return self._sim.cropping_state 
    
    def is_grabber_finished(self)->bool:
        return not (self._grabber and self._sim.grabber_state and self._sim.aquisition_state)

    def start_aquisition(self)->None:
        if self._grabber is None:
            raise RuntimeError("Grabber is not started")
        self._sim.grabber_state = True 
        self._acq_thread = Thread( target=self._grabber.acquire )
        self._acq_thread.start()
        
    
    def stop_aquisition(self)->None:
        self._sim.aquisition_state = False 
        

    def is_acquisition_running(self):
        return self._sim.aquisition_state

    def save_images_buffer(self, filename: str, start_index: int, end_index:int):
        ... 
    
    
    def enable_badpixel(self)->None:
        self._sim.bad_pixel_state = True 

    def disable_badpixel(self)->None:
        self._sim.bad_pixel_state = True 

    def is_badpixel_enabled(self)->bool:
        return self._sim.bad_pixel_state 
    
    def build_bias(self):
        ...

    def is_bias_enabled(self):
        return self._sim.bias_state
    
    def enable_bias(self)->None:
        self._sim.bias_state = True 
    
    def disable_bias(self)->None:
        self._sim.bias_state = False 

    def get_image_buffer(self, start_index:int , end_index:int)->np.ndarray:
        if end_index < start_index:
            images = self._grabber.buffer.data[ start_index: self.get_buffer_size() ]
            images += self._grabber.buffer.data[ 0: end_index ]
        else:
            images = self._grabber.buffer.data[ start_index:end_index]
        return np.array(images)

    def get_single_image(self, index:int, mustProcess:bool  = False)->np.ndarray:
        if mustProcess:
            raise ValueError("Processed image is not implemented for the simulator")
        return self._grabber.buffer.data[index] 

    def upload_frames(self, frame_data):
        frame_data = np.asarray( frame_data ) 
        if len( frame_data.shape)>2: 
            for frame in frame_data:
                self._grabber.buffer.append(frame) 
        else:
            self._grabber.buffer.append(frame)

    def upload_raw_file(self, file_name: str):
        self.log.error("simulator cannot upload file to buffer")
    
    def get_sizes(self):
        cropEnabled, cropData =  self.get_cropping()
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


class RingBuffer:
    """ class that implements a not-yet-full buffer """
    def __init__(self, data, size_max):
        self.max = size_max
        self.data = data

    class __Full:
        """ class that implements a full buffer """
        def append(self, x):
            """ Append an element overwriting the oldest one. """
            self.data[self.cur] = x
            self.cur = (self.cur+1) % self.max
        def get(self):
            """ return list of elements in correct order """
            return self.data[self.cur:]+self.data[:self.cur]

    def append(self,x):
        """append an element at the end of the buffer"""
        self.data.append(x)
        if len(self.data) == self.max:
            self.cur = 0
            # Permanently change self's class from non-full to full
            self.__class__ = self.__Full

    def get(self):
        """ Return a list of elements from the oldest to the newest. """
        return self.data



if __name__ == "__main__":
    from ipag_cred2.setup import Cred2Setup
    c = Cred2Sim(); setup = Cred2Setup()
    setup.setup(c)
    c._sim.buffer_size = 6 
    print( c.acquire_n_pictures( 4).shape)
    print("------")
    print( c.acquire_n_pictures(4).shape)
    c.set_cropping( 0, 64, 0, 128)
    print( c.acquire_n_pictures( 4).shape)

    print( " ------------ " )

    print( c.set_sensor_temperature( 5) ) 
    c.set_temperature( 45) 
    # import inspect
    # for k,v in Cred2Sim.__dict__.items():
    #     if k.startswith("_"): continue 
    #     if hasattr( v, "__call__"):
    #         print( f"def {k}{inspect.signature(v)}:\n    ...")

