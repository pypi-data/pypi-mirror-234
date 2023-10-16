__version__ = "0.0.1"
__author__ = "Vlad Romanenko"


from zmeiapi.zmei_io.Logger import logger


class General:
    def __init__(self):
        self.title = "None"
        self.acelib = "None"
        self.nfylib = "None"
        self.declib = "None"
        self.ures = 1
        self.include = None
        self.gcu = [0]
        self.bc = 1
        self.pop = [10000, 100, 20]
        self.src = "n"
        self.repro = 0
        self.shbuf = [0, 0]
        self.poi = None
        self.cmm = 1
        self.micro = 'defaultmg_ext'
        self.ene = ['g1', 1, 1E-09, 2.15E-06, 20.0]
        self.nfg = self.ene[0]
        self.div = None
        self.materials_lines = []
        self.pins_lines = []
        self.surfaces_lines = []
        self.cells_lines = []
        self.burnup_lines = []
        self.additional_lines = []
        pass

    def _compile_title(self, file):
        file.write(f'set title \"{self.title}\" \n')

    def _compile_acelib(self, file):
        file.write(f'set acelib \"{self.acelib}\" \n')

    def _compile_nfylib(self, file):
        file.write(f'set nfylib \"{self.nfylib}\" \n')

    def _compile_declib(self, file):
        file.write(f'set declib \"{self.declib}\" \n')

    def _compile_ures(self, file):
        file.write(f'set ures {int(self.ures)} \n')

    def _compile_include(self, file):
        if self.include is None:
            pass
        elif type(self.include) is list:
            for f in self.include:
                file.write(f'include \"{f}\" \n')
        else:
            logger.error(f'Include attribute must have a list type')
            raise AttributeError(f'Include attribute must have a list type')

    def _compile_gcu(self, file):
        if self.gcu is None:
            pass
        elif (type(self.gcu) is list) or (type(self.gcu) is int):
            _line = 'set gcu '
            for f in self.gcu:
                _line += f'{f} '
            file.write(f'{_line} \n')
        else:
            logger.error(f'Gcu attribute must have a list type {type(self.gcu)}')
            raise AttributeError(f'Gcu attribute must have a list type')

    def _compile_bc(self, file):
        if self.bc is None:
            pass
        elif (self.bc == 1) or (self.bc == 2):
            file.write(f'set bc {self.bc} \n')
        else:
            logger.error(f'Bc attribute possible values must be 1 or 2')
            raise AttributeError(f'Bc attribute possible values must be 1 or 2')

    def _compile_pop(self, file):
        if self.pop is None:
            pass
        elif type(self.pop) is list:
            _line = 'set pop '
            for f in self.pop:
                if type(f) == int:
                    _line += f'{f} '
                else:
                    logger.error(f'Pop attribute must contain integer numbers')
                    raise AttributeError(f'Pop attribute must contain integer numbers')
            file.write(f'{_line} \n')
        else:
            logger.error(f'Pop attribute must have a list type')
            raise AttributeError(f'Pop attribute must have a list type')

    def _compile_src(self, file):
        if self.src is None:
            pass
        elif self.src == "n":
            file.write(f'src {self.src} \n')
        else:
            logger.error(f'Src attribute possible values must be "n" or None')
            raise AttributeError(f'Src attribute possible values must be "n" or None')

    def _compile_poi(self, file):
        if self.poi is None:
            pass
        elif type(self.poi) == list and len(self.poi) == 2:
            file.write(f'set poi {int(self.poi[0])} {self.poi[1]}\n')

    def _compile_micro(self, file):
        file.write(f'set micro {self.micro} \n')

    def _compile_ene(self, file):
        file.write(f'ene {self.ene[0]} {int(self.ene[1])} \n')
        for i in range(2, len(self.ene)):
            file.write(f'{self.ene[i]} \n')

    def _compile_nfg(self, file):
        file.write(f'set nfg {self.nfg} \n')

    def _compile_cmm(self, file):
        file.write(f'set cmm {self.cmm} \n')

    def _compile_repro(self, file):
        file.write(f'set repro {self.repro} \n')

    def _compile_shbuf(self, file):
        file.write(f'set shbuf {self.shbuf[0]} {self.shbuf[1]} \n')

    def _compile_div(self, file):
        if self.div is None:
            pass
        else:
            for key in self.div.keys():
                file.write(f'div {key} sep {int(self.div[key][0])} '
                           f'subr {int(self.div[key][1])} {self.div[key][2]} {self.div[key][3]} \n')

    def _compile_additional_lines(self, file):
        for line in self.additional_lines:
            file.write(f'{line} \n')

    def compile(self, filename):
        with open(filename, 'w') as file:
            self._compile_title(file)
            file.write('\n')
            self._compile_acelib(file)
            self._compile_nfylib(file)
            self._compile_declib(file)
            file.write('\n')
            self._compile_ures(file)
            file.write('\n')
            self._compile_repro(file)
            self._compile_shbuf(file)
            file.write('\n')
            self._compile_include(file)
            file.write('\n')
            self._compile_bc(file)
            file.write('\n')
            self._compile_pop(file)
            file.write('\n')
            self._compile_src(file)
            file.write('\n')
            self._compile_micro(file)
            file.write('\n')
            self._compile_ene(file)
            file.write('\n')
            self._compile_nfg(file)
            self._compile_gcu(file)
            self._compile_cmm(file)
            file.write('\n')
            self._compile_poi(file)
            file.write('\n')
            self._compile_div(file)
            file.write('\n')
            self._compile_additional_lines(file)
            file.write('\n')


if __name__ == '__main__':
    general = General()

    general.compile('input')
