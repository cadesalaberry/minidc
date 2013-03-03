'''
minidc.py
Created on 2013-02-23
@author: J. Berthiaume
'''

import sys

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
        
        global val_stack
        global val_stack_old
        global cmd_stack
        global cmd_stack_old
        
        #If the first character is an underscore, we have a negative number
        if val[0] == '_':
            # Convert to a list so that it is mutable, then add the negative sign and change back to string
            val_list = list(val)        
            val_list[0] = '-'
            val = ''.join(val_list)
        
        # If it's a number, add to the value stack. Otherwise, add to the command stack.    
        try:        
            val_stack.append(float(val))        
            return False
        except ValueError:
            if val in valid_commands:
                # The command is valid
                cmd_stack.append(val)
                return False
            else:
                # The command is invalid: revert the stack to its previous state
                sys.stderr.write("\nUnknown command: \'%s\' does not exist\n" % val)
                val_stack = val_stack_old[:]
                cmd_stack = cmd_stack_old[:]
                return True
                
        
    def handle_input(self):
        
        global val_stack
        global val_stack_old
        global cmd_stack
        global cmd_stack_old
    
        # Keep going until the command stack runs out of values
        while cmd_stack: 
            
            # Pop the first command off the stack and handle it       
            curr_cmd = cmd_stack.pop()        
            
            if curr_cmd == 'exit':  
                # Exit the application
                print "Goodbye." 
                return False            
            elif curr_cmd == 'P':
                # Print the top number in the stack without popping it
                print str(val_stack[-1])            
            elif curr_cmd == 'n':
                # Print the top number in the stack and pop it
                print str(val_stack.pop())            
            elif curr_cmd == 'f':
                # Print the whole stack
                print str(val_stack)            
            elif curr_cmd == '+':
                # Add the top two numbers in the stack and push the result
                val_stack.append(val_stack.pop() + val_stack.pop())               
            elif curr_cmd == '-':
                #Subtract the second number in the stack from the top number in the stack and push the result
                val_stack.append(val_stack.pop() - val_stack.pop())            
            elif curr_cmd == '*':
                # Multiply the top two numbers in the stack and push the result
                val_stack.append(val_stack.pop() * val_stack.pop())          
            elif curr_cmd == '/':
                # Divide the top two numbers in the stack and push the result
                val_stack.append(val_stack.pop() / val_stack.pop())             
            else:
                # Program should never get here, as error cases are handled in push_value
                sys.stderr.write("Unexpected error")
                val_stack = val_stack_old[:]
                cmd_stack = cmd_stack_old[:]
                return False
        
        # Save the current state of the stack
        val_stack_old = val_stack[:] 
        cmd_stack_old = cmd_stack[:]                  
        return True
    
    def parse_input(self, input):
        # Turns a string input from the test program into a list of commands
        user_input = input.split("|")
        
        for i in range(len(user_input)):
            user_input[i] = user_input[i].split()
            user_input[i].reverse()
           
        return user_input
    
    def runDC(self, input):    
        run = True
        error = False 
        
        if input == '':
            # No arguments = input taken from stdin
            print "Welcome to minidc."
            
            while run:  
                error = False                     
                # Get the user's input and split it up into a list of arguments (delimiter is whitespace)
                sys.stdout.write('>>')
                user_input = raw_input().split()
                user_input.reverse()
                
                # Add the input values to the stack
                for element in user_input:
                    if not error:
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
                # Add the individual values to the stack
                for element in command:
                    if not error:
                        error = self.push_value(element)          
                
                # Reverse the input command for display in the console, then change it back before handling the command
#                command.reverse()
#                print ">> %s" % str( ' '.join(command) )
#                command.reverse()
                self.handle_input() 
#                print "Actual: %s\n" % str(val_stack) ###DEBUG###        
            return val_stack #returns the full stack once operation is done
        
    def clear_stack(self):   
        global val_stack
        global val_stack_old
        global cmd_stack
        global cmd_stack_old     
        val_stack = []
        val_stack_old = []
        cmd_stack = []
        cmd_stack_old = []
    
valid_commands = ['p', 'n', 'f', '+', '-', '*', '/', 'exit']
val_stack = []
val_stack_old = []
cmd_stack = []
cmd_stack_old = []

if __name__ == "__main__":
    mdc = minidc()
    if len(sys.argv) == 2:
        mdc.runDC(sys.argv[1]) # Run from test program
    elif len(sys.argv) == 1:
        mdc.runDC('')          # Run from user input
    else:
        print "Unexpected error. Check your arguments"