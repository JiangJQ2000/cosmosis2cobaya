import sys, os
from pathlib import PurePath
import pygraphviz as pgv
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

G = pgv.AGraph(sys.argv[1])
root_directory = os.getenv('COSMOSIS_ROOT_DIRECTORY')
if root_directory is None:
    print('Please set COSMOSIS_ROOT_DIRECTORY !', file=sys.stderr)
cwd = os.getcwd()
os.chdir(root_directory)
config = cosmosis.runtime.config.Inifile(sys.argv[2])
os.chdir(cwd)

skip_modules = ('Sampler', 'consistency', 'bbn_consistency', 'camb')
module = G.get_node("Sampler")
pre_module = None

def get_inputs_outputs_nextnode(node: pgv.agraph.Node, pre_module):
    next_node = None
    inputs = []
    outputs = []
    for n in G.iterneighbors(node):
        if n == pre_module: continue
        if n.attr['group'] == 'pipeline':
            next_node = n
        else:
            try:
                G.get_edge(node, n)
                outputs.append(n)
            except KeyError:
                pass
            try:
                G.get_edge(n, node)
                inputs.append(n)
            except KeyError:
                pass
    return next_node, inputs, outputs

section2module = {}
yaml_dict = {}

next_node, _, _ = get_inputs_outputs_nextnode(module, None)

while next_node is not None:
    next_node, inputs, outputs = get_inputs_outputs_nextnode(module, pre_module)
    if module not in skip_modules:
        yaml_dict[f"cosmosis2cobaya.{PurePath(config[module, 'file']).with_suffix('').as_posix().replace('/', '.')}.{module}"] = {
            "renames_input": {
                str(i): f"{i}__after__{section2module[i]}".lower() if i in section2module else str(i) for i in inputs if len(set(G.iterneighbors(i))) != 1 # case that only connect to self
            },
            "renames_output": {
                str(o): f"{o}__after__{module}".lower() if o != 'likelihoods' else 'likelihoods' for o in outputs
            }
        }
        section2module |= {o: module for o in outputs}
    pre_module = module
    module = next_node

dump(yaml_dict, Dumper=Dumper, sort_keys=False, stream=sys.stdout)

