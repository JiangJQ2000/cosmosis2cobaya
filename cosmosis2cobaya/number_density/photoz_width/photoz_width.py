from cosmosis2cobaya._base import base

class photoz_width(base):
    
    def cosmosis_datablock_inputs(self):
        config = self.module.data
        mode = config['mode']
        pz = config['sample']
        interpolation = config['interpolation']
        biases = config['bias_section']
        return [pz, biases]
    
    def cosmosis_datablock_outputs(self):
        config = self.module.data
        mode = config['mode']
        pz = config['sample']
        interpolation = config['interpolation']
        biases = config['bias_section']
        return [pz,]

class lens_photoz_width(photoz_width):
    pass
