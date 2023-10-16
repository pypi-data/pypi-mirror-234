""" This is the API for cred2 

The client is not imported in this API. This is to be abble to use the 
simulator from the API if Sdk libraries are not installed 
"""

from typing import Union
from ipag_cred2.define import (
    Cred2Temperatures, 
    Cred2ClientProtocol, 
    Cred2Error, 
    Cred2Config, 
    ConversionGain,
    cred2_config
)

from ipag_cred2.sim import Cred2Sim

from ipag_cred2.setup import (
        CropSetup, 
        CropPosSetup, 
        Cred2DetSetup, 
        Cred2HouseKeepingSetup, 
        Cred2Setup,
        Cred2FlatSetup, 
        Cred2ExposureSetup,
    )

from ipag_cred2.state import (
    Cred2DetState, 
    Cred2HouseKeepingState, 
    Cred2CameraState, 
    Cred2State
)

from ipag_cred2.io import Cred2FrameReader

from ipag_cred2 import metadata_model
cred2_metadata_model = metadata_model


def new_cred2_client(
        config :Cred2Config = cred2_config, 
        simulate: bool =False, 
        sdk_path: str = ""
    )->Cred2ClientProtocol:
    """ Build a new cred2 client 

    Args:
        config: optional, default cred2 client config
        simulate: If True return a simulator
        sdk_path: If Path to FLI SDK is not added to the system
            This can be fixed here. If given it will be added to 
            the sys.path if not present.
    """
    if simulate: 
        return Cred2Sim(config)
    else:
        if sdk_path:
            import sys 
            if not sdk_path in sys.path:
                sys.path.append(sdk_path)
        from ipag_cred2.client import Cred2Client
        return Cred2Client(config)
new_client = new_cred2_client 

# Automatically Alias all class starting with Cred2
__g__ = globals()
for __k__, __v__ in list(__g__.items()):
    if __k__.startswith("Cred2"):
        __g__[__k__[5:]] = __v__ 
del __g__, __k__, __v__

