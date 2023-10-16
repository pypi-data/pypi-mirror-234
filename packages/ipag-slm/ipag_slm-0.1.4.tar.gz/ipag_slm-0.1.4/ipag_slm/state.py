import math
from ipag_core import ipag
from ipag_slm.define import SlmClientProtocol 


class SlmState(ipag.StateModel):
    temperature: float = math.nan 
    """[C] Slm temprature """

    def update(self, slm: SlmClientProtocol)->None:
        self.temperature = slm.get_temperature()

    
