from cosmosis2cobaya._base import base

class fast_pt_interface(base):
    
    def cosmosis_datablock_inputs(self) -> list[str]:
        return ['matter_power_lin', 'matter_power_nl']
    
    def cosmosis_datablock_outputs(self):
        return ['fastpt']

class fast_pt(fast_pt_interface):
    pass
