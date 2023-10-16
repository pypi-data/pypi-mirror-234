from pkg_resources import resource_filename
import pickle
import yaml


NUCLIDES_DICT_PATH = resource_filename('zmeiapi.data', 'nuclides_dict.pkl')
NUCLIDES_MASSES_DICT_PATH = resource_filename('zmeiapi.data', 'nuclides_masses.pkl')
RESULTS_KEYS_DICT_PATH = resource_filename('zmeiapi.data', 'res_keys.yml')

with open(NUCLIDES_DICT_PATH, 'rb') as file:
    nuclides_dict = pickle.load(file)

with open(NUCLIDES_MASSES_DICT_PATH, 'rb') as file:
    nuclides_masses_dict = pickle.load(file)

with open(RESULTS_KEYS_DICT_PATH, 'r') as file:
    res_keys = yaml.safe_load(file)

N_AVO = 0.60221

