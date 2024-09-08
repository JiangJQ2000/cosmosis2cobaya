from cosmosis2cobaya._base import base

class cl_to_cosebis_interface(base):
    
    def cosmosis_datablock_inputs(self):
        return ['shear_cl']
    
    def cosmosis_datablock_outputs(self):
        return ['cosebis']

class cosebis(cl_to_cosebis_interface):
    pass
