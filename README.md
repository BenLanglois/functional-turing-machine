# Functional Turing Machine

## What is a Turing Machine?
A Turing machine is a mathematical computer that was proposed by Alan Turing in 1936. Turing machines run simple programs, and expressions typically consist of an initial state, an initial value, a move, a final state, and a final value. You can read more [here](https://en.wikipedia.org/wiki/Turing_machine). Several simulations exist online that can run Turing machine programs (a quick Google search will return several results).

## What is the Function Turing Machine Language?
Turing machine programs can be fun to write, however more complex programs can quickly become very tedious to write. The goal of the Functional Turing Machine language is to combine the simplicity of Turing machines with a few key features from modern programming languages. The most important feature of Functional Turing Machine is "flags", which enables the programmer to keep track of various positions on the tape. This allows programs to jump back and forth between flags, test for flag locations, and pass flags as parameters to functions.

## Running Functional Turing Machine Programs
The Functional Turing Machine compiler is written in Python. You will need to have Python 3.6 or higher installed to run the compiler. To compile and run a Function Turing Machine script, run the `functional_turing_machine.py` program. If you do not pass any command line arguments, you will be prompted to input a filename. Filenames must end with the extension `.ftm`.

Alternatively, you can pass the filename as the first command line argument. If you choose this method, you can also specify up to 4 additional arguments. These are:
- `-max_tape N`: Sets the maximum size of the tape to `N`. The default value is 10000.
- `-max_stack N`: Sets the maximum recursion/stack depth to `N`. The default value is 1000.
- `-print_tape`: Causes the program to print the tape after every step.
- `-print_state`: Causes the program to print the state name after every step. Note that this will cause the tape to be printed whether or not `-print_tape` is passed.

I would recommend aliasing the `functional_turing_machine.py` file to make it easier to run programs. The alias should resemble:

    alias ftm="python3 ~/PATH_TO_FILENAME/functional_turing_machine.py"


# Syntax

If you would like to see some examples of working Functional Turing Machine programs, look in the `examples` folder in this repository.

## Basics
All memory in Functional Turing Machine programs is stored on a "tape" (or an array). There can only be `1`s and `0`s on the tape. The tape can only be accessed at one position on the tape at a time. The tape at the start of a program is initialized to all zeros. The initial position of the tape at the start of execution is at the first element. The position can never extend below the first element of the tape or above the maximum size of the tape (specified by the `-max_tape` command line argument).

Each expression in a Functional Turing Machine program must be on its own line. All expressions must be inside of a function. The `main` function will be called at the start of execution, so that is where your program will start.

All expressions consist of an `initial_state` and an `initial_value`. For an expression to be executed, its `initial_state` must match the current state of the program, and its `initial_value` must match the value at the current position on the tape.

Valid variable names contain letters, digits, and/or underscores (`a-z`, `A-Z`, `0-9`, or `_`). The variable name cannot be composed only of digits (i.e. it must contain at least one letter or underscore).

Flags are special positions on the tape that can be added or moved. You cannot access their address directly, but they can be jumped to, tested for, and passed as parameters to functions. Flag names must be valid variable names.

## Comments
A comment start with a `#` symbol. All text on the line after this symbol will be ignored by the compiler.

## Function Declarations
All expressions must appear inside of a user-define function. To declare a function, use the following syntax:
```
@function_name (parameters) initial_state
```

- `function_name`: A valid variable name. It must be unique from all other function names.
- `parameters`: A list of comma separated flag names.
- `initial_state`: The state that the tape will be set to when the function is executed.

The end of a function is signified by the start of another function or the end of the file.

## Function Scope
Functions cannot access flags from another scope. In order to pass flags from another scope, they must be passed as parameters to the function. Flags are passed as values, not as references (i.e. a function cannot modify another function's flags). When a function is called and when a function returns, the current position of the tape will not be changed. Functions cannot directly return information, however they can change the position of the tape and modifiy values on the tape.





## This README is not complete. It will be finished shortly.
