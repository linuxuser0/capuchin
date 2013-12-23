import unittest
from capuchin.capuchin import capuchin

class TestCapuchin():

    def setUp(self):
        self.test_capuchin = capuchin.Capuchin() 

    def test_capuchin_exists(self):
        assert self.test_capuchin != None
