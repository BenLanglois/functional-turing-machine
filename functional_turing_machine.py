import sys
import re

class TuringTape:
    def __init__(self, max_size=10000):
        "Create a tape with maximum size max_size."
        self._tape = [0]
        self._position = 0
        self._max_size = int(max_size)
        self._flags = {}

    @property
    def selected(self):
        "Returns the selected value."
        return self._tape[self.get_position()]

    @selected.setter
    def selected(self, new_val):
        "Sets the selected value."
        self._tape[self.get_position()] = new_val

    def right(self, count, fill):
        "Moves the tape to the right and returns the selected value after the move."
        if self.get_position() + count >= self._max_size:
            raise IndexError(f"TuringTape has reached its maximum size of {self._max_size}.")

        if self.get_position() + count >= len(self._tape):
            # Extend the tape
            self._tape += [0] * (1 + self.get_position() + count - len(self._tape))

        if fill != '*':
            # Change all cells that the tape moves over to the fill value
            for i in range(self.get_position() + 1, self.get_position() + count + 1):
                self._tape[i] = int(fill)

        # Move the cursor
        self._position += count

    def left(self, count, fill):
        "Moves the tape to the left and returns the selected value after the move."
        if self.get_position() - count < 0:
            raise IndexError("TuringTape cannot extend below position 0.")

        if fill != '*':
            # Change all cells that the tape moves over to the fill value
            for i in range(self.get_position() - count, self.get_position()):
                self._tape[i] = int(fill)

        # Move the cursor
        self._position -= count

    def get_position(self):
        "Returns the position of the tape."
        return self._position

    def set_position(self, new_pos):
        "Sets the position of the tape."
        if 0 <= new_pos < len(self._tape):
            self._position = new_pos
        else:
            raise IndexError("Index out of range of tape.")

    '''
    def set_flag(self, flag_name):
        self._flags[flag_name] = self.get_position()

    def goto_flag(self, flag_name):
        if flag_name in self._flags.keys():
            self._position = self._flags[flag_name]
        else:
            raise KeyError("Invalid flag name.")
    '''

    def __repr__(self):
        "A list-like representation of the tape, where the cursor looks like: '>X<'"
        return (('[' if self.get_position() == 0 else '[ ') +
			' '.join(str(cell) for cell in self._tape[0:self.get_position()]) +
			f">{self.selected}<" +
			' '.join(str(cell) for cell in self._tape[self.get_position() + 1:]) +
			(']' if self.get_position() + 1 == len(self._tape) else ' ]'))

r'''
def assert_valid_variable_name(name, line_num, allow_asterisk=False):
    if allow_asterisk and name == '*':
        return '*'
    elif isinstance(name, str) and name != "" and name[0].isalpha():
        for char in name[1:]:
            if not (char.isalnum() or char == '_'):
                ValueError(f"Invalid variable name on line {line_num}.")
        return name
    else:
        raise ValueError(f"Invalid variable name on line {line_num}.")

def assert_valid_value(val, line_num):
    if val in ['0', '1']:
        return int(val)
    elif val == '*':
        return val
    else:
        raise ValueError(f"Invalid cell value on line {line_num}.")

def assert_valid_move(mv, line_num):
    if mv == '*':
        return mv
    else:
        move_pattern = re.compile(r"(?P<operation>[<>])(?P<count>[1-9][0-9]*)?(?P<fill>:[01\*])?$")
        match = move_pattern.match(mv)
        if match is not None:
            operation = match.group('operation')
            count = match.group('count') or '1'
            fill = match.group('fill') or ':*'
            return operation + count + fill
        else:
            raise ValueError(f"Invalid move on line {line_num}.")

def assert_valid_function_name(fnc, line_num):
    if fnc in _valid_functions:
        return fnc
    else:
        raise ValueError(f"Invalid function name on line {line_num}.")
'''


