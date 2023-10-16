from zmeiapi.zmei_io.Logger import logger


class Lattice:
    def __init__(
            self,
            name,
            cells_numbers: list[list[int]],
            cells_types: [list[int]],
            pins_types: dict,
            lattice_type=3,
            x0=0.0,
            y0=0.0,
            lattice_pitch=1.275
    ):
        self.lines = []
        first_line = f'lat {name} {lattice_type} {x0} {y0} {len(cells_numbers)} {len(cells_numbers[0])} {lattice_pitch} \n'
        self.lines.append(first_line)
        self._check_lists(cells_numbers, cells_types)
        self._check_pin_types_existence(cells_types, pins_types)
        self._fill_lattice(cells_numbers, cells_types, pins_types)

        pass

    def write_to_file(self, filename: str):
        with open(filename, 'w') as file:
            file.writelines(self.lines)

    def _fill_lattice(self, cells_numbers: list[list[int]], cells_types: [list[int]], pins_types: dict):
        for row in zip(cells_numbers, cells_types):
            _line = ''
            for cell_number, cell_type in zip(row[0], row[1]):
                if pins_types[cell_type] == 'BC':
                    _l = f'p{pins_types[cell_type]} '
                else:
                    _l = f'p{pins_types[cell_type]}_{cell_number:03} '
                _line += f'{_l:18}'
                # print(cell_number, cell_type)
            _line += ' \n'
            self.lines.append(_line)
        pass

    @staticmethod
    def _check_lists(cells_numbers: list[list[int]], cells_types: [list[int]]):
        if len(cells_numbers) != len(cells_types):
            logger.error('cells_numbers and cells_types lists must have equal lengths')
            raise RuntimeError('cells_numbers and cells_types lists must have equal lengths')
        for cells_rows in zip(cells_numbers, cells_types):
            if len(cells_rows[0]) != len(cells_numbers) and len(cells_rows[1]) != len(cells_types):
                logger.error('cells_numbers and cells_types lists must have equal row\'s and column\'s lengths')
                raise RuntimeError('cells_numbers and cells_types lists must have equal row\'s and column\'s lengths')

    @staticmethod
    def _check_pin_types_existence(cells_types: [list[int]], pins_types: dict):
        cells_types = list(set(i for j in cells_types for i in j))
        for name in cells_types:
            if name in pins_types:
                pass
            else:
                logger.error('cells_numbers and cells_types lists must have equal row\'s and column\'s lengths')
                raise RuntimeError('cells_numbers and cells_types lists must have equal row\'s and column\'s lengths')


if __name__ == '__main__':
    TVSA_cells_numbers = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 56, 77, 98, 119, 140, 161, 182, 203, 224, 245, 266, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 46, 67, 88, 109, 130, 151, 172, 193, 214, 235, 256, 277, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 37, 57, 78, 99, 120, 141, 162, 183, 204, 225, 246, 267, 287, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 29, 47, 68, 89, 110, 131, 152, 173, 194, 215, 236, 257, 278, 296, 0],
        [0, 0, 0, 0, 0, 0, 0, 22, 38, 58, 79, 100, 121, 142, 163, 184, 205, 226, 247, 268, 288, 304, 0],
        [0, 0, 0, 0, 0, 0, 16, 30, 48, 69, 90, 111, 132, 153, 174, 195, 216, 237, 258, 279, 297, 311, 0],
        [0, 0, 0, 0, 0, 11, 23, 39, 59, 80, 101, 122, 143, 164, 185, 206, 227, 248, 269, 289, 305, 317, 0],
        [0, 0, 0, 0, 7, 17, 31, 49, 70, 91, 112, 133, 154, 175, 196, 217, 238, 259, 280, 298, 312, 322, 0],
        [0, 0, 0, 4, 12, 24, 40, 60, 81, 102, 123, 144, 165, 186, 207, 228, 249, 270, 290, 306, 318, 326, 0],
        [0, 0, 2, 8, 18, 32, 50, 71, 92, 113, 134, 155, 176, 197, 218, 239, 260, 281, 299, 313, 323, 329, 0],
        [0, 1, 5, 13, 25, 41, 61, 82, 103, 124, 145, 166, 187, 208, 229, 250, 271, 291, 307, 319, 327, 331, 0],
        [0, 3, 9, 19, 33, 51, 72, 93, 114, 135, 156, 177, 198, 219, 240, 261, 282, 300, 314, 324, 330, 0, 0],
        [0, 6, 14, 26, 42, 62, 83, 104, 125, 146, 167, 188, 209, 230, 251, 272, 292, 308, 320, 328, 0, 0, 0],
        [0, 10, 20, 34, 52, 73, 94, 115, 136, 157, 178, 199, 220, 241, 262, 283, 301, 315, 325, 0, 0, 0, 0],
        [0, 15, 27, 43, 63, 84, 105, 126, 147, 168, 189, 210, 231, 252, 273, 293, 309, 321, 0, 0, 0, 0, 0],
        [0, 21, 35, 53, 74, 95, 116, 137, 158, 179, 200, 221, 242, 263, 284, 302, 316, 0, 0, 0, 0, 0, 0],
        [0, 28, 44, 64, 85, 106, 127, 148, 169, 190, 211, 232, 253, 274, 294, 310, 0, 0, 0, 0, 0, 0, 0],
        [0, 36, 54, 75, 96, 117, 138, 159, 180, 201, 222, 243, 264, 285, 303, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 45, 65, 86, 107, 128, 149, 170, 191, 212, 233, 254, 275, 295, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 55, 76, 97, 118, 139, 160, 181, 202, 223, 244, 265, 286, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 66, 87, 108, 129, 150, 171, 192, 213, 234, 255, 276, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    TVSA_pins_types = {
        0: 'BC',
        1: 'GC',
        2: 'CC',
        3: 'FU_1.3',
        4: 'FU_2.2',
        5: 'FU_3.0',
        6: 'FU_3.6',
        7: 'FU_4.0',
        8: 'GDFU_2.4_5.0',
        9: 'GDFU_3.3_5.0'
    }

    TVSA_30AV5_cells_types = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 8, 5, 5, 5, 5, 5, 5, 5, 8, 5, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 0],
        [0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 0, 0, 0, 5, 5, 5, 5, 1, 5, 8, 5, 1, 5, 5, 5, 5, 1, 5, 5, 5, 5, 0],
        [0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 0, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 8, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 8, 5, 5, 1, 5, 5, 5, 5, 2, 5, 5, 5, 5, 1, 5, 5, 8, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 5, 0, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0],
        [0, 5, 5, 5, 5, 1, 5, 5, 5, 5, 1, 5, 5, 5, 1, 5, 5, 5, 5, 0, 0, 0, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 8, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0],
        [0, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 5, 8, 5, 5, 5, 5, 5, 5, 5, 8, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    lattice = Lattice('TVSA', TVSA_cells_numbers, TVSA_30AV5_cells_types, TVSA_pins_types)
    lattice.write_to_file('test_lattice')



