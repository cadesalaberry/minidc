'''
minidc.py
Created on 2013-02-23
@author: J. Berthiaume
'''

import subprocess
import sys
import os

class minidc():
    
#    def __init__(self):
#        if len(user_input) == 2:
#            return self.runDC(user_input[1]) # Run from test program
#        elif len(user_input) == 1:
#            return self.runDC('')          # Run from user input
#        else:
#            print "Error: %s " % user_input

    # Pushes a value onto the appropriate stack. Returns True if there is an error, False otherwise
    def push_value(self, val):
        
        #If the first character is an underscore, we have a negative number
        if val[0] == '_':
            # Convert to a list so that it is mutable, then add the negative sign and change back to string
            val_list = list(val)        
            val_list[0] = '-'
            val = ''.join(val_list)
        
        # If it's a number, add to the value stack. Otherwise, add to the command stack.    
        try:
            f_val = float(val)       
            if f_val > sys.maxint or f_val < -sys.maxint:
                # Error: number out of range
                error = "Error: number out of range\n"
                sys.stderr.write(error)
                self.add_err_to_log(error)
                return -2
            else:
                val_stack.append(f_val)        
            return 0
        except ValueError:
            if val in valid_commands:
                # The command is valid
                cmd_stack.append(val)
                return 0
            else:
                # The command is invalid: revert the stack to its previous state
                error = "Unknown command: \'%s\' does not exist\n" % val
                sys.stderr.write(error)
                self.add_err_to_log(error)
                self.revert_stack()
                return -1
                
        
    def handle_input(self):

        # Keep going until the command stack runs out of values
        while cmd_stack: 
            
            # Pop the first command off the stack and handle it       
            curr_cmd = cmd_stack.pop()        
            
            if curr_cmd == 'exit':  
                # Exit the application
                print "Goodbye." 
                return False  
                      
            elif curr_cmd == 'p':
                # Print the top number in the stack without popping it
                try:
                    output = str(val_stack[-1])
                    print output  
                    self.add_output_to_log(output) 
                except IndexError:
                    error = "Error: stack is empty\n"
                    sys.stderr.write(error)
                    self.add_err_to_log(error)
                    self.revert_stack()  
                            
            elif curr_cmd == 'n':
                # Print the top number in the stack and pop it
                try:
                    output = str(val_stack.pop())
                    print output
                    self.add_output_to_log(output) 
                except IndexError:
                    error = "Error: stack is empty\n"
                    sys.stderr.write(error)
                    self.add_err_to_log(error)
                    self.revert_stack()     
                             
            elif curr_cmd == 'f':
                # Print the whole stack
                output = str(val_stack) 
                print output
                self.add_output_to_log(output)
                          
            elif curr_cmd == '+':
                # Add the top two numbers in the stack and push the result
                try:
                    val_stack.append(val_stack.pop() + val_stack.pop())
                except IndexError:
                    error = "Error: could not perform operation - stack does not contain 2 values\n"
                    sys.stderr.write(error)
                    self.add_err_to_log(error)
                    self.revert_stack()
                               
            elif curr_cmd == '-':
                #Subtract the second number in the stack from the top number in the stack and push the result
                try:
                    val_stack.append(val_stack.pop() - val_stack.pop())   
                except IndexError:
                    error = "Error: could not perform operation - stack does not contain 2 values\n"
                    sys.stderr.write(error)
                    self.add_err_to_log(error)
                    self.revert_stack()     
                     
            elif curr_cmd == '*':
                # Multiply the top two numbers in the stack and push the result
                try:
                    val_stack.append(val_stack.pop() * val_stack.pop()) 
                except IndexError:
                    error = "Error: could not perform operation - stack does not contain 2 values\n"
                    sys.stderr.write(error)
                    self.add_err_to_log(error)
                    self.revert_stack()   
                       
            elif curr_cmd == '/':
                # Divide the top two numbers in the stack and push the result
                try:
                    try:
                        val_stack.append(val_stack.pop() / val_stack.pop())
                    except ZeroDivisionError:
                        error = "Error: cannot divide by zero\n"
                        sys.stderr.write(error)
                        self.add_err_to_log(error)
                        self.revert_stack()                        
                except IndexError:
                    error = "Error: could not perform operation - stack does not contain 2 values\n"
                    sys.stderr.write(error)
                    self.add_err_to_log(error)
                    self.revert_stack()  
                           
            else:
                # Program should never get here, as error cases are handled in push_value
                error = "Unexpected error"
                sys.stderr.write(error)
                self.add_err_to_log(error)
                self.revert_stack
                return False
        
        # Save the current state of the stack
        self.update_stack()                 
        return True
    
    def parse_input(self, input):
        # Turns a string input from the test program into a list of commands
        user_input = input.split("|")
        
        for i in range(len(user_input)):
            user_input[i] = user_input[i].split()
            user_input[i].reverse()
           
        return user_input
    
    def runDC(self, *input_vals):    
        run = True
        error = 0                    
        f1 = open('stderr.txt', 'w')
        f2 = open('stdout.txt', 'w')
        
        # Temp variables to save state of stdout/stderr
        t1 = sys.stderr
        t2 = sys.stdout  
        # Write stderr/stdout to a file instead of the console
        sys.stderr = f1 
        sys.stdout = f2
        
        # Make sure there wasn't too many arguments provided
        if len(input_vals) > 1:
            sys.stderr.write("Incorrect usage: too many arguments\n")
            sys.stderr = t1
            sys.stdout = t2
            f1.close()  
            f2.close()
            return -1
        else:
            input = input_vals[0]
        
        if input == '':
            # No arguments = input taken from stdin
            print "Welcome to minidc."
            
            # Print to console instead of file
            sys.stderr = t1
            sys.stdout = t2
            f1.close()  
            f2.close()    
            
            while run:  
                error = 0                     
                # Get the user's input and split it up into a list of arguments (delimiter is whitespace)
                sys.stdout.write('>>')
                user_input = raw_input().split()
                user_input.reverse()
                
                # Add the input values to the stack
                for element in user_input:
                    if error >= 0:
                        error = self.push_value(element) 
    
                run = self.handle_input() 
            print "\nAfter execution, the stack contains the following values: %s" % str(val_stack) 
            return val_stack #returns the full stack once operation is done
        
        else:
            # Argument provided = input taken from test program  
    
            
            # The input should be a string where individual commands are separated by a the character "|"
            # Example - the input "1 2 + | 3 4 +" simulates a user entering the command "1 2 +" followed by the command "3 4 +"                    
            user_input = self.parse_input(input)
    
            for command in user_input:
                error = 0
                # Add the individual values to the stack
                for element in command:
                    if error >= 0:
                        error = self.push_value(element)          
                
                # Reverse the input command for display in the console, then change it back before handling the command