if __name__ == "__main__":
    # Get command line arguments
    command_line_args = sys.argv

    # Get file name
    if len(command_line_args) == 2:
        input_file_name = command_line_args[1]
    elif len(command_line_args) == 1:
        input_file_name = input("Enter input file name: ")
    else:
        raise ValueError("Incorrect number of command line arguments.")


    # Read file
    with open(input_file_name) as input_file:
        script = input_file.readlines()

    # Compile the script
    functions = {}
    curr_function = None
    empty_line_pattern = re.compile(r"^\s*(?:#.*)?$")
    new_func_pattern = re.compile(r"^\s*@(?P<name>[a-zA-Z_]\w*)\s*\((?P<parameters>(?:\s*[a-zA-Z_]\w*\s*(?:,\s*[a-zA-Z_]\w*\s*)*)|(?:\s*))\)\s*(?P<initial_state>[a-zA-Z_]\w*)\s*(?:#.*)?$")
    exec_func_pattern = re.compile(r"^\s*(?P<initial_state>[a-zA-Z_]\w*)\s+(?P<initial_value>[01\*])\s+!(?P<function>[a-zA-Z_]\w*)\s+\((?P<parameters>(?:\s*[a-zA-Z_]\w*\s*(?:,\s*[a-zA-Z_]\w*\s*)*)|(?:\s*))\)\s+(?P<final_state>[a-zA-Z_]\w*|\*)\s*(?:#.*)?$")
    # move_pattern = re.compile(r"^\s*(?P<initial_state>[a-zA-Z_]\w*)\s+(?P<initial_value>[01\*])\s+(?P<final_value>[01\*])\s+(?:(?P<operation>[<>])(?P<count>[1-9][0-9]*)?(?::(?P<fill>[01\*]))?|(?:\*))\s+(?P<final_state>[a-zA-Z_]\w*)\s*(?:#.*)?$")
    move_pattern = re.compile(r"^\s*(?P<initial_state>[a-zA-Z_]\w*)\s+(?P<initial_value>[01\*])\s+(?P<final_value>[01\*])\s+(?P<operation>[<>\*])(?:(?<!\*)(?P<count>[1-9][0-9]*)?(?::(?P<fill>[01\*]))?)?\s+(?P<final_state>[a-zA-Z_]\w*|\*)\s*(?:#.*)?$")

    for line_num, line in enumerate(script):
        # Use a 1-indexed line number
        line_num += 1

        empty_line_match = empty_line_pattern.match(line)
        if empty_line_match is not None:
            # Empty line
            continue

        new_func_match = new_func_pattern.match(line)
        if new_func_match is not None:
            # Start of new function

            # Get expression information
            name = new_func_match.group("name")

            if name in functions.keys():
                # Duplicate function name
                raise ValueError(f"Repeated function name on line {line_num}.")

            curr_function = name
            initial_state = new_func_match.group("initial_state")

            # Create new function
            functions[name] = {"parameters": [], "initial_state": initial_state, "expressions": {}}

            # Get parameters
            parameter_string = new_func_match.group("parameters")
            for p in parameter_string.split(','):
                if p.strip() != '':
                    functions[name]["parameters"].append(p.strip())

            # Main function cannot take any parameters
            if name == "main" and len(functions[name]["parameters"]) != 0:
                raise ValueError(f"Main function on line {line_num} must not take any parameters.")

            continue

        if curr_function is None:
            # Expression is not inside of a function
            raise ValueError(f"Expression on line {line_num} is not inside a function.")

        exec_func_match = exec_func_pattern.match(line)
        if exec_func_match is not None:
            # Expression calls a function
            initial_state = exec_func_match.group("initial_state")
            initial_value = exec_func_match.group("initial_value")

            if (initial_state, initial_value) in functions[curr_function]["expressions"].keys():
                # Repeated expression
                raise ValueError(f"Repeated expression on line {line_num}.")

            function = exec_func_match.group("function")
            parameters = []
            for p in exec_func_match.group("parameters").split(','):
                parameters.append(p.strip())

            final_state = exec_func_match.group("final_state")

            if function in ("goto", "flag") and final_state in (initial_state, '*'):
                # Infinite loop
                raise ValueError(f"Infinite loop detected on line {line_num}.")

            # Add expression
            functions[curr_function]["expressions"][(initial_state, initial_value)] = \
                {"is_function": True, "function": function, "parameters": parameters, "final_state": final_state}

            continue

        move_match = move_pattern.match(line)
        if move_match is not None:
            # Expression does not call a function
            initial_state = move_match.group("initial_state")
            initial_value = move_match.group("initial_value")

            if (initial_state, initial_value) in functions[curr_function]["expressions"].keys():
                # Repeated expression
                raise ValueError(f"Repeated expression on line {line_num}.")

            final_value = move_match.group("final_value")
            operation = move_match.group("operation")
            count = move_match.group("count") or '1'
            fill = move_match.group("fill") or '*'
            final_state = move_match.group("final_state")

            if operation == '*' and final_state in ('*', initial_state) and ('*' in (initial_value, final_value) or final_value == initial_value):
                # Infinite loop
                raise ValueError(f"Infinite loop detected on line {line_num}.")

            # Add expression
            functions[curr_function]["expressions"][(initial_state, initial_value)] = \
                {"is_function": False, "final_value": final_value, "operation": operation, "count": count, "fill": fill, "final_state": final_state}

            continue

        # Invalid expression
        raise ValueError(f"Invalid expression on line {line_num}.")

    if "main" not in functions.keys():
        raise ValueError("No main function specified.")

    '''
    for name in functions:
        print(f"name: {name}, initial_state: {functions[name]['initial_state']}")
        for key in functions[name]["expressions"]:
            print(f"{key}: {functions[name]['expressions'][key]}")
        print()
    '''

    # print(''.join(script))

    # Initialize the tape
    tape = TuringTape()
    stack = [{"name": "main", "flags": {}, "state": functions["main"]["initial_state"]}]

    # Run the program
    while True:
        # print(f"{tape}    function: {stack[-1]['name']}    state: {stack[-1]['state']}")
        print(tape)

        # Get the current command
        try:
            cmd = functions[stack[-1]["name"]]["expressions"][(stack[-1]["state"], '*')]
        except KeyError:
            try:
                cmd = functions[stack[-1]["name"]]["expressions"][(stack[-1]["state"], tape.selected)]
            except KeyError:
                # Remove top layer from the stack
                del stack[-1]
                if len(stack) == 0:
                    break
                else:
                    continue


        if cmd["is_function"]:
            # Execute function
            if cmd["function"] == "flag":
                if len(cmd["parameters"]) != 1:
                    raise IndexError("Incorrect number of parameters for function !flag.")
                stack[-1]["flags"][cmd["parameters"][0]] = tape.get_position()
                stack[-1]["state"] = cmd["final_state"]

            elif cmd["function"] == "goto":
                if len(cmd["parameters"]) != 1:
                    raise IndexError("Incorrect number of parameters for function !goto.")
                try:
                    tape.set_position(stack[-1]["flags"][cmd["parameters"][0]])
                except KeyError:
                    raise KeyError(f"Flag name {cmd['parameters'][0]} referenced before creation.")
                stack[-1]["state"] = cmd["final_state"]
            else:
                # Custom function
                if cmd["function"] not in functions.keys():
                    raise ValueError(f"Invalid function {cmd['function']}.")
                elif len(cmd["parameters"]) != len(functions[cmd["function"]]["parameters"]):
                    raise IndexError(f"Incorrect number of parameters for function !{cmd['function']}.")

                if cmd["final_state"] != '*':
                    stack[-1]["state"] = cmd["final_state"]

                # Add new layer to stack
                flags = {}
                for i in range(len(cmd["parameters"])):
                    try:
                        flags[functions[cmd["function"]]["parameters"][i]] = stack[-1]["flags"][cmd["parameters"][i]]
                    except KeyError:
                        raise KeyError(f"Flag name {cmd['parameters'][i]} referenced before creation.")

                stack.append({"name": cmd["function"], "flags": flags, "state": functions[cmd["function"]]["initial_state"]})

        else:
            # Set the selected value
            if cmd["final_value"] != '*':
                tape.selected = cmd["final_value"]

            if cmd["operation"] == '<':
                tape.left(int(cmd["count"]), cmd["fill"])
            elif cmd["operation"] == '>':
                tape.right(int(cmd["count"]), cmd["fill"])

            if cmd["final_state"] != '*':
                stack[-1]["state"] = cmd["final_state"]
