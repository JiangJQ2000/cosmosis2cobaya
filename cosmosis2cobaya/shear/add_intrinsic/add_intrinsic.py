from cosmosis2cobaya._base import base

class add_intrinsic(base):
    want_intrinsic_intrinsic_bb = True

    def cosmosis_datablock_inputs(self):
        config = self.module.data
        do_shear_shear, do_position_shear, do_shear_cmbkappa, perbin, sec_names = config

        shear_shear = sec_names['shear_shear']
        shear_shear_bb = sec_names['shear_shear_bb']
        shear_shear_gg = sec_names['shear_shear_gg']
        galaxy_shear = sec_names['galaxy_shear']
        galaxy_intrinsic = sec_names['galaxy_intrinsic']
        shear_intrinsic = sec_names['shear_intrinsic']
        parameters = sec_names['parameters']
        intrinsic_intrinsic = sec_names['intrinsic_intrinsic']
        intrinsic_intrinsic_bb = sec_names['intrinsic_intrinsic_bb']
        shear_cmbkappa = sec_names['shear_cmbkappa']
        intrinsic_cmbkappa = sec_names['intrinsic_cmbkappa']

        ret = []
        if do_shear_shear:
            ret += [shear_shear, intrinsic_intrinsic, shear_intrinsic]
            if self.want_intrinsic_intrinsic_bb:
                ret.append(intrinsic_intrinsic_bb)
        if do_position_shear:
            ret += [galaxy_intrinsic]
        if do_shear_cmbkappa:
            ret += [shear_cmbkappa, intrinsic_cmbkappa]
        if do_position_shear:
            ret += [galaxy_shear]
        
        if perbin:
            ret += [parameters]
        
        return ret
    
    def cosmosis_datablock_outputs(self):
        config = self.module.data
        do_shear_shear, do_position_shear, do_shear_cmbkappa, perbin, sec_names = config

        shear_shear = sec_names['shear_shear']
        shear_shear_bb = sec_names['shear_shear_bb']
        shear_shear_gg = sec_names['shear_shear_gg']
        galaxy_shear = sec_names['galaxy_shear']
        galaxy_intrinsic = sec_names['galaxy_intrinsic']
        shear_intrinsic = sec_names['shear_intrinsic']
        parameters = sec_names['parameters']
        intrinsic_intrinsic = sec_names['intrinsic_intrinsic']
        intrinsic_intrinsic_bb = sec_names['intrinsic_intrinsic_bb']
        shear_cmbkappa = sec_names['shear_cmbkappa']
        intrinsic_cmbkappa = sec_names['intrinsic_cmbkappa']

        ret = []
        if do_shear_shear:
            ret += [shear_shear_gg, shear_shear]
            if self.want_intrinsic_intrinsic_bb:
                ret.append(shear_shear_bb)
        if do_position_shear:
            ret.append(galaxy_shear)
        if do_shear_cmbkappa:
            ret.append(shear_cmbkappa)
        
        return ret
