from ._base import base

class fits_nz(base):
    
    def cosmosis_datablock_inputs(self):
        return ['_cosmosis2cobaya._dummy']
    
    def cosmosis_datablock_outputs(self):
        config = self.module.data
        return list(config.keys())
