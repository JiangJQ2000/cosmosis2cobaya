import os, sys
from pathlib import Path
from yaml import load, dump
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper

import cosmosis.runtime.config

try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    pass

root_directory = os.getenv('COSMOSIS_ROOT_DIRECTORY')
if root_directory is None:
    print('Please set COSMOSIS_ROOT_DIRECTORY !', file=sys.stderr)
cwd = os.getcwd()
os.chdir(root_directory)

config = cosmosis.runtime.config.Inifile(sys.argv[1])
value_path = Path(root_directory) / config[('pipeline', 'values')]
prior_path = Path(root_directory) / config[('pipeline', 'priors')]

config_value = cosmosis.runtime.config.Inifile(value_path)
config_prior = cosmosis.runtime.config.Inifile(prior_path)

params = {}
priors = {}

for key in config_prior.sections():
    for k, v in config_prior.items(key):
        dist, a, b = v.split()
        if dist != 'gaussian':
            raise NotImplementedError(dist)
        priors[f"{key}__{k}"] = {
            "prior": {
                "dist": "norm",
                "loc": float(a),
                "scale": float(b),
            }
        }

for key in config_value.sections():
    if key in ('cosmological_parameters', 'halo_model_parameters'):
        continue
    for k, v in config_value.items(key):
        v = v.split()
        if len(v) == 1:
            params[f"{key}__{k}"] = float(v[0])
        elif len(v) == 3:
            params[f"{key}__{k}"] = {
                "prior": {
                    "min": float(v[0]),
                    "max": float(v[-1]),
                },
                "ref": float(v[1]),
                "drop": True,
            }
            if f"{key}__{k}" in priors:
                params[f"{key}__{k}"] |= priors[f"{key}__{k}"]
        else:
            raise NotImplementedError(v)
    params[key] = {
        'value': "lambda " + ','.join(f"{key}__{k}" for k,_ in config_value.items(key)) + ": {" + ','.join(f"'{k}':{key}__{k}" for k,_ in config_value.items(key)) + "}",
        'derived': False,
    }
print(dump({'params': params}, Dumper=Dumper))

os.chdir(cwd)
