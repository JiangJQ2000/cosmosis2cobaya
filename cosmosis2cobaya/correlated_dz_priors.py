from ._base import base

class correlated_dz_priors(base):
    
    def cosmosis_datablock_inputs(self):
        return ['nofz_shifts_kids']
    
    def cosmosis_datablock_outputs(self):
        return ['nofz_shifts_kids']
