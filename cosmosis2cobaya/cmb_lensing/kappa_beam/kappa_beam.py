from cosmosis2cobaya._base import base

class kappa_beam(base):
    want_galkappa = True
    want_shearkappa = True
    want_kappakappa = True

    def cosmosis_datablock_inputs(self):
        config = self.module.data
        shearkappa_section = config['shearkappa_section']
        galkappa_section = config['galkappa_section']
        kappakappa_section = config['kappakappa_section']
        shearkappa_output_section = config['shearkappa_output_section']
        galkappa_output_section = config['galkappa_output_section']
        kappakappa_output_section = config['kappakappa_output_section']
        beam_sigma = config['beam_sigma']
        save_name = config['save_name']

        ret = []
        if self.want_galkappa:
            ret.append(galkappa_section)
        if self.want_shearkappa:
            ret.append(shearkappa_section)
        if self.want_kappakappa:
            ret.append(kappakappa_section)
        
        return ret
    
    def cosmosis_datablock_outputs(self):
        config = self.module.data
        shearkappa_section = config['shearkappa_section']
        galkappa_section = config['galkappa_section']
        kappakappa_section = config['kappakappa_section']
        shearkappa_output_section = config['shearkappa_output_section']
        galkappa_output_section = config['galkappa_output_section']
        kappakappa_output_section = config['kappakappa_output_section']
        beam_sigma = config['beam_sigma']
        save_name = config['save_name']

        ret = []
        if self.want_galkappa:
            ret.append(galkappa_output_section)
        if self.want_shearkappa:
            ret.append(shearkappa_output_section)
        if self.want_kappakappa:
            ret.append(kappakappa_output_section)
        
        return ret

class beam_kappa_spt(kappa_beam):
    pass

class beam_kappa_planck(kappa_beam):
    pass
