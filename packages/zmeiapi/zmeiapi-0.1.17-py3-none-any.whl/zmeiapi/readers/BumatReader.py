__version__ = '0.0.1'
__author__ = 'Vlad Romanenko'


import os
import glob
from zmeiapi.zmei_io.Logger import logger


class BumatMaterialObject:
    def __init__(
            self,
            material_name: str,
            burnup: float,
            burnup_days: float,
            concentrations_sum: float,
            vol: float,
            nuclides: list,
            concentrations: list
    ):
        """
        :param material_name: name of material
        :param burnup: burnup value (MWt*d/kg)
        :param burnup_days: burnup value (days)
        :param concentrations_sum: sum of all nuclides' concentration
        :param vol: material volume
        :param nuclides: list of nuclides
        :type nuclides:
        :param concentrations: list of concentrations according to the nuclides list
        :type concentrations:
        """
        self.burnup = burnup
        self.burnup_days = burnup_days
        self.material_name = material_name
        self.concentrations_sum = concentrations_sum
        self.vol = vol

        self.nuclides = nuclides
        self.concentrations = concentrations

        self.nuclides_and_concentrations = {}
        for nuclide, concentration in zip(self.nuclides, self.concentrations):
            self.nuclides_and_concentrations[nuclide] = concentration

    def __str__(self):
        return f'BumatObject {self.material_name}, burnup = {self.burnup} MWd/kgU'


class BumatReader:
    def __init__(self, folder_path):
        self.bumat_filenames = glob.glob(os.path.join(folder_path, '*.bumat*'))
        if not self.bumat_filenames:
            logger.error(f"Bumat files not found")
            raise RuntimeError(f"Bumat files not found")
        self.bumat_filenames = sorted(self.bumat_filenames, key=self.__bumat_key_val)

        with open(self.bumat_filenames[0], 'r') as file:
            _lines = file.readlines()
        self.mat_indexes = self._get_mat_indexes(_lines)

        self.bumat_mat_dict = {}
        for bumat_file in self.bumat_filenames:
            bumat_file_index = self.__bumat_key_val(bumat_file)
            self.bumat_mat_dict[bumat_file_index] = self._read_bumat_file(bumat_file)

    @staticmethod
    def __bumat_key_val(string: str) -> int:
        val = int(string.split('bumat')[-1])
        return val

    @staticmethod
    def _get_burnup(bumat_lines):
        burnup = None
        burnup_days = None
        for line in bumat_lines:
            if line.startswith("% Material compositions"):
                # splitting the line by '(' symbol
                # % Material compositions (0.00 MWd/kgU / 0.14 days)
                _splited_line_with_burnup = line.split('(')[1]
                _splited_burnups = _splited_line_with_burnup.split()
                burnup = float(_splited_burnups[0])
                burnup_days = float(_splited_burnups[-2])
                break

        if (burnup is None) or (burnup_days is None):
            logger.error(f"Burnup or burnup_days value not found")
            raise RuntimeError(f"Burnup or burnup_days value not found")
        return burnup, burnup_days

    @staticmethod
    def _get_mat_indexes(bumat_lines: list[str]) -> list[int]:
        # get indexes (lines numbers) for all start lines for each material
        indexes = [i for i, line in enumerate(bumat_lines) if line.startswith("mat  ")]
        indexes.append(len(bumat_lines))
        return indexes

    def _read_bumat_file(self, filename: str) -> list[BumatMaterialObject]:
        with open(filename, 'r') as file:
            bumat_lines = file.readlines()

        burnup, burnup_days = self._get_burnup(bumat_lines)
        # print(burnup, burnup_days)

        mat_indexes = self._get_mat_indexes(bumat_lines)
        # print(mat_indexes[-1])
        # print(bumat_lines[mat_indexes[-1]])

        bumat_material_objects_list = []

        for ind_num, ind in enumerate(mat_indexes):
            if ind == mat_indexes[-1]:
                break
            nuclides = []
            concentrations = []

            _f_name_line = bumat_lines[ind]
            # print(_f_name_line, ind)
            material_name = _f_name_line.split()[1].split('pp')[0]
            concentrations_sum = float(_f_name_line.split()[2])
            vol = float(_f_name_line.split()[4])

            for nuclide_counter in range(ind + 1, mat_indexes[ind_num + 1]):
                _l = bumat_lines[nuclide_counter].split()
                nuclides.append(_l[0].split('.'[0])[0])
                concentrations.append(float(_l[1]))
            bumat_material_object = BumatMaterialObject(
                material_name, burnup, burnup_days, concentrations_sum, vol, nuclides, concentrations
            )
            bumat_material_objects_list.append(bumat_material_object)
        return bumat_material_objects_list

    def get_material_nuclides_concentrations_over_time(self, material_name):
        print(self.bumat_mat_dict.keys())
        burnup = []
        nuclides_and_concentrations_over_time = {}
        for i, key in enumerate(self.bumat_mat_dict.keys()):
            for bumat_obj in self.bumat_mat_dict[key]:
                if bumat_obj.material_name == material_name:
                    burnup.append(bumat_obj.burnup)
                    for nuclide in bumat_obj.nuclides_and_concentrations.keys():
                        if i == 0:
                            nuclides_and_concentrations_over_time[nuclide] = \
                                [bumat_obj.nuclides_and_concentrations[nuclide]]
                        else:
                            nuclides_and_concentrations_over_time[nuclide] += \
                                [bumat_obj.nuclides_and_concentrations[nuclide]]

                    continue
        return burnup, nuclides_and_concentrations_over_time


if __name__ == '__main__':
    path = '/home/vlad/Serpent/Calculation/22AU_312/22AU_b'
    b = BumatReader(path)
    print(b.bumat_mat_dict[150][-1])
    b, nuces = b.get_material_nuclides_concentrations_over_time('fu_Fuel_001')
    print(nuces['92235'])
    from zmeiapi.utilities.Graphs import SimpleGraph, AnimatedBarPlot
    SimpleGraph(b, nuces['54135'])

    nuclides_list = list(nuces.keys())
    concentrations = []
    for j in range(len(nuces['54135'])):
        concentrations.append([])
        for i, key in enumerate(nuces.keys()):
            concentrations[j].append(nuces[key][j])
        pass
    print(nuclides_list)
    print(len(concentrations))
    AnimatedBarPlot(nuclides_list, concentrations, yscale='log')
