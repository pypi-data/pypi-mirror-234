from __future__ import annotations


from dataclasses import dataclass
from ipag_core import ipag
from ipag_core.define import MetadataLike

from ipag_slm.define import SlmClientProtocol
import numpy as np 


@dataclass
class SlmImageWriter(ipag.DataWriter):
    """ Writer for the slm """
    
    slmcl: SlmClientProtocol 
    """ slm client object """
    
    timeout_ms: int|None = None 
    """ optional timeout in ms. Used to wait the readiness for writing new data """
    
    def write(self, data: Any, metadata: MetadataLike | None = None) -> None:
        data = np.asanyarray( data )
        if data.dtype != np.dtype('uint8'):
            raise ValueError( f"expecting a uint8 image got a {data.dtype} " )
        self.slmcl.wait_write_completed(self.timeout_ms)  
        self.slmcl.write_image( data ) 
