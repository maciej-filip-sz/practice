#! /usr/bin/python2

from splinter import Browser


class Test_BinaryDecimal(object):
    url = 'http://localhost:8000/app/binary-decimal.html'

    @classmethod
    def setup_class(cls):
        # chrome returns incorrect value of input field
        cls.b = Browser('chrome')
        cls.b.visit(cls.url)

    @classmethod
    def teardown_class(cls):
        cls.b.driver.close()
        del cls.b


    def set_binary(self, text):
        self.b.fill('binary', text)
    def set_decimal(self, text):
        self.b.fill('decimal', text)

    def get_binary(self):
        return self.b.find_by_id('binary')[0].value
    def get_decimal(self):
        return self.b.find_by_id('decimal')[0].value


    def test_FillingDecimalChangesBinary(self):
        prev_binary = self.get_binary()
        self.set_decimal(100)
        assert self.get_binary() != prev_binary
    def test_FillingBinaryChangesDecimal(self):
        prev_decimal = self.get_decimal()
        self.set_binary(100)
        assert self.get_decimal() != prev_decimal

    def test_ClearingDecimalClearsBinary(self):
        self.set_binary(100)
        self.set_decimal('')
        assert self.get_binary() == ''
    def test_ClearingBinaryClearsDecimal(self):
        self.set_decimal(999)
        self.set_binary('')
        assert self.get_decimal() == ''

    def test_FillingDecimalFillsBinaryWithEqualValue(self):
        cases = (
            (0, '0'),
            (1, '1'),
            (2, '10'),
            (12, '1100'),
            (345, '101011001'),
            (6789, '1101010000101'),
        )
        for given, expected in cases:
            self.set_decimal(given)
            assert self.get_binary() == expected
    def test_FillingBinaryFillsDecimalWithEqualValue(self):
        cases = (
            (0, '0'),
            (1, '1'),
            (10, '2'),
            (1100, '12'),
            (101011001, '345'),
            (1101010000101, '6789'),
            (10001, '17'),
            (100011, '35'),
            (11001100, '204'),
        )
        for given, expected in cases:
            self.set_binary(given)
            assert self.get_decimal() == expected