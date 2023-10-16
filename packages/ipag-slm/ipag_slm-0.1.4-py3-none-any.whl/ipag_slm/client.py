from __future__ import annotations
from logging import getLogger
from re import A

from ipag_slm.define import SlmClientProtocol, SlmConfig,  slm_config, SlmError
import numpy as np 
import ctypes



ctypes.cdll.LoadLibrary("Blink_C_wrapper")
SlmSdk = ctypes.CDLL("Blink_C_wrapper")
# change the return type of Get_last_error_message (this is not a int, but char)
SlmSdk.Get_last_error_message.restype = ctypes.c_char_p
SlmSdk.Read_SLM_temperature.restype = ctypes.c_double


class SlmClient(SlmClientProtocol):
    
    log = getLogger(slm_config.logger)

    _board: ctypes.c_int = None 
    """ board number (None when connection is not established) """
    
    _shape = None

    def __init__(self, config: SlmConfig = slm_config):
        self.config = config 
    
    def is_on(self)->bool:
        return self._board is not None

    def write_image(self, img: np.ndarray, wait_for_trigger: bool = False, timeout: int | None = None)->None:
        timeout = self.config.default_timeout if timeout is None else timeout
            
        w, h = img.squeeze().shape  
        if w == 512: 
            size = 512 
        else:
            size = w*h # should be 1920x1152 
            if size!= (1920*1152):
                raise ValueError(f"input images should be of shape 512x521 for small slm or 1920x1152 got {img.shape} ")
         
        pulse = ctypes.c_uint(0)
        pulse_refresh = ctypes.c_uint(0) 

        image_pointer = img.ctypes.data_as( ctypes.POINTER( ctypes.c_ubyte))
        wait_for_trigger = ctypes.c_uint(1) if wait_for_trigger else ctypes.c_uint(0)
        timeout = ctypes.c_uint( timeout )
        # TODO  check the pulse_refresh, could not find it on manual 
        if SlmSdk.Write_image( 
            self._board, image_pointer, 
            wait_for_trigger, pulse, pulse_refresh, timeout 
        ):
            raise SlmError( f"Write image failed: last SLM error {self.get_last_error()}")


    
    def switchon(self, board_number: int | None = None)->None:
        
        self.log.info('Switchon ON SLM ...')
        board_number = self.config.board_number if board_number is None else board_number
        # Call the Create_SDK constructor
        # Returns a handle that's passed to subsequent SDK calls

        bit_depth = ctypes.c_uint(self.config.model.properties.bit_depth) 
        # TODO: Check stype of is_nematic_type 
        is_nematic_type = ctypes.c_bool(  self.config.model.properties.nematic_type )
        number_of_boards_found = ctypes.c_uint(0)
        constructed_okay = ctypes.c_int(-1)

        ram_write_enable = ctypes.c_bool(self.config.ram_write_enable) 
        use_gpu = ctypes.c_bool( self.config.use_gpu)
        max_transiant_frame = ctypes.c_int( self.config.max_transiant_frame) 

        SlmSdk.Create_SDK(
                bit_depth,
                ctypes.byref(number_of_boards_found), 
                ctypes.byref(constructed_okay), 
                is_nematic_type, 
                ram_write_enable, 
                use_gpu, 
                max_transiant_frame, 
                0, # TODO: Check this, manual says it needs a regional LUT file 
            )
        if not constructed_okay.value :
            try:
                error = SlmSdk.Get_last_error_message()
            except Exception:
                error = "Unknown error"
            
            self.log.error(f'Blink SDK did not construct successfully: {error}')
            raise SlmError(f' when creating SDK: {error}')
        
        n_board_found: int = number_of_boards_found.value 
        if board_number is not None:
            if board_number>=n_board_found:
                raise ValueError(f"provided board number is {board_number} however only {n_board_found} board was found")
        else:
            if n_board_found>1:
                raise ValueError(f"More than one board was found ({n_board_found}). Please provide a board number")
            board_number = 1
        
        self.log.info('Blink SDK was successfully constructed')
        self.log.info(f'Board number set to {board_number}')
        self._board = ctypes.c_uint8( board_number )
    
    def switchoff(self):
        SlmSdk.Delete_SDK()
        self._board = None 
         
    def __del__(self):
        try:
            self.switchoff()
        except Exception:
            pass
    
    @staticmethod
    def get_last_error():
        return SlmSdk.Get_last_error_message()
        
    def wait_write_completed(self, timeout_ms:int|None = None) -> bool:
        if timeout_ms is None:
            timeout_ms = self.config.default_timeout

        c_timeout = ctypes.c_uint(timeout_ms)
        # TODO check the return 
        if SlmSdk.ImageWriteComplete(self._board, c_timeout):
            raise SlmError(f"timeout after {timeout_ms}ms. Last SLM Error {self.get_last_error()}")
 
    def get_temperature(self)->float:
        return SlmSdk.Read_SLM_temperature(self._board)
        
    def turn_power_on(self)->None:
        return SlmSdk.SLM_power(ctypes.c_bool(1))
    
    def turn_power_off(self)->None:
        return SlmSdk.SLM_power(ctypes.c_bool(0))
    
    def load_lut(self, filename:str)->None:
        status = SlmSdk.Load_LUT_file(self._board, bytes(filename, encoding='utf-8'))        
        if status:
            raise SlmError( f"Cannot load LUT {filename!r}" )
        else:
            self.log.info(f'lookup table {filename} loaded')
    
    def get_shape(self) -> tuple[float, float]:
        if self._shape is None:
            h = SlmSdk.Get_image_height(self._board)
            w = SlmSdk.Get_image_width(self._board) 
            self._shape = (h,w)
        return self._shape
