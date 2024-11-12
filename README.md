# CosmoSIS2cobaya

Utilize CosmoSIS modules in cobaya.

It was used in
* [A model-independent reconstruction of the matter power spectrum](https://arxiv.org/abs/2411.07082)

## Basic Usage

### Installation

- Make sure you have installed python>=3.9, [CosmoSIS](https://github.com/joezuntz/cosmosis) and [cosmosis-standard-library](https://github.com/joezuntz/cosmosis-standard-library) properly [^1].

- Install cosmosis2cobaya with `pip install cosmosis2cobaya`.

### Run the preconfigured weak lensing and galaxy clustering likelihoods

In `example/`, there are some preconfigured weak lensing and galaxy clustering yaml file you can start with.

- Set environment variable `COSMOSIS_ROOT_DIRECTORY` to the path of cosmosis-standard-library and set `COSMOSIS_INI_PATH` to the CosmoSIS ini file related to your run (We need it to load the configuration of the CosmoSIS module).
Alternatively, if you have `python-dotenv` installed, you can set them in your `.env` file.

- `cobaya-run XXXXX.yaml`

If it works well, you can modify these yaml files to what you want.

> [!NOTE]
> We do not treat each dataset as a single likelihood in order to take full advantage of blocking for speedup.

## Advanced usage

cosmosis2cobaya allows you to use almost any module (called component, theory, likelihood in cobaya) from CosmoSIS in cobaya.
But first, let's clarify some of the differences between CosmoSIS and cobaya.

- There are two ways to automatically organize modules: either give the execution order of the modules and then let the data automatically flow in and out, or first give the data that flows in and out of each module and then automatically determine the execution order based on the dependencies. CosmoSIS is the former and cobaya is the latter. So in order to port the CosmoSIS module to cobaya, we must first determine what data goes in and out.

- Because the execution order is given in CosmoSIS, data with the same name can be read and written repeatedly. But in cobaya, data names are used to determine dependencies, so they can only be written (created) by one module.

- CosmoSIS is case insensitive to data names but cobaya is case sensitive. Although we try to make it case-insensitive at the transit layer, it is recommended to always use lowercase data names.

- Unused parameters are not allowed in cobaya. And they may also cause unexpected errors.

- Since cobaya already has Boltzmann components, we use them directly and convert to the CosmoSIS data format using the `cosmosis2cobaya.boltzmann` theory component. This component also accepts some CosmoSIS options.

With these in mind, we can adapt as follows.

### Conversion of parameters and priors

There is a helper script `ini2yaml.py` help you to convert parameters and priors:
``` bash
python3 ini2yaml.py <CosmoSIS input file>.ini
```

Remember to remove unused parameters before pasting into the `params:` section of the yaml.

### Write cobaya components

For each module, create a file at the same path in cosmosis2cobaya as the `file` value of the corresponding section in the CosmoSIS ini file ( certainly with a `.py` extension).

Its content is like
``` python
from cosmosis2cobaya._base import base

class tatt_interface(base):

    def cosmosis_datablock_inputs(self):
        return ['cosmological_parameters', 'matter_power_lin', 'matter_power_nl', 'fastpt', 'intrinsic_alignment_parameters']
    
    def cosmosis_datablock_outputs(self):
        return [
            'intrinsic_power',
            'intrinsic_power_ee',
            'intrinsic_power_bb',
            'matter_intrinsic_power',
            'intrinsic_alignment_parameters'
        ]

class IA(tatt_interface):
    pass
```
For theory (those will not give likelihood values), inherit a class (`tatt_interface` in the template above) from `cosmosis2cobaya._base.base`.
For likelihoods (those will give likelihood values), inherit from `cosmosis2cobaya._base.base_Likelihood`.
It is recommended to use the same class name as the file name.

Implement `cosmosis_datablock_inputs` and `cosmosis_datablock_outputs`, which return the names of the data read/written by CosmoSIS, respectively.
The results returned by the CosmoSIS module `setup()` can be read from `self.module.data`.

Assuming the file path is `cosmosis2cobaya/intrinsic_alignments/tatt/tatt_interface.py`, now you can use it in cobaya:
``` yaml
theory:
    cosmosis2cobaya.intrinsic_alignments.tatt.tatt_interface:
```

To load the configuration from the CosmoSIS ini file, we use the class name (`tatt_interface` in the above) as the section name to search for in the ini.
However, sometimes the class name is different from the section name or we have to use the module multiple times.
We can inherit from that class, using another class name (`IA` in the example above) and use it in cobaya:
``` yaml
theory:
    cosmosis2cobaya.intrinsic_alignments.tatt.tatt_interface.IA:
```

However, sometimes the section name in ini cannot be used as the class name, then the section name can be specified by the attribute `name`, e.g.:
``` python
class TwoPt_point_mass(TwoPointLikelihood):
    name = '2pt_like'
```

To avoid writing data with the same name multiple times, rename the data in yaml:
``` yaml
theory:
  cosmosis2cobaya.boltzmann:
    renames_output:
      matter_power_lin: matter_power_lin__0
      matter_power_nl: matter_power_nl__0
  cosmosis2cobaya.extrapolate:
    renames_input:
      matter_power_lin: matter_power_lin__0
      matter_power_nl: matter_power_nl__0
      # what_cosmosis_modules_see: what_cobaya_see
```

There is a helper script `dot2yaml.py` help you to generate them for the dot file (see [here](https://cosmosis.readthedocs.io/en/latest/features/pipeline_features.html#making-pipeline-graphs) how to generate it):
``` bash
python3 dot2yaml.py <dot file> <ini file>
```

But it can go wrong when there are loops in the pipeline graph (e.g. des-y3_and_kids-1000) or the module name is duplicated with the data name (e.g. kids-1000).


[^1]: https://github.com/JiangJQ2000/cosmosis2cobaya/blob/master/.github/workflows/test.yml provides an example of manual installation on a Debian-based system.
