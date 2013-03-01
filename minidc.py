'''
minidc.py
Created on 2013-02-23
@author: J. Berthiaume
'''

import sys

# Pushes a value onto the appropriate stack. Returns True if there is an error, False otherwise
def push_value(val):
    
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
            
    
def handle_input():
    
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

valid_commands = ['p', 'n', 'f', '+', '-', '*', '/', 'exit']
val_stack = []
val_stack_old = []
cmd_stack = []
cmd_stack_old = []
run = True

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
            error = push_value(element)          
    
    run = handle_input()
         
        
            
            
        
    
    
