from cosmosis2cobaya._base import base_Likelihood

class shear_ratio_likelihood(base_Likelihood):

    def cosmosis_datablock_inputs(self):
        lkl = self.module.data
        return [
            lkl.y_section,
        ]
    
    def cosmosis_datablock_outputs(self):
        return ['data_vector', 'likelihoods']

class shear_ratio_like(shear_ratio_likelihood):
    pass
