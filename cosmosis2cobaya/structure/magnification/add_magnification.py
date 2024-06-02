from cosmosis2cobaya._base import base

class add_magnification(base):

    def cosmosis_datablock_inputs(self):
        config = self.module.data
        do_galaxy_galaxy, do_galaxy_shear, do_galaxy_cmbkappa, include_intrinsic = config
        ret = []
        if do_galaxy_galaxy:
            ret += ['galaxy_cl', 'galaxy_magnification_cl', 'magnification_cl']
        if do_galaxy_shear:
            ret += ['galaxy_shear_cl', 'magnification_shear_cl', 'magnification_intrinsic_cl']
        if do_galaxy_cmbkappa:
            ret += ['galaxy_cmbkappa_cl', 'magnification_cmbkappa_cl']
        return ret
    
    def cosmosis_datablock_outputs(self):
        config = self.module.data
        do_galaxy_galaxy, do_galaxy_shear, do_galaxy_cmbkappa, include_intrinsic = config
        ret = []
        if do_galaxy_galaxy:
            ret += ['galaxy_cl', 'galaxy_cl_gg']
        if do_galaxy_shear:
            ret += ['galaxy_shear_cl', 'galaxy_shear_cl_gg']
        if do_galaxy_cmbkappa:
            ret += ['galaxy_cmbkappa_cl_gk', 'galaxy_cmbkappa_cl']
        return ret

