#!/usr/bin/python -i
# Zephaniah Hill | Univeristy of Michigan, Ann Arbor
# July 23, 2020
######################################################################################3333
# Usage: call this file on a .isc benchmark with: python BMC.py input_file.isc outputfile.isc unrolling_depth
# where unrolling_depth is an integer > 0. The circuit is considered the 0th step.


class gate():
    def __init__(self, output, gate_type, input_set):
        self.output = output
        self.type = gate_type
        self.input_set = input_set

class DFF():
    def __init__(self, current, next):
        self.current = current
        self.next = next


class parser(): # takes the ISCAS 89 file as input and finds all input output pairs
    def __init__(self, ISCAS_filename):
        self.filename = ISCAS_filename
        self.gate_dict = {}
        self.output_set = []
        self.input_set = []
        self.DFF_set = []
        self.gate_set = []


    def get_dff(self, line):
        # X = DFF(X_next)
        # Y = DFF(Y_next)
        next_state = str(re.search('\((.+?)\)', line).group(1))
        current_state = str(re.search('(.+?) =', line).group(1))
        self.DFF_set.append(DFF(current_state, next_state))
        #self.DFF_dict[current_state] = next_state

    def get_circuit_output(self, line):
        self.output_set.append(str(re.search('\((.+?)\)', line).group(1))) # add each output to the output set.

    def get_circuit_input(self, line):
        self.input_set.append(str(re.search('\((.+?)\)', line).group(1))) # add each output to the output set.

    def get_output(self, line):
        return str(re.search('(.+?) =', line).group(1)) # save outputs as strings to a variable


    def get_gate_type(self,line):
            return str(re.search('= (.+?)\(', line).group(1)) # find each gate bounded by "= ... ("

    def get_input_set(self, line):
        found = re.search('\((.+?)\)', line).group(1) # find each input set inside brackets (x1 ... xn)
        return str(found).split(", ") # split into a list of inputs [x1, ... xn]

    def parse(self):
        file_id = open(self.filename, "r")
        lines = file_id.readlines()
        for line in lines:
            if "DFF" in line:
                self.get_dff(line)
                continue

            if "OUTPUT" in line:
                self.get_circuit_output(line)
                continue
            if "INPUT" in line:
                self.get_circuit_input(line)
                continue

            if "=" in line: # find all lines with logic gates/circuits
                output = self.get_output(line)

                gate_type = self.get_gate_type(line)

                input_set = self.get_input_set(line)

                temp_gate = gate(output, gate_type, input_set)

                self.gate_set.append(temp_gate)

        return self.gate_set, self.output_set, self.input_set, self.DFF_set




class BMC():
    def __init__(self, ISCAS_output_filename, gate_set, output_set, input_set, DFF_set):
        self.file_ID = ISCAS_output_filename
        self.gate_set = gate_set
        self.output_set = output_set
        self.input_set  = input_set
        self.DFF_set = DFF_set
        #self.unrolling_depth = unrolling_depth
        self.unrolling_level = 1 # start at 1

    def increment_DFF_set(self):
        for DFF in self.DFF_set:
            DFF.current = DFF.next
            if DFF.next in self.input_set: # don't update inputs
                continue
            if DFF.next[len(DFF.next)-2] == "_": # increase the unrolling level
                DFF.next = DFF.next[:len(DFF.next)-2] + "_" + str(self.unrolling_level)
            else:
                DFF.next = DFF.next + "_" + str(self.unrolling_level)

    def is_DFF(self, signal):
        for DFF in self.DFF_set:
            if signal == DFF.current:
                return DFF.next
        else:
            return 0


    def increment_gate(self, gate):
        # update output
        if gate.output not in self.input_set: # don't update inputs
        #if gate.output
            if self.is_DFF(gate.output):
                gate.output = self.is_DFF(gate.output)
            elif gate.output[len(gate.output)-2] == "_": # increase the unrolling level
                gate.output = gate.output[:len(gate.output)-2] + "_" + str(self.unrolling_level)
            else:
                gate.output = gate.output + "_" + str(self.unrolling_level)

        # update input
        for index, input in enumerate(gate.input_set):
            if input in self.input_set:
                continue  # don't update inputs

            if self.is_DFF(input):
                input = self.is_DFF(input)

            elif input[len(input)-2] == "_": # increase the unrolling level
                input = input[:len(input)-2] + "_" + str(self.unrolling_level)
            else:
                input = input + "_" + str(self.unrolling_level)


            gate.input_set[index] = input


    def print_DFF_set_to_file(self):
        self.file_ID.write( "\n##############################################################\n") # space between iterations

        for DFF in self.DFF_set:
            self.file_ID.write(DFF.current + " = DFF(")
            self.file_ID.write(DFF.next + ")\n")

    def print_gate_set_to_file(self):
        self.file_ID.write( "\n") # space between iterations

        #self.file_ID = open(self.filename, "a")
        for gate in self.gate_set:
            self.file_ID.write(gate.output + " = ")
            self.file_ID.write(gate.type)
            input_str = "("
            for input in gate.input_set:
                input_str += str(input) + ", "
            input_str = input_str[:len(input_str) - 2] + ")\n"
            self.file_ID.write(input_str)

    def step_forward(self):

        for gate in self.gate_set:
            self.increment_gate(gate)

        self.increment_DFF_set()
        self.unrolling_level += 1





def main():

    ###############################
    INPUT_FILE = str(sys.argv[1]) #"s27.isc" #
    ###############################


    ###############################
    OUTPUT_FILE = str(sys.argv[2]) # "output_test.isc" #
    ###############################

    ###############################
    unrolling_depth = int(sys.argv[3]) # 2
    ###############################



    gate_set, output_set, input_set, DFF_set = parser(INPUT_FILE).parse()
    file_ID = open(OUTPUT_FILE , "w")

    #print DFF_set
    BMC_Manager = BMC(file_ID, gate_set, output_set, input_set, DFF_set)


    BMC_Manager.print_DFF_set_to_file()
    BMC_Manager.print_gate_set_to_file()

    for unrolling_level in range(0,unrolling_depth):
        BMC_Manager.step_forward()
        BMC_Manager.print_DFF_set_to_file()
        BMC_Manager.print_gate_set_to_file()


if __name__ == '__main__':
    import re # used for parsing
    import sys # used for everything
    main()


"""
 TODO:
 Add all logic functions
 MAybe a clearer way to encode DFF?
"""
