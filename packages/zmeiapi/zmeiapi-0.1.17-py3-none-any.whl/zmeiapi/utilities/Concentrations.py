from zmeiapi.data.Materials import materials_data, nuclides_masses_dict, nuclides_dict, N_AVO


class SimpleMaterialConcentrations:
    """
    Класс для расчета концентраций нуклидов в простых материалах (материалов, в которых задана плотность и массовые
    доли всех нуклидов)
    """

    def __init__(self, material=None, density=6.0):
        """
        :param material: имя материала, соответствующие параметры материала будут найдены из
        модуля data.MaterialsParameters (материал должен быть прописан там)
        :type material: str
        :param density: плотность материала [г/см3]
        :type density: float
        """
        self.density = density
        if material is None:
            self.nuclides = None
        else:
            self.nuclides = materials_data[material]['nuclides']

        if material is None:
            self.concentrations = None
        else:
            self.concentrations = []
            for i, nuclide in enumerate(self.nuclides):
                nuclide_concentration = materials_data[material]['mass_fractions'][nuclide] * self.density * \
                                        N_AVO / nuclides_masses_dict[nuclide]
                self.concentrations.append(nuclide_concentration)


class UO2MaterialConcentration:
    def __init__(self, enrichment=3.0, density=10.2):
        """
        :param density: плотность топлива [г/см3]
        :param enrichment: обогащение топлива по урану-235 [%]
        :var self.nuclides: список нуклидов топлива
        :var N_U235: ядерная концентрация урана-235
        :var N_U238: ядерная концентрация урана-238
        :var N_O: ядерная концентрация кислорода
        :var self.concentrations: список ядерных концентраций нуклидов, порядок соответствует списку self.nuclides
        """
        self.nuclides: list = ['U-235', 'U-238', 'O-16']
        M_U235 = nuclides_masses_dict['U-235']
        M_U238 = nuclides_masses_dict['U-238']
        M_O = nuclides_masses_dict['O-16']
        N_U235 = density * N_AVO / M_U235 / \
                 (
                         (1 + 2 * M_O / M_U235) +
                         (1 + 2 * M_O / M_U238) * ((100. - enrichment) / enrichment)
                 )
        N_U238 = density * N_AVO / M_U238 / \
                 (
                         (1 + 2 * M_O / M_U235) * enrichment / (100. - enrichment) +
                         (1 + 2 * M_O / M_U238)
                 )
        N_O = 2. * (N_U235 + N_U238)

        self.concentrations: list = [N_U235, N_U238, N_O]
        w_U235 = M_U235 / (enrichment / 100 * (M_U235 + M_O) + (1.0 - enrichment / 100) * (M_U238 + M_O))
        w_U238 = M_U238 / (enrichment / 100 * (M_U235 + M_O) + (1.0 - enrichment / 100) * (M_U238 + M_O))
        w_O = M_O / (enrichment / 100 * (M_U235 + M_O) + (1.0 - enrichment / 100) * (M_U238 + M_O))
        self.mass_fractions: list = [w_U235, w_U238, w_O]


class MixTwoMaterialConcentrations:
    def __init__(self, nuclides_1, concentrations_1, nuclides_2, concentrations_2, mass_fraction_1=0.5):
        self.nuclides_1: list = nuclides_1
        self.nuclides_2: list = nuclides_2
        self.concentrations_1: list = concentrations_1
        self.concentrations_2: list = concentrations_2
        self.mass_fraction_1: float = mass_fraction_1
        self.mass_fraction_2: float = 1.0 - mass_fraction_1
        self.nuclides_concentrations_dict_1: dict = {}
        self.nuclides_concentrations_dict_2: dict = {}
        self.resulting_nuclides: list = []
        self.resulting_concentrations: list = []
        self.resulting_nuclides_concentrations: dict = {}

        self.generate_nuclides_concentrations_dictionaries()
        self.calculate_resulting_nuclides_and_concentrations()
        self.mix()
        self.resulting_nuclides = list(self.resulting_nuclides_concentrations.keys())
        self.resulting_concentrations = list(self.resulting_nuclides_concentrations.values())

    def generate_nuclides_concentrations_dictionaries(self):
        for i, nuclide in enumerate(self.nuclides_1):
            self.nuclides_concentrations_dict_1[nuclide] = self.concentrations_1[i]
        for i, nuclide in enumerate(self.nuclides_2):
            self.nuclides_concentrations_dict_2[nuclide] = self.concentrations_2[i]

    def calculate_resulting_nuclides_and_concentrations(self):
        for key in self.nuclides_concentrations_dict_1.keys():
            self.nuclides_concentrations_dict_1[key] = self.nuclides_concentrations_dict_1[key] * self.mass_fraction_1
        for key in self.nuclides_concentrations_dict_2.keys():
            self.nuclides_concentrations_dict_2[key] = self.nuclides_concentrations_dict_2[key] * self.mass_fraction_2

    def mix(self):
        common_keys = set(self.nuclides_concentrations_dict_1).intersection(self.nuclides_concentrations_dict_2)
        unique_keys = set(self.nuclides_concentrations_dict_1).symmetric_difference(self.nuclides_concentrations_dict_2)
        for key in common_keys:
            self.resulting_nuclides_concentrations[key] = self.nuclides_concentrations_dict_1[key] + \
                                                          self.nuclides_concentrations_dict_2[key]
        for key in unique_keys:
            if key in self.nuclides_concentrations_dict_1:
                self.resulting_nuclides_concentrations[key] = self.nuclides_concentrations_dict_1[key]
            if key in self.nuclides_concentrations_dict_2:
                self.resulting_nuclides_concentrations[key] = self.nuclides_concentrations_dict_2[key]


if __name__ == '__main__':
    b = UO2MaterialConcentration(enrichment=19.5)
    print(b.nuclides)
    print(b.concentrations)

    b_1 = UO2MaterialConcentration(enrichment=17.8)
    print(b_1.nuclides)
    print(b_1.concentrations)
    from zmeiapi.objects.Material import Material

    m = Material('gd2o3', nuclides=b.nuclides, concentrations=b.concentrations)
    # for line in m.lines:
    #    print(line)

    a = SimpleMaterialConcentrations(material='АК-12')
    print(a.nuclides)
    print(a.concentrations)

    c = MixTwoMaterialConcentrations(a.nuclides, a.concentrations, b.nuclides, b.concentrations,
                                     mass_fraction_1=0.593)
    print(c.resulting_nuclides_concentrations)
    for key in c.resulting_nuclides_concentrations.keys():
        print(f'${key}$ & {round(c.resulting_nuclides_concentrations[key], 5):4f} \\\\ \hline%')

    c_1 = MixTwoMaterialConcentrations(a.nuclides, a.concentrations, b_1.nuclides, b_1.concentrations,
                                       mass_fraction_1=0.593)
    print(c_1.resulting_nuclides_concentrations)
    for key in c_1.resulting_nuclides_concentrations.keys():
        print(f'${key}$ & {round(c_1.resulting_nuclides_concentrations[key], 5):4f} \\\\ \hline%')
