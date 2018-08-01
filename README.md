# Functional Turing Machine

## What is a Turing Machine?
A Turing machine is a mathematical computer that was proposed by Alan Turing in 1936. Turing machines run simple programs, and expressions typically consist of an initial state, an initial value, a move, a final state, and a final value. You can read more [here](https://en.wikipedia.org/wiki/Turing_machine). Several simulations exist online that can run Turing machine programs (a quick Google search will return several results).

## What is the Function Turing Machine Language?
Turing machine programs can be fun to write, however more complex programs can quickly become very tedious to write. The goal of the Functional Turing Machine language is to combine the simplicity of Turing machines with a few key features from modern programming languages. The most important feature of Functional Turing Machine is "flags", which enables the programmer to keep track of various positions on the tape. This allows programs to jump back and forth between flags, test for flag locations, and pass flags as parameters to functions.

## Running Functional Turing Machine Programs
The Functional Turing Machine compiler is written in Python. You will need to have Python 3.6 or higher installed to run the compiler. To compile and run a Function Turing Machine script, run the `functional_turing_machine.py` program. If you do not pass any command line arguments, you will be prompted to input a filename. Filenames must end with the extension `.ftm`.

Alternatively, you can pass the filename as the first command line argument. If you choose this method, you can also specify up to 4 settings. These settings are:
- `-max_tape`: Sets the maximum size of the tape.
- `-max_stack`: Sets the maximum recursion/stack depth.
- `-print_tape`: Causes the program to print the tape after every step.
- `-print_state`: Causes the program to print the state name after every step. Note that this will cause the tape to be printed regardless of `-print_tape` being passed or not.

If you are running on a Mac, I recommend aliasing the `functional_turing_machine.py` file in your `.bash_profile`. Add a line that resembles:

    alias ftm="python3 ~/PATH_TO_FILENAME/functional_turing_machine.py"

### This README is not complete. It will be finished shortly.
