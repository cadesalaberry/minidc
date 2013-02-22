#Assignment B
#Test Driven Development

## Specifications

* Due Feb 24, 2013 (23:59)
* Group of 2 students
* Implement the **minidc** application with TDD 

### Info

Minidc ‐ Modelled after the UNIX command line tool “dc”.

* Minidc is a reverse‐polish desk calculator.   Minidc reads from the standard input.  All normal output is to standard output; all error output is to standard error.

* A reverse‐polish calculator stores numbers on a stack.  Entering a number pushes it on the stack. Arithmetic operations pop arguments off the stack and push the results.

* To enter a number in Minidc, type the digits with an optional decimal point. To enter a negative number, begin the number with “_”.  “‐” cannot be used for this, as it is the operator for subtraction instead.


###Available commands

	P
>Prints the value on the top of the stack, without altering the stack.

	n
>Prints the value on the top of the stack, popping it off.

	f
>Prints the entire contents of the stack without altering anything.

	+
>Pops two values off the stack, adds them, and pushes the result.

	‐
>Pops two values off the stack, subtracts the first one popped from the second one popped, and pushes the result.

	*
>Pops two values, multiplies them, and pushes the result.

	/
>Pops two values, divides the second one popped from the first one popped, and pushes the result.


## Instructions

Order of TDD should start by exercising valid domain  logic, invalid domain logic, valid input 
syntax, invalid input syntax and then valid and invalid parameter types and numbers.

To get full marks:

* All tests should have clearly indicated purposes.

* A clear indication should be made showing the test failing before code is added.

* A clear indication should be made showing which code has been added.

* There is a clear indication (strong evidence) that failed test pass after new code is added.

* There is a clear indication (strong evidence) that all previous tests pass after new code is added.

* No invalid input should pass to the program without displaying an error.

* The test progression should be clear.

* The tests are processed in order (ie. logic-syntax-parameters).

* Tests should not be redundant.

* Formatting should be clear and easy to follow.

* Student ID and Name are specified in the submission.

**Note that the assignment is out of 20, but if you accumulate too much malus points you can end at -44**
