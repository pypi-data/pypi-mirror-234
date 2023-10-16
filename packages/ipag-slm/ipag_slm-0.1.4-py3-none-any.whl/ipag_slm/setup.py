from __future__ import annotations
from typing import Union
from ipag_core import ipag
from ipag_slm.define import SlmClientProtocol 

resource_path = ipag.ResourcePath(env="IPAG_RESOURCES", pkg_directories=["resources"], pkg_name="ipag_slm")

class SlmSetup(ipag.UserModel):
    lut: Union[str,int,None] = None
    """ If a  string, relative path to serources or absolute path 
    If a int, it is the wavelength in nano meter. In this case the 
    serial number should be set correctly 
    """
    switchon: bool = True
    """ should be True to switch on the hardware if not on  """
    
    def setup(self, client: SlmClientProtocol)->None:
        if self.switchon:
            client.switchon()

        if self.lut:
            if isinstance(self.lut, int):
                lut_file = f"slm{client.config.serial:04d}_at{self.lut:04d}.lut"
            else:
                lut_file = self.lut
            client.load_lut( resource_path.get_path( lut_file) ) 



if __name__ == "__main__":

    from ipag_slm.sim import SlmSim 
    slm = SlmSim() 
    s = SlmSetup(lut = 'slm5776_at1175.lut')
    s = SlmSetup(lut = 1175)
    s.setup(slm)