#                command.reverse()
#                print ">> %s" % str( ' '.join(command) )
#                command.reverse()
                self.handle_input() 
#                print "Actual: %s\n" % str(val_stack) ###DEBUG### 
            sys.stderr = t1
            sys.stdout = t2
            f1.close()  
            f2.close()    
            return val_stack #returns the full stack once operation is done
        
    def update_stack(self):
        global val_stack
        global val_stack_old
        global cmd_stack
        global cmd_stack_old
        val_stack_old = val_stack[:] 
        cmd_stack_old = cmd_stack[:] 
    
    def revert_stack(self):
        # Reverts the stack to the previously saved state
        global val_stack
        global val_stack_old
        global cmd_stack
        global cmd_stack_old
        val_stack = val_stack_old[:]
        cmd_stack = cmd_stack_old[:]        
        
    def clear_stack(self):   
        # Clears the stack completely       
        global val_stack
        global val_stack_old
        global cmd_stack
        global cmd_stack_old     
        val_stack = []
        val_stack_old = []
        cmd_stack = []
        cmd_stack_old = []
    
    def add_err_to_log(self, err_entry):
        global err
        err.append(err_entry)
        
    def read_err_log(self):
        global err
        return err
    
    def clear_err_log(self):
        global err
        err = []
        
    def add_output_to_log(self, stdout_entry):
        global output
        output.append(stdout_entry)
        
    def read_output_log(self):
        global output
        return output
    
    def clear_output_log(self):
        global output
        output = []
    
valid_commands = ['p', 'n', 'f', '+', '-', '*', '/', 'exit']
val_stack = []
val_stack_old = []
cmd_stack = []
cmd_stack_old = []
err = []
output = []

if __name__ == "__main__":
    mdc = minidc()
    if len(sys.argv) == 2:
        mdc.runDC(sys.argv[1]) # Run from input string
    elif len(sys.argv) == 1:
        mdc.runDC('')          # Run from interactive user input
    else:
        sys.stderr.write("Incorrect usage. Check your arguments\n")