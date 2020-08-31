import parser # all we need to pull in the parser.

CNF_formula, var_dict = parser.cnf_parser('test_out.cnf').parse() # can use the class like a function now.

print CNF_formula # testing functionality
print var_dict
