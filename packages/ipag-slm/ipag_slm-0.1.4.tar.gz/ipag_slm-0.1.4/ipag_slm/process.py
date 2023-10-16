from __future__ import annotations


from dataclasses import dataclass
from typing import Callable
from ipag_core import ipag
import numpy as np


def _get_min_and_max( data, cuts):
    if hasattr( cuts, "__call__"):
            vmin, vmax = cuts(data)
    else:
        vmin, vmax = cuts 
    if vmin is None:
        vmin = np.min(data) 
    if vmax is None:
        vmax = np.max(data) 
    return vmin, vmax 


@dataclass
class BmpConvertor(ipag.DataProcessor):
    """ Simple BmpConvertor from any incoming data 
    
    $$ bmp = (fill-offset)/(vmax-vmin) * (data-vmin) + offset $$

    Where fill and offset are 255 and 0 by default

    Exemple::

        image_writer = ipag.DataPipe( BmpConvertor( cuts=(0, 2*np.pi)), slm.SlmImageWriter(slmcl) )

        np.ones( )

    """

    cuts : tuple[float,float] | Callable  = (None, None)
    """ optional (min,max) cuts for the incoming data 
    if None they are respectively min and max of the data. 
    
    (min, max) values will be (offset, fill) i.e. (0,255) BMP by default 

    Cuts can also be a function of signature f(data)->(min,max)
    """
    
    crop: bool = False  
    """ If True, values bellow min are copped to min(->0 BPM) 
    and value above max are cut to max(->255 BMP) 
    If False (default) values are wrapped with a preiod p=max-min with 
    discontinuity in the BMP ( e.i. 256 is 0 257 is 1 etc .. ).  
    """
    
    fill: int = 255 
    """ fill the value, basicaly the vmax data will converted to fill BMP 
    """

    offset: int = 0 
    """ Offset value. The min of data will be converted to offset  """

    def process(self, data, metadata=None) -> np.ndarray:
        data = np.asarray(data)
        vmin, vmax = _get_min_and_max(data, self.cuts)
         

        scale =  (self.fill-self.offset)/(vmax-vmin)
        
        bmp = scale * (data-vmin) + self.offset
        if self.crop:
            bmp_min = self.offset 
            bmp_max = self.fill 
            if bmp.shape:
                bmp[bmp<bmp_min] = bmp_min
                bmp[bmp>bmp_max] = bmp_max
            else:
                bmp = max( min( bmp, bmp_max), bmp_min) 
        return bmp.astype('uint8')



if __name__=="__main__":

    c = BmpConvertor( cuts=(0,255), crop=True )

    assert np.max( c.process([10]) ) == 10  
    assert np.max( c.process([256]) ) == 255 
    
    
