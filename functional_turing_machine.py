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

def _unescape(in_str):
    index = 0
    out_str = ""
    while index < len(in_str):
        if in_str[index] == "\\":
            out_str += in_str[index+1]
            index += 2
        else:
            out_str += in_str[index]
            index += 1
    return out_str

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

    file_name_pattern = re.compile(r"^\w+\.ftm$")

    if file_name_pattern.match(input_file_name) is None:
        raise NameError('Invalid file name. Functional Turing Machine files must end with ".ftm"')


    # Read file
    with open(input_file_name) as input_file:
        script = input_file.readlines()

    # Compile the script
    functions = {}
    curr_function = None
    empty_line_pattern = re.compile(r"^\s*(?:#.*)?$")
    new_func_pattern = re.compile(r"^\s*@(?P<name>[a-zA-Z_]\w*)\s*\((?P<parameters>(?:\s*[a-zA-Z_]\w*\s*(?:,\s*[a-zA-Z_]\w*\s*)*)|(?:\s*))\)\s*(?P<initial_state>[a-zA-Z_]\w*)\s*(?:#.*)?$")
    exec_func_pattern = re.compile(r"^\s*(?P<initial_state>[a-zA-Z_]\w*)\s+(?P<initial_value>[01\*])\s+!(?P<function>[a-zA-Z_]\w*)\s*\((?P<parameters>(?:\s*[a-zA-Z_]\w*\s*(?:,\s*[a-zA-Z_]\w*\s*)*)|(?:\s*))\)\s+(?P<final_state>[a-zA-Z_]\w*|\*)\s*(?:#.*)?$")
    move_pattern = re.compile(r"^\s*(?P<initial_state>[a-zA-Z_]\w*)\s+(?P<initial_value>[01\*])\s+(?P<final_value>[01\*])\s+(?P<operation>[<>\*])(?:(?<!\*)(?P<count>[1-9][0-9]*)?(?::(?P<fill>[01\*]))?)?\s+(?P<final_state>[a-zA-Z_]\w*|\*)\s*(?:#.*)?$")
    if_pattern = re.compile(r"^\s*(?P<initial_state>[a-zA-Z_]\w*)\s+(?P<initial_value>[01\*])\s+!if\s*\(\s*(?P<condition>[a-zA-Z_]\w*)\s*\)\s*(?P<true_state>[a-zA-Z_]\w*)\s*:\s*(?P<false_state>[a-zA-Z_]\w*)\s*(?:#.*)?$")
    input_pattern = re.compile(r'^\s*(?P<initial_state>[a-zA-Z_]\w*)\s+(?P<initial_value>[01\*])\s+!input\s*\(\s*(?P<min_count>[1-9]\d*)\s*,\s*(?:(?P<max_count>[1-9]\d*),\s*)?"(?P<prompt>(?:(?<!\\)(?:\\{2})*\\"|[^"\\])*(?<!\\)(?:\\{2})*)"\s*\)\s*(?P<final_state>[a-zA-Z_]\w*|\*)\s*(?:#.*)?$')
    print_pattern = re.compile(r'^\s*(?P<initial_state>[a-zA-Z_]\w*)\s+(?P<initial_value>[01\*])\s+!print\s*\(\s*"(?P<text>(?:(?<!\\)(?:\\{2})*\\"|[^"\\])*(?<!\\)(?:\\{2})*)"\s*\)\s*(?P<final_state>[a-zA-Z_]\w*)\s*(?:#.*)?$')

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

            if name in ("flag", "goto", "if", "input", "print"):
                # User tried to re-define builtin function
                raise ValueError(f'Unable to re-define builtin function "!{name}" on line {line_num}.')

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
            if function in ("if", "input", "print"):
                raise ValueError(f'Incorrect syntax for executing builtin function "!{function}" on line {line_num}.')

            parameters = []
            for p in exec_func_match.group("parameters").split(','):
                if p.strip() != '':
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

        if_match = if_pattern.match(line)
        if if_match is not None:
            initial_state = if_match.group("initial_state")
            initial_value = if_match.group("initial_value")
            condition = if_match.group("condition")
            true_state = if_match.group("true_state")
            false_state = if_match.group("false_state")

            if initial_state in (true_state, false_state):
                # Infinite loop
                raise ValueError(f"Infinite loop detected on line {line_num}.")

            functions[curr_function]["expressions"][(initial_state, initial_value)] = \
                {"is_function": True, "function": "if", "condition": condition, "true_state": true_state, "false_state": false_state}
            continue

        input_match = input_pattern.match(line)
        if input_match is not None:
            initial_state = input_match.group("initial_state")
            initial_value = input_match.group("initial_value")
            min_count = input_match.group("min_count")
            max_count = input_match.group("max_count")
            prompt = input_match.group("prompt")
            final_state = input_match.group("final_state")

            if max_count is None:
                max_count = min_count
            elif int(max_count) < int(min_count):
                raise ValueError(f"The maximum input count is less than the minimum input count on line {line_num}.")

            if final_state == initial_state:
                # Infinite loop
                raise ValueError(f"Infinite loop detected on line {line_num}.")

            functions[curr_function]["expressions"][(initial_state, initial_value)] = \
                {"is_function": True, "function": "input", "min_count": min_count, "max_count": max_count, "prompt": _unescape(prompt), "final_state": final_state}

            continue

        print_match = print_pattern.match(line)
        if print_match is not None:
            initial_state = print_match.group("initial_state")
            initial_value = print_match.group("initial_value")
            text = print_match.group("text")
            final_state = print_match.group("final_state")

            if final_state == initial_state:
                # Infinite loop
                raise ValueError(f"Infinite loop detected on line {line_num}.")

            functions[curr_function]["expressions"][(initial_state, initial_value)] = \
                {"is_function": True, "function": "print", "text": _unescape(text), "final_state": final_state}
            continue

        # Invalid expression
        raise ValueError(f"Invalid expression on line {line_num}.")

    if "main" not in functions.keys():
        raise ValueError("No main function specified.")

    '''
    # print all expressions
    for f in functions:
        print(f"Name: {f}, Parameters: {functions[f]['parameters']}")
        for e in functions[f]["expressions"]:
            print(e, functions[f]["expressions"][e])
    '''


    # Initialize the tape
    tape = TuringTape()
    stack = [{"name": "main", "flags": {}, "state": functions["main"]["initial_state"]}]

    # Run the program
    while True:
        print(tape)

        # Get the current command
        try:
            cmd = functions[stack[-1]["name"]]["expressions"][(stack[-1]["state"], '*')]
        except KeyError:
            try:
                cmd = functions[stack[-1]["name"]]["expressions"][(stack[-1]["state"], str(tape.selected))]
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

            elif cmd["function"] == "if":
                if cmd["condition"] not in stack[-1]["flags"].keys():
                    raise KeyError(f"Flag name {cmd['condition']} referenced before creation.")
                if stack[-1]["flags"][cmd["condition"]] == tape.get_position():
                    stack[-1]["state"] = cmd["true_state"]
                else:
                    stack[-1]["state"] = cmd["false_state"]

            elif cmd["function"] == "input":
                # Get user input
                user_input = input(cmd["prompt"] + ' ')
                user_input_pattern = re.compile("^[01]{" + cmd["min_count"] + ',' + cmd["max_count"] + "}$")
                user_input_match = user_input_pattern.match(user_input)

                while not user_input_match:
                    # Get valid user input
                    if min_count == max_count:
                        if min_count == '1':
                            user_input = input(f"ERROR: Enter a 0 or a 1: ")
                        else:
                            user_input = input(f"ERROR: Enter exactly {cmd['min_count']} 0s and 1s: ")
                    else:
                        user_input = input(f"ERROR: Enter between {cmd['min_count']} and {cmd['max_count']} 0s and 1s: ")

                    user_input_match = user_input_pattern.match(user_input)

                # Add user input to the tape
                for bit in user_input_match.group():
                    tape.selected = int(bit)
                    tape.right(1, '*')

                stack[-1]["state"] = cmd["final_state"]

            elif cmd["function"] == "print":
                print(cmd["text"])
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
            # Move expression
            # Set the selected value
            if cmd["final_value"] != '*':
                tape.selected = int(cmd["final_value"])

            if cmd["operation"] == '<':
                tape.left(int(cmd["count"]), cmd["fill"])
            elif cmd["operation"] == '>':
                tape.right(int(cmd["count"]), cmd["fill"])

            if cmd["final_state"] != '*':
                stack[-1]["state"] = cmd["final_state"]
