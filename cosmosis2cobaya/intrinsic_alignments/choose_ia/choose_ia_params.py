from cosmosis2cobaya._base import base

class choose_ia_params(base):

    def cosmosis_datablock_inputs(self):
        return [
            'intrinsic_alignment_parameters'
        ]
    
    def cosmosis_datablock_outputs(self):
        return [
            'intrinsic_alignment_parameters',
        ]

class choose_des_ia(choose_ia_params):
    pass

class choose_kids_ia(choose_ia_params):
    pass
