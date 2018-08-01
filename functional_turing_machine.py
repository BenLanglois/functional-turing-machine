import sys
import re

class TuringTape:
    def __init__(self, max_size, new_cell_value=0):
        "Create a tape with maximum size max_size and where new cells are set to new_cell_value."
        self._new_cell_value = new_cell_value
        self._tape = [self._new_cell_value]
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
            self._tape += [self._new_cell_value] * (1 + self.get_position() + count - len(self._tape))

        if fill != '*':
            # Change all cells that the tape moves over to the fill value
            for i in range(self.get_position() + 1, self.get_position() + count + 1):
                self._tape[i] = fill

        # Move the cursor
        self._position += count

    def left(self, count, fill):
        "Moves the tape to the left and returns the selected value after the move."
        if self.get_position() - count < 0:
            raise IndexError("TuringTape cannot extend below position 0.")

        if fill != '*':
            # Change all cells that the tape moves over to the fill value
            for i in range(self.get_position() - count, self.get_position()):
                self._tape[i] = fill

        # Move the cursor
        self._position -= count

    def get_position(self):
        "Returns the position of the tape."
        return self._position

    def set_position(self, new_pos):
        "Sets the position of the tape."
        if not isinstance(new_pos, int):
            raise TypeError("new_pos must be an integer")
        if 0 <= new_pos < len(self._tape):
            self._position = new_pos
        else:
            raise IndexError("Index out of range of tape.")

    def get_value_at(self, pos):
        if 0 <= pos < len(self._tape):
            return self._tape[pos]
        else:
            raise IndexError("Index out of range of tape")

    def __repr__(self):
        "A list-like representation of the tape, where the cursor looks like: '>X<'"
        return (('[' if self.get_position() == 0 else '[ ') +
			' '.join(str(cell) for cell in self._tape[0:self.get_position()]) +
			f">{self.selected}<" +
			' '.join(str(cell) for cell in self._tape[self.get_position() + 1:]) +
			(']' if self.get_position() + 1 == len(self._tape) else ' ]'))

