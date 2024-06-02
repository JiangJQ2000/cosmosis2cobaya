from cosmosis2cobaya._base import base

class photoz_bias(base):
    
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

class source_photoz_bias(photoz_bias):
    pass

class lens_photoz_bias(photoz_bias):
    pass
