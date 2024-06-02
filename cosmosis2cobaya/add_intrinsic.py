from ._base import base

class add_intrinsic(base):

    def cosmosis_datablock_inputs(self):
        return [
            'shear_cl_gi',
            'shear_cl_ii',
            'shear_cl'
        ]
    
    def cosmosis_datablock_outputs(self):
        return [
            'shear_cl_gg',
            'shear_cl',
        ]
