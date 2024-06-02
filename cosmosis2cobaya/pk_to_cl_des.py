from ._base import base

class pk_to_cl_des(base):

    def cosmosis_datablock_inputs(self):
        return [
            'cosmological_parameters',
            'distances',
            'intrinsic_power',
            'intrinsic_power_ee',
            'intrinsic_power_bb',
            'matter_intrinsic_power',
            'matter_power_nl',
            'nz_source_des',
        ]
    
    def cosmosis_datablock_outputs(self):
        return [
            'shear_cl_gi',
            'shear_cl_ii',
            'shear_cl_bb',
            'shear_cl'
        ]
