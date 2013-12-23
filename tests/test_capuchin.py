import unittest
from capuchin.capuchin import capuchin, imprinter

class TestCapuchin():

    def setUp(self):
        self.test_imprinter = imprinter.Imprinter()
        self.test_capuchin = capuchin.Capuchin()

    def test_capuchin_exists(self):
        assert self.test_capuchin != None

    def test_capuchin_imprinter(self):
        assert self.test_capuchin.imprinter.imprint() != None

    def test_capuchin_run(self):
        assert self.test_capuchin.run() != None


