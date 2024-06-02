from ._base import base

class photoz_bias_des(base):
    
    def cosmosis_datablock_inputs(self):
        config = self.module.data
        pz = config['sample']
        # biases = config['bias_section']
        # return [pz, biases, ]
        return [
            pz,
            'wl_photoz_errors_des',
        ]
    
    def cosmosis_datablock_outputs(self):
        config = self.module.data
        pz = config['sample']
        return [config["output_deltaz_section_name"], pz]
