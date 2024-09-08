import os, importlib, sys
from pathlib import Path
import numpy as np
from cosmosis2cobaya._base import base_Likelihood

class TwoPointLikelihood(base_Likelihood):
    name = '2pt_like_mass'
    
    def cosmosis_datablock_inputs(self):
        root_directory = os.getenv('COSMOSIS_ROOT_DIRECTORY')
        sys.path.insert(0, Path(root_directory) / 'likelihood/2pt')
        from twopoint_cosmosis import theory_names

        lkl = self.module.data
        if len(lkl.suffixes) == 1:
            suffixes = np.tile(lkl.suffixes[0], len(lkl.two_point_data.spectra))
        elif len(lkl.suffixes) > 1 and len(lkl.suffixes) == len(lkl.two_point_data.spectra):
            suffixes = lkl.suffixes
        
        ret = []
        for spectrum, suffix in zip(lkl.two_point_data.spectra, suffixes):
            section, x_name, y_name = theory_names(spectrum)
            section += suffix
            ret.append(section)
        
        if lkl.do_pm_marg or lkl.do_smallscale_marg:
            if lkl.gammat_name in lkl.used_names:
                if (lkl.do_smallscale_marg) or (lkl.do_pm_sigcritinv and lkl.do_pm_marg):
                    ret.append(lkl.sigma_crit_inv_section)

        return ret
    
    def cosmosis_datablock_outputs(self):
        return ['data_vector', 'likelihoods']

class TwoPt_point_mass(TwoPointLikelihood):
    name = '2pt_like'
