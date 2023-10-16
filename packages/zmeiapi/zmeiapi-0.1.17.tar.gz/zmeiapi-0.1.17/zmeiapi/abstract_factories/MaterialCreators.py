__version__ = "0.1.0"
__author__ = 'Vlad Romanenko'


from abc import ABC, abstractmethod
from zmeiapi.zmei_io.Logger import logger


class MaterialCreator(ABC):
    @abstractmethod
    def __init__(self, number, layer_number):
        self.number = number
        self.layer_number = layer_number

    @abstractmethod
    def create_material(
            self,
            name: str,
            nuclides: list,
            concentrations: list,
            **kwargs
    ):
        pass


class NumberedMaterialsCreator(ABC):
    @abstractmethod
    def __init__(self, number):
        self.number = number

    @abstractmethod
    def create_materials(
            self,
            name: str,
            nuclides: list,
            concentrations: list,
            **kwargs
    ):
        pass


class CoreMaterialsCreator(ABC):
    @abstractmethod
    def __init__(self, fas_amount, layers_amount):
        self.fas_amount = fas_amount
        self.layers_amount = layers_amount

    @abstractmethod
    def create_materials(
            self,
            name: str,
            nuclides: list,
            concentrations: list,
            **kwargs
    ):
        pass
