from zmeiapi.zmei_io.Logger import logger


class Cell:
    instances = []

    @classmethod
    def write_instances_to_file(cls, filename) -> None:
        """
        Class method to write all instances into the file
        :param filename: name of the file
        :type filename: str
        :return: None
        """
        with open(filename, 'w') as file:
            for instance in cls.instances:
                file.writelines(instance.lines)

    def __init__(self, name, universe, material, surfaces, fill=False, delimiter='  ', **kwargs):
        self.__class__.instances.append(self)
        self.name = f'c{name}'
        self.universe = universe
        self.fill = fill
        if self.fill:
            self.material = f'fill {material}'
        else:
            self.material = material
        self.surfaces = surfaces
        self.delimiter = delimiter
        self.line = f'cell {self.name}{self.delimiter}{self.universe}{self.delimiter}{self.material}'

        for surface in self.surfaces:
            self.line += f'{self.delimiter}{surface}'
        pass

    def __str__(self):
        return self.line

    def __add__(self, other):
        if type(other) == str:
            _cell = Cell(self.name[1:], self.universe, self.material, self.surfaces, delimiter=self.delimiter)
            _cell.line += f'{self.delimiter}{other}'
            return _cell
        elif type(other) == Cell:
            _cell = Cell(self.name[1:], self.universe, self.material, self.surfaces, delimiter=self.delimiter)
            _cell.line += f'{self.delimiter}{other.name}'
            return _cell
        else:
            logger.error.TypeError('Unsupported operand type. Operand must have type str or Cell')
            raise TypeError('Unsupported operand type. Operand must have type str or Cell')

    def __sub__(self, other):
        if type(other) == str:
            _cell = Cell(self.name[1:], self.universe, self.material, self.surfaces, delimiter=self.delimiter)
            _cell.line += f'{self.delimiter}-{other}'
            return _cell
        elif type(other) == Cell:
            _cell = Cell(self.name[1:], self.universe, self.material, self.surfaces, delimiter=self.delimiter)
            _cell.line += f'{self.delimiter}#{other.name}'
            return _cell
        elif type(other) == list:
            """!! rebuild this to return Cell type"""
            for i, cell in enumerate(other):
                if type(cell) == Cell:
                    _cell_name = cell.name
                elif type(cell) == str:
                    _cell_name = cell
                else:
                    raise RuntimeError('should be list of str or Cell')

                if i == 0:
                    self.line += f'{self.delimiter} -({_cell_name}'
                elif i == len(other) - 1:
                    self.line += f'{self.delimiter} {_cell_name})'
                else:
                    self.line += f'{self.delimiter} {_cell_name}'
            return self.line


if __name__ == '__main__':
    c = Cell('name', 'uni', 'mat', ['1', '2'])
    c1 = Cell('name1', 'uni', 'mat', ['1', '2'], fill=True)
    c2 = Cell('name2', 'uni', 'mat', ['1', '2'])

    c3 = c1 + c2
    for inst in Cell.instances:
        print(inst)


