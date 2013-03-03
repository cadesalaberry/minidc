
import sys

sys.path.append("./lib/pyunit-1.4.1/")

from widget import Widget

import unittest

class MiniDCTestCase(unittest.TestCase):
	
	def testLogic():

		print "Testing correctness of Logic:"
		for i in range(100):
			for j in range(100):
				assert minidc([i,j,'+']) == i + j, 'Logic:addition test did not pass.'
				assert minidc([i,j,'-']) == i - j, 'Logic:subtraction test did not pass.'
				assert minidc([i,j,'*']) == i * j, 'Logic:multiplication test did not pass.'
				assert minidc([i,j,'/']) == i / j, 'Logic:division test did not pass.'

		#The program should refuse numbers if they are too big
		assert minidc([-sys.maxint - 1,1,'+']) == 'Out of Bound.', 'Logic:minimum test did not pass'
		assert minidc([sys.maxint + 1,1,'-']) == 'Out of Bound.', 'Logic:maximum test did not pass'

	def testSyntax():

		#Ideally, there should exist a checkSyntax([]) method returning false on error
		print "Testing correctness of Syntax:"

		assert checkSyntax([1,2,'+']), 'Syntax:reverse-polish test did not pass'
		assert False == checkSyntax([3,'+',4]), 'Syntax:infix test did not pass'
		assert False == checkSyntax(['+',3,5]), 'Syntax:polish test did not pass'

		assert False == checkSyntax([1,3,4]), 'Syntax:numbers-only test did not pass'
		assert False == checkSyntax(['-','/','*']), 'Syntax:operations-only test did not pass'


		#Checks the different types of valid syntax
		assert checkSyntax([1,3,'+',2,'-']), 'Syntax:lefty-operation test did not pass'
		assert checkSyntax([1,3,2,'-','+']), 'Syntax:righty-operation test did not pass'
		assert checkSyntax([1,3,'+',2,4,'-','*']), 'Syntax:pyramid-operation test did not pass'


	def testParameters():

		print "Testing implementation of Parameters:"
		assert minidc([]) == 'Wrong usage. Please refer to README file for available commands.', 'Parameters:no-input test did not pass'

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
	#unittest.main(defaultTest="MiniDCTestCase:testCheckLogic")
	unittest.main()