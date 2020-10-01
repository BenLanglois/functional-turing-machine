# Functional Turing Machine

## What is a Turing Machine?

A Turing Machine is a mathematical computer that was proposed by Alan Turing in 1936. Turing Machines run simple programs, and expressions typically consist of an initial state, an initial value, a move, a final state, and a final value. You can read more [here](https://en.wikipedia.org/wiki/Turing_machine). Several simulations exist online that can run Turing Machine programs.

## What is the Functional Turing Machine language?

Turing Machine programs can be fun to write, however more complex programs can quickly become very tedious to write. The goal of the Functional Turing Machine language is to combine the simplicity of Turing Machines with a few key features from modern programming languages. The most important feature of Functional Turing Machine is "flags", which enables the programmer to keep track of various positions on the tape. This allows programs to jump back and forth between flags, test for flag locations, and pass flags as parameters to functions.

## Running Functional Turing Machine programs

The Functional Turing Machine interpreter is written in Python. You will need to have Python 3.6 or higher installed to run the interpreter. To run a Function Turing Machine script, run the `functional_turing_machine.py` program. If you do not pass any command line arguments, you will be prompted to input a filename. Filenames must end with the extension `.ftm`.

Alternatively, you can pass the filename as the first command line argument. If you choose this method, you can also specify up to 4 settings. These settings are:

- `--max-tape N`: Sets the maximum size of the tape to `N`. The default value is 10000.
- `--max-stack N`: Sets the maximum recursion/stack depth to `N`. The default value is 1000.
- `--print-tape`: Causes the program to output a representation of the tape after every step.
- `--print-state`: Causes the program to print the state name after every step. Implies `--print-tape`.

For ease of access, you may want to create an alias for running `functional_turing_machine.py`.

    alias ftm="python3 /PATH/TO/FILE/functional_turing_machine.py"

## Language specification

### Basics

#### The tape

All memory in Functional Turing Machine programs is stored on a "tape". There can only be `1`s and `0`s on the tape. The tape can only be accessed at one position on the tape at a time. The tape at the start of execution is initialized to all `0`s. The initial position of the tape at the start of execution is at the left-most position. The position can never extend to the left of the left-most position or to the right of the maximum size of the tape (specified by the `--max_tape` command line argument).

#### Comments

The `#` symbol denotes the start of a single-line comment. All characters after the symbol are ignored.

#### Variable names

Valid variable names use the characters `a-z`, `A-Z`, `0-9`, and `_`. There must be at least one non-digit character somewhere in the name. This applies to function names, flag names, and state names.

#### Whitespace

Each instruction must be separated by at least one newline character. Instructions may be preceded or followed by any number of spaces.

#### Scope

Functions have global scope and can be called from anywhere. Flags and states have local scope and can only be accessed by instructions in the same function definition.

### Syntax

#### Instructions

Each line in a program can be split into four categories:

- Blank line
- Comment
- Function definition
- Instruction

Blank lines and lines with only a comment do not change the execution of the program. Function definitions (described below) always begin with an `@` symbol preceded by zero or more spaces. All other lines are instructions. There must be at least one function definition before the first instruction in a program. All instructions follow the basic syntax:

    INITIAL_STATE INITIAL_VALUE ... NEXT_STATE

where:

- `INITIAL_STATE` is the state that the Turing Machine must be in in order to execute the instruction. It can be any valid variable name.
- `INITIAL_VALUE` describes the value that must be at the current position on the tape in order to execute the instruction. It must be one of the following symbols:
  - `0` will only run the instruction if the value at the current position on the tape is 0.
  - `1` will only run the instruction if the value at the current position on the tape is 1.
  - `*` will match any value at the current position on the tape.
- `NEXT_STATE` is the state that the Turing Machine will be in after the instruction has been executed. It can be any valid variable name or `*` to match `INITIAL_STATE`.
- `...` is syntax specific to each instruction

In order for an instruction to run, the Turing Machine must be in the state `INITIAL_STATE` AND the value that must be at the current position on the tape must match `INITIAL_VALUE`. No two instructions in the same function may have the `INITIAL_STATE` and `INITIAL_VALUE`.

#### Function definitions

Function definitions have the following syntax:

    @FUNCTION_NAME ( PARAM_1, PARAM_2, ... ) INITIAL_STATE

where:

- `FUNCTION_NAME` is the name of the function being defined.
- `PARAM_1`, `PARAM_2`, ... are the comma-separated parameters for the function. Zero or more parameters may be declared. These parameters are flags defined in the function's scope.
- `INITIAL_STATE` is the state that the function will begin execution in.

**Program execution always begins at the function named `main`.** There must be a definition for the `main` function that takes no parameters in every program.

User-defined function names must not match any of the built-in function names, which are:

- `flag`
- `goto`
- `if`
- `input`
- `print_str`
- `print_val`

Instructions following the function declaration belong to the function being defined. The function ends when another function is declared or the end of the file is reached.

Function names must be unique across the entire program. Flag and parameter names must be unique throughout the function they are defined in.

**Example:** Define a function named `foo` which takes two parameters `a` and `b` and begins execution in state `start`.

    @foo (a, b) start

#### Calling user-defined functions

Calling user-defined functions has the following syntax:

    INITIAL_STATE INITIAL_VALUE !FUNCTION_NAME ( PARAM_1, PARAM_2, ... ) NEXT_STATE

where:

- `FUNCTION_NAME` is the name of the function that is being called.
- `PARAM_1`, `PARAM_2`, ... are the comma-separated parameters for the function. The number of parameters passed to the function must match the number of parameters declared in the function definition. These parameters must be flags defined in the local scope.

The state is set to `NEXT_STATE` after the function is finished execution; it does not determine which state the function begins execution in.

Parameters are passed as values, not as references. This means that if the callee function modifies the value of its parameters, the caller function's flags will not me modified.

**Example:** Call a function named `foo` which takes two parameters `a` and `b`. `foo` should be called if the state is `call_foo` and the value at the current position on the tape is 1. After `foo` is called, the next state should be `done`.

    call_foo 1 !foo(a, b) done

#### Move, set, and fill

TODO

#### If statement

TODO

### Built-in functions

TODO
