from cosmosis2cobaya._base import base

class add_gammat_point_mass(base):
    want_B_section = True

    def cosmosis_datablock_inputs(self):
        config = self.module.data
        ret = [config['lens_nz_section'], config['source_nz_section']]

        if not config['use_fiducial']:
            ret += ['cosmological_parameters', 'distances']
        if config['add_togammat']:
            ret += ['galaxy_shear_xi', config["gammat_section"]]
        if self.want_B_section:
            ret += [config['B_section'], ]
        return ret
    
    def cosmosis_datablock_outputs(self):
        config = self.module.data
        ret = [config["sigcrit_inv_section"], ]

        if config['add_togammat']:
            ret += [config["gammat_section"], 'point_mass']
        return ret

class add_point_mass(add_gammat_point_mass):
    pass
