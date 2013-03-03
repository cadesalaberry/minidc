
import sys

sys.path.append("./lib/pyunit-1.4.1/")
sys.path.append("./lib/pyunit-1.4.1/examples")

from widget import Widget
import unittest
import minidc

class MiniDCTestCase(unittest.TestCase):
	
	# The input should be a string where individual commands are separated by a the character "|"
    # Example - the input "1 2 + | 3 4 +" simulates a user entering the command "1 2 +" followed by the command "3 4 +"            
	
	def testLogic(self):

		print "Testing correctness of Logic:"
		for i in range(100):
			for j in range(100):
				# Tempfix to preserve accuracy of non-integer numbers
				m = float(i)
				n = float(j)
				mdc.clear_stack()
				assert mdc.runDC('%s %s +' % (m,n)) == [m + n], '\nLogic:addition test did not pass.'
				mdc.clear_stack()
				assert mdc.runDC('%s %s -' % (m,n)) == [m - n], 'Logic:substraction test did not pass.'
				mdc.clear_stack()
				assert mdc.runDC('%s %s *' % (m,n)) == [m * n], 'Logic:multiplication test did not pass.'
				mdc.clear_stack()
				if j != 0: # Prevent divide by zero errors
#					print "Expected: %s " % [m / n] ###DEBUG###
					assert mdc.runDC('%s %s /' % (m,n)) == [m / n], 'Logic:division test did not pass.'
					mdc.clear_stack()

	def testSyntax(self):
		#############################################################################
		# TODO: change all of these from arrays to strings							#
		#############################################################################

		#Ideally, there should exist a checkSyntax([]) method returning false on error
		print "Testing correctness of Syntax:"

		assert True == checkSyntax([1,2,'+']), 'Syntax:reverse-polish test did not pass'
		assert False == checkSyntax([3,'+',4]), 'Syntax:infix test did not pass'
		assert False == checkSyntax(['+',3,5]), 'Syntax:polish test did not pass'

		assert False == checkSyntax([1,3,4]), 'Syntax:numbers-only test did not pass'
		assert False == checkSyntax(['-','/','*']), 'Syntax:operations-only test did not pass'


		#Checks the different types of valid syntax
		assert True == checkSyntax([1,3,'+',2,'-']), 'Syntax:lefty-operation test did not pass'
		assert True == checkSyntax([1,3,2,'-','+']), 'Syntax:righty-operation test did not pass'
		assert True == checkSyntax([1,3,'+',2,4,'-','*']), 'Syntax:pyramid-operation test did not pass'


	def testParameters(self):
		print ''

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