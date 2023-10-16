from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
import numpy as np
import time

from ipag_core import ipag

from ipag_cred2.define import Cred2ClientProtocol
from ipag_cred2.metadata_model import cred2 as cred2_model

@dataclass
class Cred2FrameReader:
    """ Read Only IO taking images from cred2 

    Attribute:
        cred2_client: client to communicate with the cred2
        ndit (int): number of images to aquire  
    """
    cred2: Cred2ClientProtocol
    ndit: int = 1
    
    
    def read(self, metadata: ipag.MetadataLike|None = None)->np.ndarray:
        c = self.cred2 

        c.enable_grabber( self.ndit )
        start_frame_index = c.get_buffer_filling()

        c.start_aquisition() 
        time.sleep(1e-4)
        if c.is_grabber_enabled():
            while not c.is_grabber_finished():
                time.sleep(1e-5)
            c.disable_grabber()
        c.stop_aquisition()
            
        bufFilling = c.get_buffer_filling()
        img_array = c.get_image_buffer(start_frame_index, bufFilling)
        # make sure we are returning the ndit last
        # the first extra frame can be an old one 
        img_array = img_array[-self.ndit:]
        if metadata is not None:
            ipag.metadata_model.ndit.set_to_metadata( metadata, self.ndit)
            ipag.metadata_model.datetime.set_to_metadata( metadata, datetime.now())
        return img_array



if __name__ == "__main__":
    from ipag_cred2.sim import Cred2Sim 
    c = Cred2Sim()
    exp = Cred2FrameReader(c,  ndit = 4 )
    metadata = ipag.new_metadata()
    data = exp.read(metadata=metadata)
    print(  data.shape )
    print( repr( metadata) )
