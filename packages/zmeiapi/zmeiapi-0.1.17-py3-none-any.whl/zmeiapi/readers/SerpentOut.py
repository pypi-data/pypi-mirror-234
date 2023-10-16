from zmeiapi.zmei_io.Logger import logger
from zmeiapi.objects.Res import Res


class OutReader:
    def __init__(self, out_filename):
        self.out_filename = out_filename
        with open(self.out_filename, 'r') as file:
            self.lines = file.readlines()

        self.blines = []
        self.bresults = []
        self.counter_lines = []

        self.results = {
            'ANA_KEFF': [],
            'IMP_KEFF': [],
            'INF_FLX': [],
            # xs results
            'MACRO_NG': [],
            'MACRO_E': [],
            'INF_ABS': [],
            'INF_FISS ': [],
            'INF_NSF': [],
            'INF_S0': [],
            'CMM_DIFFCOEF ': [],
            'INF_I135_YIELD': [],
            'INF_XE135_YIELD': [],
            'INF_PM149_YIELD': [],
            'INF_XE135_MICRO_ABS': [],
            'INF_SM149_MICRO_ABS': [],
            'INF_CHIT': [],
            'INF_CHIP': [],
            'INF_CHID': [],
            'INF_INVV': [],
            'BETA_EFF': [],
            'LAMBDA ': [],
            'BURN_STEP': [],
            'BURNUP ': [],
            'BURN_DAYS': [],
            'GC_UNIVERSE_NAME': []
        }
        self.uni_results = {}
        serpent_res = []
        self.divide_file_to_burnup_steps()

        for bstep, lines in enumerate(self.blines):

            for key in self.results.keys():
                self.results[key].append([])

            for line in self.blines[bstep]:
                for key in self.results.keys():
                    if line.startswith(key):
                        splited_line = line.split('=')
                        res_line = splited_line[-1].split()
                        if key == 'MACRO_NG':
                            self.results[key][bstep].append(res_line[0])
                            # print(key, self.results[key])
                        elif key == 'BURN_STEP':
                            self.results[key][bstep].append(res_line[0])
                        else:
                            # print(self.results[key])
                            self.results[key][bstep].append(res_line[1:-1])
                            self.results[key][bstep] = self.results[key][bstep][0]
                            # print(key, self.results[key])
            # self.bresults.append(self.results)

        self.results_to_float()
        self.divide_file_by_counter()
        self.form_uni_results()

    def divide_file_to_burnup_steps(self):
        with open(self.out_filename, 'r') as file:
            lines = file.read()
        self.blines = lines.split('% Increase counter:')[1:]
        for i, part in enumerate(self.blines):
            self.blines[i] = part.split('\n')
        pass

    def divide_file_by_counter(self):
        with open(self.out_filename, 'r') as file:
            lines = file.read()
        _counter_lines = lines.split('% Increase counter:')[1:]
        self.counter_lines = ['% Increase counter:\n' + line for line in _counter_lines]

    def form_uni_results(self):
        res_objects = []
        for record_number, lines in enumerate(self.counter_lines):
            _r_obj = None
            _r_obj = Res(record_number)
            # print(_r_obj)
            # print(lines)
            _new_lines = lines.split('\n')
            _r_obj.fill_values_from_lines(_new_lines)
            res_objects.append(_r_obj)

        res_universes = [obj.name[0] for obj in res_objects]
        # print(res_universes)
        res_universes = list(set(res_universes))
        # print(res_universes)

        for key in res_universes:
            self.uni_results[key] = []
            for obj in res_objects:
                if obj.name[0] == key:
                    self.uni_results[key].append(obj)

        for key in self.uni_results:
            self.uni_results[key].sort(key=lambda x: x.burnup_step, reverse=False)
            # for obj in self.uni_results[key]:
            #     print(key, obj.burnup_step)
        # for key in self.uni_results['0'][0].results.keys():
        #     print(key, self.uni_results['0'][0].results[key])

    def results_to_float(self):
        # print(len(self.results))
        for key in self.results.keys():
            for bstep in range(len(self.results['ANA_KEFF'])):
                for i, el in enumerate(self.results[key][bstep]):
                    # pass
                    self.results[key][bstep][i] = float(el)

    def print_res(self):
        for key in self.results.keys():
            print(key, self.results[key])


if __name__ == '__main__':
    serpent_results = OutReader('/home/vlad/Serpent/Calculation/SHELF/SHELF_FA_b/SHELF_FA_b_res.m')  # ('FA_OM1_NO_SUZ_3D_b_res.m')
    # serpent_results = SerpentOut('./22AU_b_res.m')
    print(len(serpent_results.bresults))
    print(serpent_results.uni_results['0'])
    for key in serpent_results.uni_results['0'][0].results.keys():
        for i in range(len(serpent_results.uni_results['0'])):
            print(key, i, serpent_results.uni_results['0'][i].results[key])
