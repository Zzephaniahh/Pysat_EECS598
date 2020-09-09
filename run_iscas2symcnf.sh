# An ISC file is needed to start, please follow isc formatting exactly as the tool is not forgiving for poor syntax

./iscas2symcnf s27.isc test_out.cnf

# produces a CNF file which can be read into pysat using the parser library
# An example of how to intake the .cnf is shown in pysat_examp.py

python cnf_intake_example.py
