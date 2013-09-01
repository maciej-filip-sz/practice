#! /usr/bin/python2

from splinter import Browser


class Test_ReverseString(object):
    url = 'http://localhost:8000/app/reverse-string.html'

    @classmethod
    def setup_class(cls):
        # phantomjs is buggy, claims connection refused
        # chrome is ~twice faster than firefox
        cls.b = Browser('chrome')
        cls.b.visit(cls.url)

    @classmethod
    def teardown_class(cls):
        cls.b.driver.close()
        del cls.b


    def set_input(self, text):
        self.b.fill('in', text)

    def get_output(self):
        return self.b.find_by_id('out')[0].value

    def reverse(self, s):
        return u''.join(reversed(list(s)))


    def test_WordOfRepeatedCharsProducesItself(self):
        givens = u'a bb ccc dddd eeeee ffffff ggggggg'.split()
        for given in givens:
            self.set_input(given)
            assert self.get_output() == given

    def test_WordOfDifferentCharsProducesReversedWord(self):
        givens = "z yx wvu tsrq ponml kjihgf edcba?!".split()
        for g in givens:
            self.set_input(g)
            assert self.get_output() == self.reverse(g)

    def test_PhrasesProduceReversedCharacters(self):
        givens = [
            'Set adrift on memory bliss...',
            'This is a journey into sound.',
            "It's gonna be a lovely day."
        ]
        for g in givens:
            self.set_input(g)
            assert self.get_output() == self.reverse(g)
