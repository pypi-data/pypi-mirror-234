import yaml
from pkg_resources import resource_filename
import pickle


NUCLIDES_DICT_PATH = resource_filename('zmeiapi.data', 'nuclides_dict.pkl')
NUCLIDES_MASSES_DICT_PATH = resource_filename('zmeiapi.data', 'nuclides_masses.pkl')
MATERIAL_DATA_PATH = resource_filename('zmeiapi.data', 'materials_data.yml')

with open(NUCLIDES_DICT_PATH, 'rb') as file:
    nuclides_dict = pickle.load(file)

with open(NUCLIDES_MASSES_DICT_PATH, 'rb') as file:
    nuclides_masses_dict = pickle.load(file)

with open(MATERIAL_DATA_PATH, 'r') as file:
    materials_data = yaml.safe_load(file)

N_AVO = 0.60221


if __name__ == '__main__':
    pass

