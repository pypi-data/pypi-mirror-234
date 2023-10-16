__version__ = "0.1.2"
__author__ = "Vlad Romanenko"


from zmeiapi.zmei_io.Logger import logger


class Pin:
    """
    Pin class provides a pin object which contains all the necessary for Serpent information
    as long as the method to write pin to file.

    :param name: name of the pin (the "p" letter and in some cases additional postfixes
        will be added to the name after creation)

    :type name: str

    :var materials: materials list

    :type materials: list[str]

    :var radiuses: list of radiuses for materialls in a pin

    :type radiuses: list[str]

    :var lines: pin lines to write into Serpent file

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

    def __init__(self, name: str, materials: list, radiuses: list):
        self.__class__.instances.append(self)
        self.name = name
        self.materials = materials
        self.radiuses = radiuses
        self._check_lenghths()
        self.lines = []
        self._create_write_lines()

    def __str__(self):
        return f'pin p{self.name}'

    def _create_write_lines(self) -> None:
        """
        Method that creates lines for the pin in a Serpent format. Called during the initialisation.
        :return: None
        :rtype: None
        """
        self.lines.append(f'pin p{self.name}\n')
        for i, mat in enumerate(self.materials):
            if i < len(self.radiuses):
                self.lines.append(f'{mat}  {self.radiuses[i]}\n')
            else:
                self.lines.append(f'{mat}\n')
        self.lines.append('\n')

    def numerate_materials(self, number: int) -> list[str]:
        """
        Additional method to add a number to materials in the pins. The number will be added in 03i format.

        **Example:**

        water -> water_01

        :param number: number that will be added to material
        :type number: int
        :return: new materials list
        :rtype: list[str]
        """
        materials = []
        for i, mat in enumerate(self.materials):
            mat = f'{mat}_{number:03}'
            materials.append(mat)
        return materials

    def write_to_file(self, file) -> None:
        """
        Method to write pin lines to file in a Serpent format
        :param file: file object
        :type file: file object
        :return: None
        :rtype: None
        """
        file.writelines(self.lines)

    def _check_lenghths(self) -> None:
        """
        Method checks the lengths of materials and radiuses lists.

        If ``len(materials) - len(radiuses) != 1`` raises AttributeError.
        :return: None
        :rtype: None
        """
        if len(self.materials) - len(self.radiuses) != 1:
            logger.error("The lenghs of materials and radiuses lists are wrong")
            raise AttributeError("The lenghs of materials and radiuses lists are wrong")


if __name__ == '__main__':
    pin1 = Pin('1', ['water'], [])
    pin2 = Pin('2', ['water'], [])
    Pin.write_instances_to_file('test')
