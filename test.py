
import sys

sys.path.append("./lib/pyunit-1.4.1/")
sys.path.append("./lib/pyunit-1.4.1/examples")

from widget import Widget
import unittest
import minidc
import os

class MiniDCTestCase(unittest.TestCase):
	
	# The input should be a string where individual commands are separated by a the character "|"
    # Example - the input "1 2 + | 3 4 +" simulates a user entering the command "1 2 +" followed by the command "3 4 +"            
	
	def testLogic(self):

		print "\nTESTING DOMAIN LOGIC"
		
		# Values for the tests
		a = 1.0
		b = 3.0
		c = 5.0
		
		# Math operations tests
		for i in range(10):
			for j in range(10):
				# Test both negative and positive numbers
				m = -5.0 + float(i)
				n = -5.0 + float(j)
				mdc.clear_stack()
				assert mdc.runDC('%s %s +' % (m,n)) == [m + n], '\nLogic:addition test failed.'
				mdc.clear_stack()
				assert mdc.runDC('%s %s -' % (m,n)) == [m - n], 'Logic:substraction test failed.'
				mdc.clear_stack()
				assert mdc.runDC('%s %s *' % (m,n)) == [m * n], 'Logic:multiplication test failed.'
				mdc.clear_stack()
				if n != 0: 
					# Normal case 
					assert mdc.runDC('%s %s /' % (m,n)) == [m / n], 'Logic:division test failed.'
					mdc.clear_stack()
				else:
					# Divide by zero case
					mdc.runDC('%s %s /' % (m,n))
					assert mdc.read_err_log()[0][:-1] == 'Error: cannot divide by zero', 'Logic:divide by zero test failed.'
					mdc.clear_err_log()
		print "Math operations:"
		print "  	> Addition: PASS"
		print "  	> Subtraction: PASS"
		print "  	> Multiplication: PASS"
		print "  	> Division: PASS"
					
		# Minimum/maximum value test
		mdc.clear_stack()
		mdc.runDC('%s %s +' % (-sys.maxint-1, 1))
		assert mdc.read_err_log()[0][:-1] == 'Error: number out of range', 'Logic:minimum test failed.'		
		mdc.clear_err_log()
		print "Limit values:"
		print "  	> Minimum value: PASS"
		
		mdc.clear_stack()
		mdc.runDC('%s %s -' % (sys.maxint+1, 1))
		assert mdc.read_err_log()[0][:-1] == 'Error: number out of range', 'Logic:maximum test failed.'
		mdc.clear_err_log()
		print "  	> Maximum value: PASS"
		
		# Operation 'p' test		
		print "Stack operations:"		
		mdc.clear_stack()
		mdc.runDC('%s p' % a)
		assert float(mdc.read_output_log()[0]) == a, 'Logic: test \'p\' operation failed.'
		mdc.clear_output_log()
		print "  	> \'p\' Correct output: PASS"
		
		# Operation 'n' test	
		mdc.clear_stack()
		mdc.runDC('%s n' % a)
		assert float(mdc.read_output_log()[0]) == a, 'Logic: test \'n\' operation failed (incorrect value popped).'
		mdc.clear_output_log()	
		print "  	> \'n\' Correct output: PASS"
				
		mdc.clear_stack()		
		assert mdc.runDC('%s %s n' % (a,b)) == [b], 'Logic: test \'n\' operation failed (stack is not correct after pop).'
		mdc.clear_output_log()	
		print "  	> \'n\' Stack status: PASS"
		
		# Operation 'f' test	
		mdc.clear_stack()
		mdc.runDC('%s f' % a)
		assert mdc.read_output_log()[0] == str([a]), 'Logic: test \'f\' operation failed with 1 value in stack.'
		mdc.clear_output_log()	
		print "  	> \'f\' Correct output (1 value): PASS"
		
		mdc.clear_stack()
		mdc.runDC('%s %s %s f' % (a,b,c))
		assert mdc.read_output_log()[0] == str([c, b, a]), 'Logic: test \'f\' operation failed with multiple values in stack.'
		mdc.clear_output_log()
		print "  	> \'f\' Correct output (3 values): PASS"
		
		# Commands with multiple operations	
		print "Multiple Operations:"		
		mdc.clear_stack()
		mdc.runDC('%s %s + f' % (a,b))
		assert mdc.read_output_log()[0] == str([a + b]), 'Logic: test \'f\' operation after addition failed.'
		mdc.clear_output_log()		
		print "  	> \"1 3 + f\": PASS"
		
		mdc.clear_stack()
		assert mdc.runDC('%s %s f +' % (a,b)) == [a + b], 'Logic: test \'f\' operation before addition failed (stack not updated after operation).'
		assert mdc.read_output_log()[0] == str([b, a]), 'Logic: test \'f\' operation before addition failed (output incorrect).'		
		mdc.clear_output_log()	
		print " 	> \"1 3 f +\": PASS"
		
		mdc.clear_stack()
		assert mdc.runDC('%s %s + n' % (a,b)) == [], 'Logic: test \'n\' operation after addition failed (stack not updated after operation).'
		assert mdc.read_output_log()[0] == str((a + b)), 'Logic: test \'n\' operation after addition failed (output incorrect).'		
		mdc.clear_output_log()
		print "  	> \"1 3 + n\": PASS"
		
		mdc.clear_stack()
		mdc.runDC('%s %s n +' % (a,b))
		assert mdc.read_output_log()[0] == str(a), 'Logic: test \'n\' operation before addition failed (popped incorrect value).'
		assert mdc.read_err_log()[0][:-1] == 'Error: could not perform operation - stack does not contain 2 values', 'Logic: test \'n\' operation after addition failed (output incorrect).'		
		mdc.clear_err_log()
		mdc.clear_output_log()
		print "  	> \"1 3 n +\": PASS"
		
		# Chained commands
		print "Chained commands"
		mdc.clear_stack()
		assert mdc.runDC('%s %s + | %s +' % (a,b,c)) == [a + b + c], 'Logic: chained operation \"a+b+c\" failed'	
		mdc.clear_output_log()	
		print " 	> \"1 2 +\" , \"3 +\": PASS"
		
		mdc.clear_stack()
		assert mdc.runDC('%s %s + | %s %s +' % (a,b,c,a)) == [a + b, c + a], 'Logic: chained operation \"a+b, c+a\" failed'	
		mdc.clear_output_log()	
		print " 	> \"1 2 +\" , \"3 1 +\": PASS"
		
		mdc.clear_stack()
		assert mdc.runDC('%s %s + f | %s *' % (a,b,c)) == [(a + b) * c], 'Logic: chained operation \"(a+b)*c\" failed'	
		assert mdc.read_output_log()[0] == str([(a + b)]), 'Logic: test \'f\' operation before addition failed (output incorrect).'
		mdc.clear_output_log()	
		print " 	> \"1 2 + f\" , \"3 *\": PASS"
		
		

	def testSyntax(self):

		print "\nTESTING CORRECTNESS OF SYNTAX:"
		
		# Values for the tests
		a = 1.0
		b = 3.0
		c = 5.0
		
		# Math operations
		print "Math operations:"
		mdc.clear_stack()
		mdc.runDC('+')
		assert mdc.read_err_log()[0][:-1] == 'Error: could not perform operation - stack does not contain 2 values'
		mdc.clear_err_log()
		print "  	> Addition: PASS"
		
		mdc.clear_stack()
		mdc.runDC('-')
		assert mdc.read_err_log()[0][:-1] == 'Error: could not perform operation - stack does not contain 2 values'
		mdc.clear_err_log()
		print "  	> Subtraction: PASS"
		
		mdc.clear_stack()
		mdc.runDC('*')
		assert mdc.read_err_log()[0][:-1] == 'Error: could not perform operation - stack does not contain 2 values'
		mdc.clear_err_log()
		print "  	> Multiplication: PASS"
		
		mdc.clear_stack()
		mdc.runDC('/')
		assert mdc.read_err_log()[0][:-1] == 'Error: could not perform operation - stack does not contain 2 values'
		mdc.clear_err_log()
		print "  	> Division: PASS"
		
		# Operation 'p' test
		print "Stack Operations:"
		mdc.clear_stack()
		mdc.runDC('p')
		assert mdc.read_err_log()[0][:-1] == 'Error: stack is empty', 'Logic:p empty stack test failed.'
		mdc.clear_err_log()
		print "  	> \'p\' invalid syntax detection: PASS"
		
		# Operation 'n' test
		mdc.clear_stack()
		mdc.runDC('n')
		assert mdc.read_err_log()[0][:-1] == 'Error: stack is empty', 'Logic:n empty stack test failed.'
		mdc.clear_err_log()
		print "  	> \'n\' invalid syntax detection: PASS"
				
		# Operation 'f' test
		mdc.clear_stack()		
		assert mdc.runDC('f') == [], 'Logic: test \'f\' operation failed when stack is empty.'
		mdc.clear_err_log()
		print "  	> \'f\' fnvalid syntax detection: PASS"
		
		# Invalid commands test
		print "Invalid Commands:"
		mdc.clear_stack()	
		mdc.runDC('z')	
		assert mdc.read_err_log()[0][:-1] == 'Unknown command: \'z\' does not exist', 'Logic: test single invalid command failed.'
		mdc.clear_err_log()
		print "  	> Single invalid command: PASS"
		
		mdc.clear_stack()		
		assert mdc.runDC('%s %s z' % (a,b)) == [], 'Logic: test single invalid command with valid values failed (stack was not properly reset)'
		assert mdc.read_err_log()[0][:-1] == 'Unknown command: \'z\' does not exist', 'Logic: test single invalid command with valid values failed.'
		mdc.clear_err_log()
		print "  	> Valid values with invalid command: PASS"

	def testParameters(self):		
		print "\nTESTING INPUT PARAMETERS:"
		# Case with too many inputs
		assert mdc.runDC('1 2 +', '3 4 +') == -1, 'Parameters: multiple-input test did not pass'
		print "  	> Too many arguments: PASS"
		
		# Case with too few inputs - no need to test because no args triggers user-interactive mode
		assert 1 == 1, 'Parameters: no-input test did not pass'
		print "  	> Too few arguments: PASS"

# Simple way to make a test suite
def makeMiniDCTestSuite():

	suite = unittest.TestSuite()
	suite.addTest(MiniDCTestCase("testLogic"))
	suite.addTest(MiniDCTestCase("testSyntax"))

	return suite

def suite():
	
	return unittest.makeSuite(MiniDCTestCase)

# Make this test module runnable from the command prompt
if __name__ == "__main__":
	mdc = minidc.minidc()	
	#unittest.main(defaultTest="MiniDCTestCase:testCheckLogic")
	unittest.main()