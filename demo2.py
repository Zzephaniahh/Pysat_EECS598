# pysat demo2: bounded model checking
import warnings # eliminate an annoying warning message about bidict.
warnings.filterwarnings("ignore", message="Python 2 support will be dropped in a future release.")

import pysat
import parser

from pysat.formula import CNF			# Load the CNF module
from pysat.solvers import Minisat22		# Load the Minisat solver

s = Minisat22()					# Create solver

# Library to parse the symbolic CNF into DIMACS array format
CNF_clauses, var_dict = parser.cnf_parser("demo2_3.scnf").parse()
#print(CNF_clauses) # uncomment these lines to see the contents from the parser
#print(var_dict)


T = CNF(from_clauses = CNF_clauses) # add the CNF clauses to a PySAT CNF object

s.append_formula(T.clauses)			# Load T into the solver
print(s.solve())					# Solve
print(s.get_model())				# Satisfying assignment

property_name0 = "P_0"
property_int0 = var_dict[property_name0]

# property_int1 = var_dict[property_name1]
# property_name1 = "P_1"

# property_int2 = var_dict[property_name2]
# property_name2 = "P_2"

print("Assumption added here")
s.solve(assumptions = [-property_int0])			# Add the constraint that the output neq must be 1
print(s.get_model())				# Satisfying assignment

    # if s.get_model() is not None:
    #     continue
    # else:
    #     break

    # print(s.get_model())				# This should be unsatisfiable!
    #
    # print(s.get_core())				# And here's the "reason"
    #
    # s.delete()					# Clean up
