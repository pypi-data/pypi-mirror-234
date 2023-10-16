from __future__ import annotations
from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional
from pydantic import BaseModel
from typing_extensions import Protocol
import numpy as np 
from ipag_core.dev_tools import deprecated 


@dataclass
class ModelProperties:
    """ Class holding properties of given Slm Model """
    shape: tuple[int,int]
    
    bit_depth: int 

    nematic_type: int  
    """ 1=>SLMs with Nematic Liquid Crystal. 0=> SLMs with Ferroelectric Liquid Crystal """
    
    

class SlmModel(str, Enum):
    SLM_L512 = 'L512'
    SLM_S512 = 'S512'
    SLM_1920x1152 = '1920x1152'

SlmModel.SLM_L512.properties = ModelProperties( (512,512) , 16, 1)
SlmModel.SLM_S512.properties = ModelProperties( (512,512) , 8, 1) 
SlmModel.SLM_1920x1152.properties = ModelProperties( (1152,1920), 12, 1) 

class SlmConfig(BaseModel):
    model: SlmModel = SlmModel.SLM_1920x1152 
    """ SLM model, enumerator containing model's dependent properties """
    
    logger: str = "ipag.slm"
    """ Logger path name """
    
    default_timeout: int = 5000 
    """ [ms] default timeout used when waiting for a trigger signal """
    
    ram_write_enable: bool = True 
    """ ram write minimize the CPU to PCIe image transfert time. Should be True """
    
    use_gpu: bool = True 
    """ if True Computation on transient frame are done on GPU if possible """
    
    max_transiant_frame: int = 10 
    """ see doc. this parameter is related toLC response and system frame rate"""
    
    board_number: Optional[int] = None
    """ Used when several board are connected. Set the targeted board.
    None is the same than one except that an error is raised if several board 
    are detected 
    """
    serial: int = 5776  
    """ serial number of the slm (used to find lut file from a wavelenght number) """
    

slm_config = SlmConfig()

class SlmError(RuntimeError):
    pass



class SlmClientProtocol(Protocol):
    
    @abstractmethod
    def write_image(self, 
       img: np.ndarray, 
       wait_for_trigger: bool = False, 
       timeout: int | None = None
    )->None:
        """ Write a new image to the slm 

        Args:
            img: numpy array of type uint8  (BMP)
            wait_for_trigger: If True function blocks until an external trigger 
                (TTL pulse) is sent to the slm 
            timeout: Timeout in ms used when an externel trigger is activated
                but wasn't receive during timeout. If None the defaul timeout 
                is used
        """
        ...
    
    @abstractmethod
    def is_on(self)->bool:
        """ True if the SLM client "is_on" """
        ...

    # TODO: switchon is probably not a good name: init, enable, startup ?
    @abstractmethod
    def switchon(self, board_number: int | None = None)->None:
        """ Switch the SLM client connection on 
        
        Args:
            board_number (optional): Must be provided if several board are found. 
                board id number starts from 1
                If only one board is connected this can be left None (first one). 

        Raises:
            ValueError: 
                - If board_number is None and several board are found.            
                - If the borad_number exceed the number of board found
        """
        ...
        
    @abstractmethod
    def wait_write_completed(self,  timeout:int|None = None)-> None:
        """ Wait the last image writing has been completed 
        
        Args:
            timeout_ms : timeout in ms. Use config.default_timeout if None
        """
        ...
    
    @abstractmethod
    def get_temperature(self)->float:
        """ get the slm current temperature """
        ...
    
    @abstractmethod
    def turn_power_on(self)->None:
        """ turn SLM on """
        ...
    
    @abstractmethod
    def turn_power_off(self)->None:
        """ turn SLM off """
        ...
    

    @abstractmethod
    def load_lut(self, filename:str)->None:
        """ load a loockup table file on the SLM 
    
        Args:
            filename: loockup table file path 
        """
        ...

    @abstractmethod
    def get_shape(self)->tuple[float, float]:
        """ Return the (n_rows, n_columns) shape 
        Of the SLM 
        """
        ... 


    # DEPRECATED METHODS 
    @deprecated("use is_write_completed instead")
    def write_image_complete(self):
        return self.wait_write_completed()
    
    @deprecated("use set_power_on or set_power_off instead")
    def set_power(self, p:bool):
        if p:
            self.turn_power_on()
        else:
            self.turn_power_off()
        return self.is_write_completed()

    


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


