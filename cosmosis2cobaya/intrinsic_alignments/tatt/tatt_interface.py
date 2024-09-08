from cosmosis2cobaya._base import base

class tatt_interface(base):

    def cosmosis_datablock_inputs(self):
        return ['cosmological_parameters', 'matter_power_lin', 'matter_power_nl', 'fastpt', 'intrinsic_alignment_parameters']
    
    def cosmosis_datablock_outputs(self):
        return [
            'intrinsic_power',
            'intrinsic_power_ee',
            'intrinsic_power_bb',
            'matter_intrinsic_power',
            'intrinsic_alignment_parameters'
        ]

class IA(tatt_interface):
    pass

class IA2(tatt_interface):
    name = 'IA'
