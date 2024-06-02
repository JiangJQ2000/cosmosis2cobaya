from ._base import base

class cosebis(base):
    
    def cosmosis_datablock_inputs(self):
        return ['shear_cl']
    
    def cosmosis_datablock_outputs(self):
        return ['cosebis']
