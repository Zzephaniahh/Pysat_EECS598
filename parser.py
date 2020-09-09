import re # used for parsing
class cnf_parser(): # takes the ISCAS 89 file as input and finds all input output pairs
    def __init__(self, ISCAS_filename):
        self.filename = ISCAS_filename
        self.variable_dict = {}
        self.variables = []
        self.DIMACS_counter = 1
        self.CNF_formula = []

    def get_variables(self, line):
        found = re.search('\((.+?)\)', line).group(1) # find each input set inside brackets (x1 ... xn)
        return str(found).split(" + ") # split into a list of inputs [x1, ... xn]

    def var_to_dimacs_dict_update(self):
        for variable in self.variables:
            if "!" in variable:
                variable = variable[1:]
            if variable not in self.variable_dict:
                self.variable_dict[variable] = self.DIMACS_counter
                self.DIMACS_counter += 1

    def get_formula(self):
        CNF = []
        for variable in self.variables:
            if "!" in variable:
                CNF.append(-1*self.variable_dict[variable[1:]])
            else:
                CNF.append(self.variable_dict[variable])
        return CNF

    def parse(self):
        file_id = open(self.filename, "r")
        lines = file_id.readlines()
        for line in lines:

            if "#" in line or "DFF" in line:
                continue

            self.variables = self.get_variables(line)

            self.var_to_dimacs_dict_update()

            CNF = self.get_formula()

            self.CNF_formula.append(CNF)

        self.variable_dict = {v: k for k, v in self.variable_dict.iteritems()}

        return self.CNF_formula, self.variable_dict


"""
TODO: Consider using bidict
"""
