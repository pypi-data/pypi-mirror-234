__version__ = '0.3.0'
__author__ = 'Vlad Romanenko'


from zmeiapi.zmei_io.Logger import logger
import pickle as pkl
from zmeiapi.data.Parameters import NUCLIDES_DICT_PATH


class Material:
    """
    Material class provides a material object which contains all the necessary for Serpent information
    as long as the method to write material to file

    :param name: material name

    :type name: str

    :param nuclides: list of nuclides the material consists of, defaults to None

    :type nuclides: one-dimensional list of strings

    :param concentrations: list of nuclides' concentrations, defaults to None

    :type concentrations: one-dimensional list of floats, len(concentrations)==len(nuclides)

    :param density: material density, defaults to 'sum'

    :type density: str or float

    :param temp: material temperature, defaults to 600

    :type temp: int or float

    :param color: color of the material in Serpent, defaults to None

    :type color: one-dimensional list of integers from 0 to 255

    :param burn: burnable material indicator, defaults to 0

    :type burn: integer, possible values 0 or 1

    :param is_coolant: indicates if material represents water-based coolant, if yes lwtr card will be added to material

    :type is_coolant: bool

    :param is_fuel: indicates if material represents fuel

    :type is_fuel: bool

    :param nuclides_format: the format of the parameter nuclides, possible values: "Mendeleev_table" or "Serpent".
        Defaults to "Mendeleev_table".

    :type nuclides_format: str

    :var nuclides_dict: dictionary with the Serpent representation of nuclides names

    :type nuclides_dict: dictionary, keys are str names of the nuclides ('H-1', 'Gd-152', ..)
        values are str names of nuclides in Serpent ('1001', '8016', ..)

    :var nuclides_concentrations: dictionary with the nuclide-concentration values

    :type nuclides_concentrations: dictionary, keys are str names of nuclides in Serpent ('1001', '8016', ..)
        values are lists with len==2, value[0] is a float (nuclide concentration),
        value[1] is a str (name of the nuclide)

    :var lines: Serpent representation of material

    :type lines: list[str]
    """

    instances = []

    @classmethod
    def write_instances_to_file(cls, filename):
        """
        Class method to write all instances into the file

        :param filename: name of the file

        :type filename: str

        :return: None
        """
        with open(filename, 'w') as file:
            for instance in cls.instances:
                file.writelines(instance.lines)

    def __init__(
            self,
            name,
            nuclides=None,
            concentrations=None,
            density='sum',
            temp=600,
            color=None,
            burn=0,
            is_coolant=False,
            is_fuel=False,
            nuclides_format="Mendeleev_table"
    ):
        """
        Constructor method
        """

        # importing pickle module to load all Serpent nuclides' names
        # import pickle as pkl
        self.__class__.instances.append(self)
        self.name = name
        self.nuclides = nuclides
        self.concentrations = concentrations
        self.density = density
        self.temp = temp
        self.color = color
        self.burn = burn
        self.is_coolant = is_coolant
        self.is_fuel = is_fuel
        self.nuclides_format = nuclides_format
        self.nuclides_concentrations = {}
        self.lines = []
        self.temp_flag = '03c'
        self._temperature_checker()
        self._set_temperature_flag()

        # loading nuclides dictionary from the pickle file
        with open(NUCLIDES_DICT_PATH, 'rb') as file:
            self.nuclides_dict = pkl.load(file)

        self._nuclides_and_concentrations_checker()
        self._create_nuclides_concentrations_dict()

        self._create_lines()

    def __str__(self):
        print(self.lines[1])

    def _nuclides_and_concentrations_checker(self):
        if (type(self.nuclides) and type(self.concentrations)) is list:
            pass
        else:
            logger.error(f"Nuclides and concentrations must have a list type, execution will be stoped")
            raise AttributeError(f"Nuclides and concentrations must have a list type, execution will be stoped")

        if len(self.nuclides) == len(self.concentrations):
            pass
        else:
            logger.error(f"Something went wrong, "
                         f"the length of nuclides and concentrations lists must be equal, "
                         f"execution will be stoped")
            raise AttributeError(f"Something went wrong, "
                                 f"the length of nuclides and concentrations lists must be equal, "
                                 f"execution will be stoped")

    def _create_nuclides_concentrations_dict(self):
        # creating nuclides_concentrations dictionary for material
        for i, nuclide in enumerate(self.nuclides):
            if self.nuclides_format == 'Mendeleev_table':
                self.nuclides_concentrations[self.nuclides_dict[nuclide]] = [self.concentrations[i], nuclide]
            elif self.nuclides_format == 'Serpent':
                self.nuclides_concentrations[nuclide] = [self.concentrations[i], nuclide]
            else:
                logger.error(f"Wrong nuclides format, execution will be stoped")
                raise AttributeError(f"Wrong nuclides format, execution will be stoped")
            # print(self.nuclides_concentrations[self.nuclides_dict[nuclide]])
        pass

    def _temperature_checker(self):
        if self.temp < 300:
            self.temp = 300.0
            print(f'Warning temperature of the material {self.name} is below 300K, '
                  f'temperature has been changed to 300K')

    def _set_temperature_flag(self):
        if self.temp > 300:
            self.temp_flag = f'{(self.temp // 300) * 3:.0f}'
        else:
            self.temp_flag = '3'
        self.temp_flag = f'{int(self.temp_flag):02}c'

    def _create_lines(self) -> None:
        self.lines.append(f'% Material {self.name}\n')
        __second_line = f'mat {self.name} {self.density} '
        if self.is_coolant:
            __second_line = __second_line + f'moder lwtr{self.temp:.1f} 1001 '
        elif self.is_fuel and self.burn == 0:
            __second_line = __second_line + f'tmp {str(self.temp)} '
        elif self.is_fuel and self.burn == 1:
            __second_line = __second_line + f'tmp {str(self.temp)} '
        elif (not self.is_coolant) and (not self.is_fuel):
            __second_line = __second_line + f'tmp {str(self.temp)} '

        if self.color is not None:
            __second_line = __second_line + f'rgb {self.color[0]} {self.color[1]} {self.color[2]} '
        if self.burn == 1:
            __second_line = __second_line + f'burn 1 '
        __second_line = __second_line + f'\n'
        self.lines.append(__second_line)

        for key in self.nuclides_concentrations.keys():
            if self.nuclides_format == 'Mendeleev_table':
                _comment = f'%{self.nuclides_concentrations[key][1]}\n'
            elif self.nuclides_format == 'Serpent':
                _comment = f'%{self.nuclides_concentrations[key][0]}\n'
            else:
                _comment = f'%'
            self.lines.append(
                f'{key}.{self.temp_flag} '
                f'{self.nuclides_concentrations[key][0]:.5E} {_comment}'
            )
        self.lines.append('\n')

    def write_to_file(self, file) -> None:
        """
        Method writes the material in the form of Serpent material input description

        :param file: the file object to write material into

        :type file: file object
        """
        file.writelines(self.lines)