if __name__ == "__main__":
    class Stack:
        def __init__(self, max_size):
            self._items = []
            self._max_size = max_size

        def is_empty(self):
            return len(self._items) == 0

        def __len__(self):
            return len(self._items)

        def add(self, name, flags, state):
            if len(self) == self._max_size:
                raise IndexError(f"Stack has reached its maximum size of {self._max_size}.")
            self._items.append({"name": name, "flags": flags, "state": state})

        def pop(self):
            self._items.pop()

        @property
        def name(self):
            return self._items[-1]["name"]

        @property
        def state(self):
            return self._items[-1]["state"]

        @state.setter
        def state(self, new_state):
            self._items[-1]["state"] = new_state

        def get_flag(self, flag):
            return self._items[-1]["flags"][flag]

        def set_flag(self, flag, pos):
            self._items[-1]["flags"][flag] = pos

    # Get command line arguments
    settings = {}

    if len(sys.argv) == 1:
        input_file_name = input("Enter input file name: ")
    else:
        input_file_name = sys.argv[1]
        i = 2
        while i < len(sys.argv):
            arg = sys.argv[i].lower()

            if arg == "-max_tape":
                # Sets the maximum tape size
                if "max_tape_size" in settings.keys():
                    raise ValueError("Argument -max_tape specified more than once.")
                settings["max_tape_size"] = int(sys.argv[i+1])
                if settings["max_tape_size"] < 1:
                    raise ValueError("Maximum tape size must be at least 1.")
                i += 2

            elif arg == "-max_stack":
                # Sets the maximum stack size
                if "max_stack_size" in settings.keys():
                    raise ValueError("Argument -max_stack specified more than once.")
                settings["max_stack_size"] = int(sys.argv[i+1])
                if settings["max_stack_size"] < 1:
                    raise ValueError("Maximum stack size must be at least 1.")
                i += 2

            elif arg == "-print_tape":
                # Print the tape after every step
                if "print_tape" in settings.keys():
                    raise ValueError("Argument -print_tape specified more than once.")
                settings["print_tape"] = True
                i += 1

            elif arg == "-print_state":
                # Print the state after every step
                if "print_state" in settings.keys():
                    raise ValueError("Argument -print_state specified more than once.")
                settings["print_state"] = True
                i += 1

            else:
                # Invalid command line argument
                raise KeyError(f"Invalid argument: {arg}.")

    # Set defaults if not specified in comand line
    if "max_stack_size" not in settings.keys():
        settings["max_stack_size"] = 1000
    if "max_tape_size" not in settings.keys():
        settings["max_tape_size"] = 10000
    if "print_tape" not in settings.keys():
        settings["print_tape"] = False
    if "print_state" not in settings.keys():
        settings["print_state"] = False

    file_name_pattern = re.compile(r"^\w+\.ftm$")

    # Validate file name
    if file_name_pattern.match(input_file_name) is None:
        raise NameError('Invalid file name. Functional Turing Machine files must end with ".ftm"')

    # Read file
    with open(input_file_name) as input_file:
        script = input_file.readlines()

    # Initialize variables
    functions = {}
    curr_function = None

    # Compile regexes
    empty_line_pattern = re.compile(r"^\s*(?:#.*)?$")
    new_func_pattern = re.compile(r"^\s*@(?P<name>\d*[a-zA-Z_]\w*)\s*\((?P<parameters>(?:\s*\d*[a-zA-Z_]\w*\s*(?:,\s*\d*[a-zA-Z_]\w*\s*)*)|(?:\s*))\)\s*(?P<initial_state>\d*[a-zA-Z_]\w*)\s*(?:#.*)?$")
    exec_func_pattern = re.compile(r"^\s*(?P<initial_state>\d*[a-zA-Z_]\w*)\s+(?P<initial_value>[01\*])\s+!(?P<function>\d*[a-zA-Z_]\w*)\s*\((?P<parameters>(?:\s*\d*[a-zA-Z_]\w*\s*(?:,\s*\d*[a-zA-Z_]\w*\s*)*)|(?:\s*))\)\s+(?P<next_state>\d*[a-zA-Z_]\w*|\*)\s*(?:#.*)?$")
    move_pattern = re.compile(r"^\s*(?P<initial_state>\d*[a-zA-Z_]\w*)\s+(?P<initial_value>[01\*])\s+(?P<next_value>[01\*])\s+(?P<operation>[<>\*])(?:(?<!\*)(?P<count>[1-9][0-9]*)?(?::(?P<fill>[01\*]))?)?\s+(?P<next_state>\d*[a-zA-Z_]\w*|\*)\s*(?:#.*)?$")
    if_pattern = re.compile(r"^\s*(?P<initial_state>\d*[a-zA-Z_]\w*)\s+(?P<initial_value>[01\*])\s+!if\s*\(\s*(?P<condition>\d*[a-zA-Z_]\w*)\s*\)\s*(?P<true_state>\d*[a-zA-Z_]\w*)\s*:\s*(?P<false_state>\d*[a-zA-Z_]\w*)\s*(?:#.*)?$")
    input_pattern = re.compile(r'^\s*(?P<initial_state>\d*[a-zA-Z_]\w*)\s+(?P<initial_value>[01\*])\s+!input\s*\(\s*(?P<min_count>[1-9]\d*|0)\s*,\s*(?:(?P<max_count>[1-9]\d*),\s*)?"(?P<prompt>.*)"\s*\)\s*(?P<next_state>\d*[a-zA-Z_]\w*|\*)\s*(?:#.*)?$')
    print_str_pattern = re.compile(r'^\s*(?P<initial_state>\d*[a-zA-Z_]\w*)\s+(?P<initial_value>[01\*])\s+!print_str\s*\(\s*"(?P<text>.*)"\s*\)\s*(?P<next_state>\d*[a-zA-Z_]\w*)\s*(?:#.*)?$')

    # Compile the script
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

            if name in ("flag", "goto", "if", "input", "print_str"):
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
            # Expression calls a non-special function
            initial_state = exec_func_match.group("initial_state")
            initial_value = exec_func_match.group("initial_value")
            initial_value = '*' if initial_value == '*' else int(initial_value)

            if (initial_state, initial_value) in functions[curr_function]["expressions"].keys():
                # Repeated expression
                raise ValueError(f"Repeated expression on line {line_num}.")

            function = exec_func_match.group("function")
            if function in ("if", "input", "print_str"):
                # Special function called with normal syntax
                raise ValueError(f'Incorrect syntax for executing builtin function "!{function}" on line {line_num}.')

            parameters = []
            for p in map(str.strip, exec_func_match.group("parameters").split(',')):
                if p != '':
                    parameters.append(p)

            next_state = exec_func_match.group("next_state")

            if function in ("flag", "print_val") and next_state in (initial_state, '*'):
                # Infinite loop
                raise ValueError(f"Infinite loop detected on line {line_num}.")
            elif function == "goto" and next_state in (initial_state, '*') and initial_state == '*':
                # Infinite loop
                raise ValueError(f"Infinite loop detected on line {line_num}.")

            if (function in ("goto, flag") and len(parameters) != 1) or (function == "print_val" and not 0 <= len(parameters) <= 2):
                # Invalid builtin function call
                raise ValueError(f'Incorrect number of parameters for function "!{function}" on line {line_num}.')


            # Add expression
            functions[curr_function]["expressions"][(initial_state, initial_value)] = \
                {"is_function": True, "function": function, "parameters": parameters, "next_state": next_state}

            continue

        move_match = move_pattern.match(line)
        if move_match is not None:
            # Expression does not call a function
            initial_state = move_match.group("initial_state")
            initial_value = move_match.group("initial_value")
            initial_value = '*' if initial_value == '*' else int(initial_value)

            if (initial_state, initial_value) in functions[curr_function]["expressions"].keys():
                # Repeated expression
                raise ValueError(f"Repeated expression on line {line_num}.")

            next_value = move_match.group("next_value")
            next_value = '*' if next_value == '*' else int(next_value)
            operation = move_match.group("operation")
            count = int(move_match.group("count") or 1)
            fill = move_match.group("fill") or '*'
            fill = '*' if fill == '*' else int(fill)
            next_state = move_match.group("next_state")

            if operation == '*' and next_state in ('*', initial_state) and ('*' in (initial_value, next_value) or next_value == initial_value):
                # Infinite loop
                raise ValueError(f"Infinite loop detected on line {line_num}.")

            # Add expression
            functions[curr_function]["expressions"][(initial_state, initial_value)] = \
                {"is_function": False, "next_value": next_value, "operation": operation, "count": count, "fill": fill, "next_state": next_state}

            continue

        if_match = if_pattern.match(line)
        if if_match is not None:
            initial_state = if_match.group("initial_state")
            initial_value = if_match.group("initial_value")
            initial_value = '*' if initial_value == '*' else int(initial_value)
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
            initial_value = '*' if initial_value == '*' else int(initial_value)
            # Note: Leave min and max count as strings because they will need to be added to a regex string later
            min_count = input_match.group("min_count")
            max_count = input_match.group("max_count")
            prompt = input_match.group("prompt")
            next_state = input_match.group("next_state")

            if max_count is None:
                if min_count == '0':
                    raise ValueError(f"The minimum input count was 0 and the maximum input count was not specified on line {line_num}.")
                else:
                    max_count = min_count
            elif int(max_count) < int(min_count):
                raise ValueError(f"The maximum input count is less than the minimum input count on line {line_num}.")

            if next_state in ('*', initial_state) and initial_value == '*':
                # Infinite loop
                raise ValueError(f"Infinite loop detected on line {line_num}.")

            functions[curr_function]["expressions"][(initial_state, initial_value)] = \
                {"is_function": True, "function": "input", "min_count": min_count, "max_count": max_count, "prompt": prompt, "next_state": next_state}

            continue

        print_str_match = print_str_pattern.match(line)
        if print_str_match is not None:
            initial_state = print_str_match.group("initial_state")
            initial_value = print_str_match.group("initial_value")
            initial_value = '*' if initial_value == '*' else int(initial_value)
            text = print_str_match.group("text")
            next_state = print_str_match.group("next_state")

            if next_state == initial_state:
                # Infinite loop
                raise ValueError(f"Infinite loop detected on line {line_num}.")

            functions[curr_function]["expressions"][(initial_state, initial_value)] = \
                {"is_function": True, "function": "print_str", "text": text, "next_state": next_state}
            continue

        # Invalid expression
        raise ValueError(f"Invalid expression on line {line_num}.")

    if "main" not in functions.keys():
        raise ValueError("No main function specified.")

    # Initialize the tape
    tape = TuringTape(settings["max_tape_size"])
    stack = Stack(settings["max_stack_size"])
    stack.add("main", {}, functions["main"]["initial_state"])

    # Run the program
    while True:
        # Get the current command
        try:
            cmd = functions[stack.name]["expressions"][(stack.state, '*')]
        except KeyError:
            try:
                cmd = functions[stack.name]["expressions"][(stack.state, tape.selected)]
            except KeyError:
                # Remove top layer from the stack
                stack.pop()
                if stack.is_empty():
                    break
                else:
                    continue

        # Print the tape/state to the screen as specified in the command line arguments
        if settings["print_state"]:
            print(tape, f"Next state: {stack.state}")
        elif settings["print_tape"]:
            print(tape)

        if cmd["is_function"]:
            # Execute function
            if cmd["function"] == "flag":
                if len(cmd["parameters"]) != 1:
                    raise IndexError("Incorrect number of parameters for function !flag.")
                stack.set_flag(cmd["parameters"][0], tape.get_position())
                stack.state = cmd["next_state"]

            elif cmd["function"] == "goto":
                if len(cmd["parameters"]) != 1:
                    raise IndexError("Incorrect number of parameters for function !goto.")
                try:
                    tape.set_position(stack.get_flag(cmd["parameters"][0]))
                except KeyError:
                    raise KeyError(f"Flag name {cmd['parameters'][0]} referenced before creation.")
                stack.state = cmd["next_state"]

            elif cmd["function"] == "if":
                try:
                    if stack.get_flag(cmd["condition"]) == tape.get_position():
                        stack.state = cmd["true_state"]
                    else:
                        stack.state = cmd["false_state"]
                except KeyError:
                    raise KeyError(f"Flag name {cmd['condition']} referenced before creation.")

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

                if cmd["next_state"] != '*':
                    stack.state = cmd["next_state"]

            elif cmd["function"] == "print_str":
                print(cmd["text"])
                stack.state = cmd["next_state"]

            elif cmd["function"] == "print_val":
                if len(cmd["parameters"]) == 0:
                    print(tape.selected)
                    stack.state = cmd["next_state"]
                    continue

                try:
                    first_pos = stack.get_flag(cmd["parameters"][0])
                except KeyError:
                    raise KeyError(f"Flag name {cmd['parameters'][0]} referenced before creation.")

                if len(cmd["parameters"]) == 1:
                    print(tape.get_value_at(first_pos))
                    stack.state = cmd["next_state"]
                    continue

                try:
                    second_pos = stack.get_flag(cmd["parameters"][1])
                except KeyError:
                    raise KeyError(f"Flag name {cmd['parameters'][1]} referenced before creation.")

                if first_pos >= second_pos:
                    raise IndexError(f"Flag {cmd['parameters'][0]} was not found before flag {cmd['parameters'][1]}")

                print(''.join(str(tape.get_value_at(pos)) for pos in range(first_pos, second_pos)))
                stack.state = cmd["next_state"]

            else:
                # Custom function
                if cmd["function"] not in functions.keys():
                    raise ValueError(f"Invalid function {cmd['function']}.")
                if len(cmd["parameters"]) != len(functions[cmd["function"]]["parameters"]):
                    raise IndexError(f"Incorrect number of parameters for function !{cmd['function']}.")

                if cmd["next_state"] != '*':
                    stack.state = cmd["next_state"]

                # Add new layer to stack
                flags = {}
                for i in range(len(cmd["parameters"])):
                    try:
                        flags[functions[cmd["function"]]["parameters"][i]] = stack.get_flag(cmd["parameters"][i])
                    except KeyError:
                        raise KeyError(f"Flag name {cmd['parameters'][i]} referenced before creation.")

                stack.add(cmd["function"], flags, functions[cmd["function"]]["initial_state"])

        else:
            # Move expression
            # Set the selected value
            if cmd["next_value"] != '*':
                tape.selected = cmd["next_value"]

            if cmd["operation"] == '<':
                tape.left(cmd["count"], cmd["fill"])
            elif cmd["operation"] == '>':
                tape.right(cmd["count"], cmd["fill"])

            if cmd["next_state"] != '*':
                stack.state = cmd["next_state"]
