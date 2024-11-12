from pathlib import Path
from typing import Mapping, Iterable, Optional
import os
from cobaya.likelihood import Likelihood
from cobaya.theory import Theory
from cobaya.model import as_requirement_list
import cosmosis.datablock
import cosmosis.runtime.module
import cosmosis.runtime.config
from cosmosis.runtime.pipeline import config_to_block, PIPELINE_INI_SECTION
try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    pass

class base(Theory):
    version = '1.0'
    root_directory: Optional[str] = None
    ini_path: Optional[str] = None
    renames_input = {}
    renames_output = {}
    check_renames = False

    def initialize(self):
        if self.root_directory is None:
            self.root_directory = os.getenv('COSMOSIS_ROOT_DIRECTORY')
            assert self.root_directory is not None, 'You need to set root_directory or env COSMOSIS_ROOT_DIRECTORY'
        if self.ini_path is None:
            self.ini_path = os.getenv('COSMOSIS_INI_PATH')
            assert self.ini_path is not None, 'You need to set ini_path or env COSMOSIS_INI_PATH'
        self.root_directory = str(Path(self.root_directory).absolute())
        self.ini_path = str(Path(self.ini_path).absolute())
        cwd = os.getcwd()
        os.chdir(self.root_directory)

        self.options = cosmosis.runtime.config.Inifile(self.ini_path)
        module_name = self.name if hasattr(self, "name") else self.__class__.__name__
        self.module = cosmosis.runtime.module.Module.from_options(
            module_name,
            self.options,
            self.root_directory,
        )
        
        # identify parameters needed for module setup
        relevant_sections = self.options.sections()

        #We let the user specify additional global sections that are
        #visible to all modules
        global_sections = self.options.get("runtime", "global", fallback=" ")
        for global_section in global_sections.split():
            relevant_sections.append(global_section)

        config_block = config_to_block(relevant_sections, self.options)
        config_block[PIPELINE_INI_SECTION, 'current_module'] = self.module.name
    
        self.module.setup(config_block)
        os.chdir(cwd)
    
    def cosmosis_datablock_inputs(self) -> list[str]:
        return []
    
    def cosmosis_datablock_outputs(self) -> list[str]:
        return []
    
    def get_requirements(self):
        if self.check_renames:
            given = set(map(str.lower, self.cosmosis_datablock_inputs()))
            should = set(self.renames_input.keys())
            assert given >= should, f"{self.__class__.__name__} inputs lacks {should - given}"
        return [self.renames_input.get(i.lower(), i).lower() for i in self.cosmosis_datablock_inputs()]
    
    def get_can_provide(self):
        if self.check_renames:
            given = set(map(str.lower, self.cosmosis_datablock_outputs()))
            should = set(self.renames_output.keys())
            assert given >= should, f"{self.__class__.__name__} outputs lacks {should - given}"
        return [self.renames_output.get(i.lower(), i).lower() for i in self.cosmosis_datablock_outputs()]
    
    def calculate(self, state, want_derived=True, **params_values_dict):
        data_package = cosmosis.datablock.DataBlock()

        # renames_input: {'what_cosmosis_modules_see': 'what_cobaya_see'}
        requirements = [(r, self.renames_input.get(r.lower(), r)) for r in self.cosmosis_datablock_inputs()]

        for cosmosis_k, cobaya_k in filter(lambda r: r[0].startswith('_metadata.'), requirements.copy()):
            _, section, name, key = cosmosis_k.split('.')
            data_package.put_metadata(section, name, key, self.provider.get_result(cobaya_k))
            requirements.remove((cosmosis_k, cobaya_k))

        for cosmosis_k, cobaya_k in requirements:
            if '.' in cosmosis_k: # section.name: value
                section, name = cosmosis_k.split('.')
                data_package[section, name] = self.provider.get_param(cobaya_k)
            else: # section: dict[name: value]
                self.log.debug("Section %s read to Datablock as %s", cobaya_k, cosmosis_k)
                try:
                    items = self.provider.get_result(cobaya_k).items()
                except KeyError:
                    items = self.provider.get_param(cobaya_k).items()
                for name, v in items:
                    data_package[cosmosis_k, name] = v
        
        self.log.debug("Sections written to DataBlock: %r", data_package.sections())
        
        self.module.execute(data_package)

        for section in self.cosmosis_datablock_outputs():
            if section.startswith('_metadata.'):
                _, sec, name, key = section.split('.')
                state[section] = data_package.get_metadata(sec, name, key)
            self.log.debug("Section %s written to cobaya as %s", section, self.renames_output.get(section, section).lower())
            state[self.renames_output.get(section.lower(), section).lower()] = {k[1]: data_package[*k] for k in data_package.keys(section=section)}
        
        if isinstance(self, base_Likelihood):
            state['logp'] = sum(data_package[*k] for k in data_package.keys(section='likelihoods'))
       
    
    def close(self):
        self.module.cleanup()

class base_Likelihood(base, Likelihood):
    pass
