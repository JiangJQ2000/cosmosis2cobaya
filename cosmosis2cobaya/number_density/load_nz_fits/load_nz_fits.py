from cosmosis2cobaya._base import base

class load_nz_fits(base):
    
    def cosmosis_datablock_inputs(self):
        return ['_cosmosis2cobaya._dummy']
    
    def cosmosis_datablock_outputs(self):
        config = self.module.data
        return list(config.keys())

class fits_nz(load_nz_fits):
    pass

class fits_nz_kids(load_nz_fits):
    pass

class fits_nz_des(load_nz_fits):
    pass
