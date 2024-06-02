from ._base import base

class fast_pt(base):
    
    def cosmosis_datablock_inputs(self) -> list[str]:
        return ['matter_power_lin', 'matter_power_nl']
    
    def cosmosis_datablock_outputs(self):
        return ['fastpt']
