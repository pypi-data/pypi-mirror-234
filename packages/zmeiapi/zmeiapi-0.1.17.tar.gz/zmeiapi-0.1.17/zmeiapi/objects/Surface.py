__version__ = "0.0.1"
__author__ = "Vlad Romanenko"


from abc import ABC, abstractmethod
from zmeiapi.zmei_io.Logger import logger


class AbstractSurface(ABC):
    @abstractmethod
    def __init__(self, name: str, params: list[float | int]):
        self.name = 's' + name
        self.params = params
        self.line = f''
        self._check_surf_parameters_type()
        self._check_surf_parameters()

    def __str__(self):
        return self.line

    def _check_surf_parameters_type(self):
        for param in self.params:
            if (type(param) is not float) and (type(param) is not int):
                logger.error(f'Parameter {param} must be type of float or int')
                raise AttributeError(f'Parameter {param} must be type of float or int')

    @abstractmethod
    def _check_surf_parameters(self):
        pass

    def _create_lines(self, surf_type: str):
        self.line += f'surf            '
        self.line += f'{self.name:15} {surf_type:15} '
        for param in self.params:
            self.line += f'{param:10} '
        self.line += f'\n'
        pass


class Surface:
    instances = []

    @classmethod
    def write_instances_to_file(cls, filename):
        """
        Class method to write all instances into the file
        :param filename: name of the file
        :type filename: str
        :return: None
        :rtype: None
        """
        with open(filename, 'w') as file:
            for instance in cls.instances:
                file.writelines(instance.lines)

    def __init__(self):
        self.__class__.instances.append(self)

    class Px(AbstractSurface):
        """
        Plane perpendicular to x-axis at x = x0
        :param params: x0, params length must be equal 1
        :type params: list[float]
        """
        def __init__(self, name: str, params: list[float | int]):
            super().__init__(name, params)
            super()._create_lines('cylz')

        def _check_surf_parameters(self):
            if len(self.params) != 1:
                logger.error('Wrong parameters number, loot at the class description')
                raise AttributeError('Wrong parameters number, loot at the class description')

    class Py(AbstractSurface):
        """
        Plane perpendicular to y-axis at y = y0
        :param params: y0, params length must be equal 1
        :type params: list[float]
        """
        def __init__(self, name: str, params: list[float | int]):
            super().__init__(name, params)
            super()._create_lines('cylz')

        def _check_surf_parameters(self):
            if len(self.params) != 1:
                logger.error('Wrong parameters number, loot at the class description')
                raise AttributeError('Wrong parameters number, loot at the class description')

    class Pz(AbstractSurface):
        """
        Plane perpendicular to z-axis at z = z0
        :param params: z0, params length must be equal 1
        :type params: list[float]
        """
        def __init__(self, name: str, params: list[float | int]):
            super().__init__(name, params)
            super()._create_lines('cylz')

        def _check_surf_parameters(self):
            if len(self.params) != 1:
                logger.error('Wrong parameters number, loot at the class description')
                raise AttributeError('Wrong parameters number, loot at the class description')

    class Cylz(AbstractSurface):
        def __init__(self, name: str, params: list[float | int]):
            super().__init__(name, params)
            super()._create_lines('cylz')

        def _check_surf_parameters(self):
            if len(self.params) != 3 and len(self.params) != 5:
                raise AttributeError('Wrong parameters number, loot at the class description')
            pass

    class Cyl(AbstractSurface):
        def __init__(self, name: str, params: list[float | int]):
            super().__init__(name, params)
            super()._create_lines('cylz')

        def _check_surf_parameters(self):
            if len(self.params) != 3 and len(self.params) != 5:
                logger.error('Wrong parameters number, loot at the class description')
                raise AttributeError('Wrong parameters number, loot at the class description')
            pass

    class Hexxc(AbstractSurface):
        def __init__(self, name:str, params: list[float | int]):
            super().__init__(name, params)
            super()._create_lines('hexxc')

        def _check_surf_parameters(self):
            if len(self.params) != 3:
                logger.error('Wrong parameters number, loot at the class description')
                raise AttributeError('Wrong parameters number, loot at the class description')

    class Hexxap(AbstractSurface):
        def __init__(self, name: str, params: list[float | int]):
            super().__init__(name, params)
            super()._create_lines('hexxap')

        def _check_surf_parameters(self):
            if len(self.params) != 5:
                logger.error('Wrong parameters number, loot at the class description')
                raise AttributeError('Wrong parameters number, loot at the class description')


if __name__ == '__main__':
    surf = Surface().Cylz('surfc', [2, 3.0, 1.0])
    surf1 = Surface().Cylz('surfc', [1, 3, 1.0])
    surf2 = Surface().Cyl('surfc', [1, 3, 1.0])

    surf3 = Surface.Hexxc('surfc', [1, 3, 1.0])

    print(surf)
    print(surf2)
    print(surf3)
    print(Surface.instances)
