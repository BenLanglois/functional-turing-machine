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
        return self._position

    def set_flag(self, flag_name):
        self._flags[flag_name] = self.get_position()

    def goto_flag(self, flag_name):
        if flag_name in self._flags.keys():
            self._position = self._flags[flag_name]
        else:
            raise KeyError("Invalid flag name.")

    def __repr__(self):
        "A list-like representation of the tape, where the cursor looks like: '>X<'"
        return (('[' if self.get_position() == 0 else '[ ') +
			' '.join(str(cell) for cell in self._tape[0:self.get_position()]) +
			f">{self.selected}<" +
			' '.join(str(cell) for cell in self._tape[self.get_position() + 1:]) +
			(']' if self.get_position() + 1 == len(self._tape) else ' ]'))

def assert_valid_variable_name(name, allow_asterisk, line_num):
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



if __name__ == "__main__":

    # Get command line arguments
    command_line_args = sys.argv

    # Get file name
    if len(command_line_args) == 2:
        input_file_name = command_line_args[1]
    elif len(command_line_args) == 1:
        input_file_name = input("Enter input file name: ")

    # Read file
    with open(input_file_name) as input_file:
        script = input_file.readlines()

    # Compile the script
    expressions = {}
    _valid_functions = ["!flag", "!goto"]

    for line_num, line in enumerate(script):
        # Use a 1-indexed line number
        line_num += 1

        if '#' in line:
            # The line has a comment on it
            line = line[:line.index('#')]

        # Remove whitespace
        line = line.strip()

        if len(line) > 0:
            # Validate the expression and add it to a dictionary
            args = line.split()

            if len(args) != 5:
                # Wrong number of arguments in expression
                raise ValueError(f"Invalid expression on line {line_num}.")

            elif len(args) == 5 and args[2][0] == "!":
                # Expression calls a function
                initial_state = assert_valid_variable_name(args[0], False, line_num)
                initial_value = assert_valid_value(args[1], line_num)
                function = assert_valid_function_name(args[2], line_num)
                flag_name = assert_valid_variable_name(args[3], False, line_num)
                final_state = assert_valid_variable_name(args[4], True, line_num)

                if (initial_state, initial_value) in expressions:
                    # Repeated expression
                    raise ValueError(f"Repeated expression on line {line_num}.")

                if final_state in (initial_state, '*'):
                    # Infinite loop
                    raise ValueError(f"Infinite loop detected on line {line_num}.")

                # Add expression
                expressions[(initial_state, initial_value)] = {"is_function": True, "function": function, "flag_name": flag_name, "final_state": final_state}

            else:
                # Expression does not call a function
                initial_state = assert_valid_variable_name(args[0], False, line_num)
                initial_value = assert_valid_value(args[1], line_num)
                final_value = assert_valid_value(args[2], line_num)
                move = assert_valid_move(args[3], line_num)
                final_state = assert_valid_variable_name(args[4], True, line_num)

                if (initial_state, initial_value) in expressions:
                    # Repeated expression
                    raise ValueError(f"Repeated expression on line {line_num}.")

                if move == '*' and final_state in ('*', initial_state) and ('*' in (initial_value, final_value) or final_value == initial_value):
                    # Infinite loop
                    raise ValueError(f"Infinite loop detected on line {line_num}.")

                # Add expression
                expressions[(initial_state, initial_value)] = {"is_function": False, "final_value": final_value, "move": move, "final_state": final_state}


    # print(''.join(script))
    # print('\n'.join(f"{key} -> {expressions[key]}" for key in expressions) + '\n')

    # Initialize the tape
    tape = TuringTape()
    curr_state = "start"
    print(tape)

    # Run the program
    while True:
        # Get the current command
        try:
            cmd = expressions[(curr_state, '*')]
        except KeyError:
            try:
                cmd = expressions[(curr_state, tape.selected)]
            except KeyError:
                break

        if cmd["is_function"]:
            # Execute function
            if cmd["function"] == "!flag":
                tape.set_flag(cmd["flag_name"])
            elif cmd["function"] == "!goto":
                try:
                    tape.goto_flag(cmd["flag_name"])
                except KeyError:
                    raise ValueError(f"Flag name {cmd['flag_name']} referenced before initialization.")
            else:
                # This should never be reachable, but is here for extra safety
                raise ValueError(f"Invalid function {cmd['function']}")

            if cmd["final_state"] != '*':
                curr_state = cmd["final_state"]

        else:
            # Set the selected value
            if cmd["final_value"] != '*':
                tape.selected = cmd["final_value"]

            move = cmd["move"]
            if move[0] in ['>', '<']:
                colon = move.index(':')
                count = int(move[1:colon])
                fill = '*' if move[colon+1] == '*' else int(move[move.index(':')+1:])
                if move[0] == '>':
                    tape.right(count, fill)
                else:
                    tape.left(count, fill)

            if cmd["final_state"] != '*':
                curr_state = cmd["final_state"]

        print(tape)
