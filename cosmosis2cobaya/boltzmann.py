import numpy as np
from typing import Mapping, Iterable
from cobaya.likelihood import Likelihood
from cobaya.theory import Theory
from cobaya.model import as_requirement_list
import cosmosis.datablock
import cosmosis.runtime.module
import cosmosis.runtime.config
from cosmosis.runtime.pipeline import config_to_block, PIPELINE_INI_SECTION

class boltzmann(Theory):
    renames_output = {}
    zmin = 0.
    zmax = 3.01
    nz = 150
    zmin_background = 0.
    zmax_background = None # = zmax
    nz_background = None # = nz
    n_logz = 0
    zmax_logz = 1100.
    zmid = None
    nz_mid = None
    same_k_grid = False # set True can make FAST-PT faster (due to different unit of k between cobaya and cosmoSIS)
    # the followings make sense only if same_k_grid = True
    nk = 200
    kmax = 10. # 1/Mpc
    want_chistar = False
    want_zstar = False

    def initialize(self):
        if self.zmax_background is None:
            self.zmax_background = self.zmax
        if self.nz_background is None:
            self.nz_background = self.nz
        self.z_background = np.linspace(self.zmin_background, self.zmax_background, self.nz_background)
        log_z = np.geomspace(self.zmax_background, self.zmax_logz, num=self.n_logz)
        self.z_background = np.append(self.z_background, log_z[1:])
    
    def get_requirements(self):
        ret = {
            'H0': None,
            'omegam': None,
            'comoving_radial_distance': {'z': self.z_background},
        }
        if self.want_zstar:
            ret['zstar'] = None
        if self.want_chistar:
            ret['CAMBdata'] = None
        if self.same_k_grid:
            self.Pk_interpolator_z = np.concatenate((
                np.linspace(self.zmin, self.zmid, self.nz_mid, endpoint=False),
                np.linspace(self.zmid, self.zmax, self.nz-self.nz_mid),
            )) if self.zmid is not None else np.linspace(self.zmin, self.zmax, self.nz)
            ret['Pk_interpolator'] = {
                'z': self.Pk_interpolator_z,
                'k_max': self.kmax, # 1/Mpc, allow H0 up to 100
                'nonlinear': [True, False],
            }
        else:
            ret['Pk_grid'] = {
                'z': np.concatenate((
                    np.linspace(self.zmin, self.zmid, self.nz_mid, endpoint=False),
                    np.linspace(self.zmid, self.zmax, self.nz-self.nz_mid),
                )) if self.zmid is not None else
                np.linspace(self.zmin, self.zmax, self.nz),
                'k_max': self.kmax, # 1/Mpc, allow H0 up to 100
                'nonlinear': [True, False]
            }
        return ret
    
    def get_can_provide(self):
        return [self.renames_output.get(i, i).lower() for i in (
            'cosmological_parameters',
            'distances',
            'matter_power_lin',
            'matter_power_nl',
        )]
    
    def calculate(self, state, want_derived=True, **params_values_dict):
        block = cosmosis.datablock.DataBlock()

        h = self.provider.get_param('H0') / 100
        block['cosmological_parameters', 'h0'] = h

        block['cosmological_parameters', 'omega_m'] = self.provider.get_param('omegam')

        block['distances', 'nz'] = len(self.z_background)
        block['distances', 'z'] = self.z_background
        block['distances', 'a'] = 1/(self.z_background+1)
        block['distances', 'd_c'] = self.provider.get_comoving_radial_distance(self.z_background)
        block['distances', 'd_m'] = block['distances', 'd_c'] # flat
        if self.want_zstar:
            block['distances', 'zstar'] = params_values_dict['zstar']

        if self.want_chistar:
            CAMBdata = self.provider.get_CAMBdata()
            block['distances', 'CHISTAR'] = CAMBdata.conformal_time(0) - CAMBdata.tau_maxvis

        if self.same_k_grid:
            z = self.Pk_interpolator_z
            kmax_power = self.kmax
            lin_Pk = self.provider.get_Pk_interpolator(nonlinear=False, extrap_kmin=1e-5*h)
            nolin_Pk = self.provider.get_Pk_interpolator(nonlinear=True, extrap_kmin=1e-5*h)
            k = np.logspace(np.log10(1e-5), np.log10(kmax_power), self.nk)
            block.put_grid('matter_power_nl', "z", z, "k_h", k, "P_k", nolin_Pk.P(z, k*h, grid=True)*h**3)
            block.put_grid('matter_power_lin', "z", z, "k_h", k, "P_k", lin_Pk.P(z, k*h, grid=True)*h**3)
        else:
            k, z, Pk = self.provider.get_Pk_grid(nonlinear=True)
            block.put_grid('matter_power_nl', "z", z, "k_h", k/h, "P_k", Pk*h**3)
            k, z, Pk = self.provider.get_Pk_grid(nonlinear=False)
            block.put_grid('matter_power_lin', "z", z, "k_h", k/h, "P_k", Pk*h**3)
        
        for section in block.sections():
            state[self.renames_output.get(section, section).lower()] = {k[1]: block[*k] for k in block.keys(section=section)}
        

