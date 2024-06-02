import abc
from cosmosis2cobaya._base import base

class project_2d(base, metaclass=abc.ABCMeta):
    # TODO

    @abc.abstractmethod
    def cosmosis_datablock_inputs(self):
        ...
    
    @abc.abstractmethod
    def cosmosis_datablock_outputs(self):
        ...

# only valid for des-y3-6x2pt

class pk_to_cl_gg(project_2d):
    def cosmosis_datablock_inputs(self):
        return [
            'cosmological_parameters',
            'bias_lens',
            'distances',
            'matter_power_lin',
            'matter_power_nl',
            'nz_lens',
        ]
    def cosmosis_datablock_outputs(self):
        return [
            'galaxy_cl',
        ]

class pk_to_cl(project_2d):
    def cosmosis_datablock_inputs(self):
        return [
            'cosmological_parameters',
            'bias_lens',
            'mag_alpha_lens',
            'distances',
            'matter_power_nl',
            'matter_power_nl',
            'nz_lens',
            'nz_source',
            'intrinsic_power_bb',
            'matter_intrinsic_power',
            'intrinsic_power',
        ]
    def cosmosis_datablock_outputs(self):
        return ['cmbkappa_cl', 'galaxy_cmbkappa_cl', 'galaxy_intrinsic_cl', 'galaxy_magnification_cl', 'galaxy_shear_cl', 'intrinsic_cmbkappa_cl', 'magnification_cl', 'magnification_cmbkappa_cl', 'magnification_intrinsic_cl', 'magnification_shear_cl', 'shear_cl', 'shear_cl_bb', 'shear_cl_gi', 'shear_cl_ii', 'shear_cmbkappa_cl']
