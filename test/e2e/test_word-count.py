#! /usr/bin/python2

from splinter import Browser


class Test_WordCount(object):
    url = 'http://localhost:8000/app/word-count.html'

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
        return self.b.find_by_id('out')[0].html


    def test_EmptyInputShowsZeroCount(self):
        self.set_input('')
        assert self.get_output() == '0'

    def test_NonWordInputShowsZeroCount(self):
        cases = [
          ' ', '\n', '\t',
          '"', ',', '.', '?',
          '999', '+', '1', '=', '1000',
          '_under', '-dash', '99redballoons', '*star', '^hat', '&amp', '%cent',
           '$dollar', '@monkey', '!bang',
        ]
        for non_word in cases:
            self.set_input(non_word)
            assert self.get_output() == '0'

    def test_ShowsNumberOfWords(self):
        cases = [
          ['yeti'],
          ['YETTI', 'SLOTH'],
          ["'ere's", "yeti's", "'erywhere!"],
          ['zebra?', 'otter...', 'cat!'],
          ['a4rdv4rk', 'd01phin', 'l0bster', 'g0000al'],
          ['yet-ti', 'OT_TER', 'sloth$']
        ]
        for word_list in cases:
            self.set_input(' '.join(word_list))
            assert self.get_output() == str(len(word_list))

    def test_CountsWordsInMultilineText(self):
        self.set_input("""
            One, two,
            three,

            four,
            five!
        """)
        assert self.get_output() == '5'

    def test_CountsWordsMixedWithNonWords(self):
        cases = [
            ("bat @ hand is == 2 @ bush", '4'),
            ("_important!_ do *not* feed the /gremlin/", '3'),
        ]
        for given, expected in cases:
            self.set_input(given)
            assert self.get_output() == expected

    def test_InfoTextUsesPluralForZeroAndMultipleWords(self):
        cases = [
            '',
            "1 + 1 = 2",
            'yeti sloth',
            'yeti <3 sloth'
        ]
        for words in cases:
            self.set_input(words)
            assert self.b.find_by_id('info-text')[0].text.endswith('words.')


    def test_InfoTextUsesSingularForSingleWord(self):
        cases = [
            'yeti',
            'yeti <3 $$$'
        ]
        for words in cases:
            self.set_input(words)
            assert self.b.find_by_id('info-text')[0].text.endswith('word.')