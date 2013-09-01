describe('word-count', function() {
  'use strict';

  var countOut = {},
      hideSElem = {},
      wordCounter = new WordCounter(countOut, hideSElem);

  beforeEach(function () {
    countOut.innerHTML = null;
    hideSElem.hidden = null;
  });

  it('puts word count in the innerHTML of the given element', function () {
    var cases = [
      "1 + 1 = 2",
      "$20 with tax",
      "Check out my new weapon, weapon of choice.",
    ];
    cases.forEach(function (text) {
      wordCounter.showCount({target: {value: text}});
      expect(countOut.innerHTML).
        toEqual(wordCounter.countWords(text));
    });
  });

  it('counts words in a string', function () {
    var text,
        cases = [
          ['yeti'],
          ['YETTI', 'SLOTH'],
          ["'ere's", "yeti's", "'erywhere!"],
          ['zebra?', 'otter...', 'cat!'],
          ['a4rdv4rk', 'd01phin', 'l0bster', 'g0000al'],
          ['yet-ti', 'OT_TER', 'sloth$']
        ];
    cases.forEach(function (wl) {
      text = wl.join(' ');
      expect(wordCounter.countWords(text)).toEqual(wl.length);
    });
  });

  it("doesn't count non-words", function () {
    var text,
        cases = [
          [' ', '\n', '\t'],
          ['"', ',', '.', '?'],
          ['999', '+', '1', '=', '1000'],
          ['_under', '-dash', '99redballoons', '*star', '^hat', '&amp', '%cent',
           '$dollar', '@monkey', '!bang'],
        ];
    cases.forEach(function (wl) {
      text = wl.join(' ');
      expect(wordCounter.countWords(text)).toEqual(0);
    });
  });

  it("counts words in texts containing non-words", function () {
    expect(wordCounter.countWords("bat @ hand is == 2 @ bush")).
      toEqual(4);
    expect(wordCounter.countWords("_important!_ do *not* feed the /gremlin/")).
      toEqual(3);
  });

  it('treats anything starting with a letter as a word', function () {
    var cases = [
      'at', 'Bat', 'cBwb', 'DUDER',
      'm3h', 'j007', 'bad-man', 'p_body'
    ];
    cases.forEach(function (text) {
      expect(wordCounter.isWord(text)).toEqual(true);
    });
  });

  it('treats anything starting with non-letter as a non-word', function () {
    var cases = [
      '~at', '!Bat', '@cBwb', '#DUDER',
      '$m3h', '%j007', '^bad-man', '9p_body'
    ];
    cases.forEach(function (text) {
      expect(wordCounter.isWord(text)).toEqual(false);
    });
  }); 

  it("hides the 's' in 'words' when there's a single word", function () {
    var cases = [
      'yeti',
      'yeti <3 $$$'
    ];
    cases.forEach(function (text) {
      wordCounter.showCount({target: {value: text}});
      expect(hideSElem.hidden).toEqual(true);
    });
  });

  it("shows the 's' in 'words' when there's zero or multiple words", function () {
    var cases = [
      '',
      "1 + 1 = 2",
      'yeti sloth',
      'yeti <3 sloth'
    ];
    cases.forEach(function (text) {
      wordCounter.showCount({target: {value: text}});
      expect(hideSElem.hidden).toEqual(false);
    });
  });
});