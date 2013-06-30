#test_realistic.py
from nose.tools import *
class TestCase:
    def setUp(self):
        pass # Do setup stuff here.

    def tearDown(self):
        pass # Do teardown stuff here.

    def test_always_passes(self):
        '''test_always_passes'''
        assert True,"I should have passed"  #will always be True, so test will always pass.

    def test_always_fails(self):
        '''test_always_passes'''
        assert False,"I failed"
