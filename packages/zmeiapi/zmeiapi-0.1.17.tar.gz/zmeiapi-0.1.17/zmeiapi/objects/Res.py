from zmeiapi.zmei_io.Logger import logger
from zmeiapi.data.Parameters import NUCLIDES_DICT_PATH, res_keys


class Res:
    def __init__(self, name):
        self.name = name
        self.burnup_step = None

        self.results = {}
        for key in res_keys:
            self.results[key] = []
        pass

    def fill_values_from_lines(self, lines):
        for line in lines:
            for key in self.results.keys():
                if line.startswith(key):
                    splited_line = line.split('=')
                    res_line = splited_line[-1].split()
                    if key == 'MACRO_NG':
                        self.results[key].append(res_line[0])
                        # print(key, self.results[key])
                    elif key == 'BURN_STEP':
                        self.results[key].append(res_line[0])
                    elif key == 'GC_UNIVERSE_NAME':
                        self.results[key].append(res_line[0].strip("'"))
                    elif key == 'BURN_STEP':
                        self.results[key].append(res_line[0])
                    else:
                        # print(self.results[key])
                        # print(key, self.results[key], res_line[1:-1])
                        self.results[key].append(res_line[1:-1])
                        self.results[key] = self.results[key][0]

        self._results_to_float()
        if self.results['GC_UNIVERSE_NAME'] is not None:
            self.name = self.results['GC_UNIVERSE_NAME']
        if self.results['BURN_STEP'] is not None:
            self.burnup_step = int(self.results['BURN_STEP'][0])

    def _results_to_float(self):
        for key in self.results.keys():
            if type(self.results[key]) is list and key != 'GC_UNIVERSE_NAME':
                for i, el in enumerate(self.results[key]):
                    self.results[key][i] = float(el)


if __name__ == '__main__':
    pass
    # r = Res()
    # print(r.results)
