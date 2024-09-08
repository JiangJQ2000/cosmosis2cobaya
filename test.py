import os, subprocess, sys
from pathlib import Path
import numpy as np
try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    pass

from cobaya import get_model
import cosmosis.runtime.config

cwd = os.getcwd()

os.chdir(os.getenv('COSMOSIS_ROOT_DIRECTORY'))

subprocess.run(
    ['cosmosis', os.getenv('COSMOSIS_INI_PATH')]
)
options = cosmosis.runtime.config.Inifile(os.getenv('COSMOSIS_INI_PATH'))
save_dir = options.get("test", "save_dir")
loglikes_cosmosis = {}
with open(Path(save_dir) / 'likelihoods' / 'values.txt', 'r') as f:
    for l in f.readlines():
        name, _, value = l.rpartition(' = ')
        loglikes_cosmosis[name] = float(value)
total_loglike_cosmosis = sum(loglikes_cosmosis.values())

os.chdir(cwd)

model = get_model(sys.argv[1])
point = model.prior.reference()
total_loglike_cobaya = model.loglike(point, return_derived=False)

print('cosmoSIS:', total_loglike_cosmosis)
print('cosmosis2cobaya:', total_loglike_cobaya)

assert np.allclose(total_loglike_cosmosis, total_loglike_cobaya, atol=0.2)
# Sources of difference (sorted by impact)
# 1. Alignment of k-grids (controlled by same_k_grid of cosmosis2cobaya.boltzmann)
# 2. cosmomc_theta option of the consistency module of cosmoSIS
# 3. BBN model (cosmoSIS use the old PArthENoPE results: https://github.com/joezuntz/cosmosis-standard-library/blob/main/utility/bbn_consistency/helium.dat)
