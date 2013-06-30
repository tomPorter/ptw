#test_realistic.py
from nose.tools import *
import count.count as c
class TestCase:
    def setUp(self):
        pass # Do setup stuff here.

    def tearDown(self):
        pass # Do teardown stuff here.

    def test_one_elephant(self):
        '''Get one elephant back when I count to 1.'''
        assert '1 Elephant' in c.count_to(1)

