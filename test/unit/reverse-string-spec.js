'use strict';

describe('reverse-string', function() {
  var reverser = new Reverser();

  it('produces an empty string when given an empty string', function() {
    expect(reverser.reverse('')).toEqual('');
  });

  it('produces the same string when given a single character string', function() {
    expect(reverser.reverse('a')).toEqual('a');
  });

  it('produces a string with characters of the given string from last to first', function() {
    expect(reverser.reverse('ab')).toEqual('ba');
    expect(reverser.reverse('abc')).toEqual('cba');
    expect(reverser.reverse('abba')).toEqual('abba');
    expect(reverser.reverse('That is an adorable sloth!')).
                 toEqual('!htols elbaroda na si tahT');
  });
});
