class BurnupInput:
    def __init__(self):
        self.mvol = None
        self.pcc = None
        self.inventory = 'all'
        self.printm = 1
        self.butot = None
        self.powdens = None
        pass

    def _compile_inventory(self, file):
        if self.inventory is None:
            pass
        else:
            file.write(f'set inventory {self.inventory} \n')

    def _compile_printm(self, file):
        if self.printm is None:
            pass
        elif type(self.printm) != int:
            pass
        else:
            file.write(f'set printm {self.printm}')

    def _compile_mvol(self, file):
        if self.mvol is None:
            pass

    def _compile_pcc(self, file):
        if self.pcc is None:
            pass
        else:
            file.write(f'set pcc {self.pcc[0]} {int(self.pcc[1])} {int(self.pcc[2])}')

    def _compile_powdens(self, file):
        if self.powdens is None:
            pass
        else:
            file.write(f'set powdens {float(self.powdens):10.5E}')

    def _compile_butot(self, file):
        if self.butot is None:
            pass
        else:
            file.write(f'dep butot \n')
            for burnup in self.butot:
                file.write(f'{burnup:10.5E} \n')

    def compile(self, filename):
        with open(filename, 'w') as file:
            self._compile_inventory(file)
            self._compile_printm(file)
            file.write('\n')
            self._compile_mvol(file)
            file.write('\n')
            self._compile_pcc(file)
            file.write('\n')
            self._compile_powdens(file)
            file.write('\n')
            self._compile_butot(file)
            file.write('\n')
        pass
