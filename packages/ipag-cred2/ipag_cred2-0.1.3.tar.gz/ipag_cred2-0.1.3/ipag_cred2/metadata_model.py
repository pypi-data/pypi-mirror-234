from __future__ import annotations

from ipag_core import ipag
from ipag_cred2.define import  ConversionGain, Cred2Temperatures
from ipag_cred2.state import Cred2CameraState, Cred2DetState, Cred2HouseKeepingState, Cred2State, CropState

_MV = ipag.MetaVal
_MNV = ipag.MetaNamedVal

def _gd(ks):
    g = globals()
    return {k:g[k] for k in ks.split()}

motherboard = _MNV("TEMP1", "motherboard", "[c] temperature value", float, unit="C")
frontend =   _MNV("TEMP2", "frontend", "[c] temperature value", float, unit="C")
sensor =     _MNV("TEMP3", "sensor", "[c] temperature value", float, unit="C")
peltier =    _MNV("TEMP4", "peltier", "[c] temperature value", float, unit="C")
heatsink =   _MNV("TEMP5", "heatsink", "[c] temperature value", float, unit="C")

cmin = _MV("CMIN", "[pixel] Crop minimum Column", int)
cmax = _MV("CMAX", "[pixel] Crop maximum Column", int)
rmin = _MV("RMIN", "[pixel] Crop minimum Row", int)
rmax = _MV("RMAX", "[pixel] Crop maximum Row", int)
enabled = _MV("USED", "T if used", bool)
fps =     _MV('FPS',"[Hz] Frame Per Seconds", float)
tint = ipag.metadata_model.dit 
dit = tint 

conversion_gain = _MV( "CGAIN", "convserion gain low,medium,high", ipag.types.valueof(ConversionGain))
badpixel = _MV("BADPIX", "Usage of sensor badpixel", bool)
bias =     _MV("USEBIAS", "Usage of build bias", bool)
led =      _MV("LEDON", "T If LED is on", bool)
max_fps =  _MV("MAXFPS", "[Hz] Max Frame /per Seconds of camera", float)
min_fps =  _MV("MINFPS", "[Hz] Min Frame /per Seconds of camera", float)
min_tint = _MV("MINTINT", "[s] max integration time", float)
max_tint = _MV("MAXTINT", "[s] min integration time", float)
sensor_setpoint_temperature = _MV("TEMPSET" ,"[C] Temperature sensor setpoint", float)

temperatures = ipag.MetaObj(Cred2Temperatures, _gd("motherboard frontend sensor peltier heatsink"))
crop = ipag.MetaObj(CropState, _gd("cmin cmax rmin rmax enabled")) 

det = ipag.MetaObj(Cred2DetState, _gd("fps conversion_gain badpixel bias crop tint"), prefixes=dict(crop='CROP'))
house_keeping = ipag.MetaObj(Cred2HouseKeepingState, _gd("led sensor_setpoint_temperature temperatures")) 
camera = ipag.MetaObj(Cred2CameraState, _gd( "max_fps min_fps min_tint max_tint" ))

cred2 = ipag.MetaObj(Cred2State, _gd("det house_keeping camera"))

set_to_metadata = cred2.set_to_metadata
get_from_metadata = cred2.get_from_metadata


if __name__ == "__main__":
    det = Cred2DetState( fps=100, tint=0.002, crop = CropState( cmin=0, cmax=31, rmin=0, rmax=63) )
    
    

    m  = ipag.new_metadata()
    cred2.det.set_to_metadata( m , det) 
    hk =  Cred2HouseKeepingState(sensor_setpoint_temperature = -15.0, temperatures=[0.0]*5)
    house_keeping.set_to_metadata(m , hk)

    print( repr(m))
    print("---------------------------------")
    m  = ipag.new_metadata()
    s = Cred2State( det= det, house_keeping=hk, camera=dict(max_fps=600.0, min_fps=0, max_tint=1, min_tint=0.0) )
    set_to_metadata( m, s, "DET1") 
    print(repr(m))
    print(get_from_metadata ( m, "DET1" ) )

    print("---------------------------------")
    m = ipag.new_metadata()
    cred2.det.set_to_metadata ( m , {'fps':120, 'tint':1/120., 'hoho':3.0}) 
    print(repr(m))

    print("---------------------------------")
    print( cred2.house_keeping.temperatures.frontend) 



