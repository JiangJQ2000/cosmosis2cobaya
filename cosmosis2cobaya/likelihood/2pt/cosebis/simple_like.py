from cosmosis2cobaya._base import base_Likelihood

class simple_like(base_Likelihood):
    
    def cosmosis_datablock_inputs(self):
        return ['cosebis']
    
    def cosmosis_datablock_outputs(self):
        return ['data_vector', 'likelihoods']

class cosebis_like(simple_like):
    pass
