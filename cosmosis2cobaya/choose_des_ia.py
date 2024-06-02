from ._base import base

class choose_des_ia(base):

    def cosmosis_datablock_inputs(self):
        return [
            'intrinsic_alignment_parameters'
        ]
    
    def cosmosis_datablock_outputs(self):
        return [
            'intrinsic_alignment_parameters',
        ]
