from __future__ import annotations
import os
from ipag_slm.define import SlmClientProtocol, SlmConfig, slm_config
from ipag_slm.sim import SlmSim

from ipag_slm.state import SlmState 
from ipag_slm.setup import SlmSetup
from ipag_slm import metadata_model

from ipag_slm.io import SlmImageWriter 



def new_slm_client( config: SlmConfig = slm_config, simulate=False, dll_path: str|None=None)->SlmClientProtocol:
    if simulate:
        return SlmSim( config)
    else:
        if dll_path:
            os.add_dll_directory(dll_path)
        from ipag_slm.client import SlmClient
        return SlmClient( config )

