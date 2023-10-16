from __future__ import annotations
from dataclasses import dataclass, field
from functools import partial
from logging import getLogger
from ipag_slm.define import SlmClientProtocol, SlmConfig,  slm_config  
import numpy as np 

def zeros()->np.ndarray:
    """ zero image for the SLM  """
    return np.zeros(slm_config.model.properties.shape, 'uint8') 

@dataclass
class SimParameters:
    image: np.ndarray = field( default_factory = zeros )
    temperature: float = 0.0
    power: bool = True 
    
class SlmSim(SlmClientProtocol):
    
    log = getLogger(slm_config.logger)

    def __init__(self, config: SlmConfig = slm_config):
        self.config = config 
        self._sim = SimParameters() 
    
    def is_on(self)->bool:
        return True 
        
    def write_image(self, img: np.ndarray, wait_for_trigger: bool = False, timeout: int | None = None)->None:
        self._sim.image = img
    
    def get_shape(self) -> tuple[float, float]:
        return self._sim.image.shape   
        
    def switchon(self, board_number: int | None = None) -> None:
        return None 

    def wait_write_completed(self, timeout:int|None = None) -> None:
        ... 
    
    def get_temperature(self) -> float:
        return self._sim.temperature
    
    def turn_power_on(self)->None:
        self._sim.power = True 
    
    def turn_power_off(self)->None:
        self._sim.power = True 
    
    def load_lut(self, filename:str)->None:
        pass
    
if __name__ == "__main__":
    SlmSim()
