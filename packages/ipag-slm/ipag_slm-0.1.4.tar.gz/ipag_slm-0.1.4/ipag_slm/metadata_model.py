
from ipag_core import ipag
from ipag_slm.state import SlmState

temperature = ipag.MetaVal( 'TEMP', '[C] Slm temperature', float)

slm = ipag.MetaObj(  SlmState, {'temperature':temperature})



if __name__ == "__main__":
    from ipag_slm.sim import SlmSim
    h = ipag.new_metadata()
    slmcl  = SlmSim()
    state = SlmState()
    state.update( slmcl )

    slm.set_to_metadata( h, state, "SLM")
    print(repr(h))
