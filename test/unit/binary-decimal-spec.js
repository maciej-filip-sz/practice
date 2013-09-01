'use strict';

describe('binary-decimal', function() {
  var binOut = {},
      decOut = {},
      bindecker = new BinDecker(binOut, decOut);

  beforeEach(function () {
    binOut.value = null;
    decOut.value = null;
  });

  it('produces the binary representation of a decimal value', function () {
    var cases = [
      0, 1, 2, 12, 345, 6789,
    ];
    cases.forEach(function (given) {
      expect(bindecker.decimalToBinary(given)).
        toEqual(parseInt(given).toString(2));
    });
  });

  it('produces the decimal representation of binary values', function () {
    var cases = [
      0, 1, 10, 1100, 10001, 100011, 11001100, 101011001, 1101010000101,
    ];
    cases.forEach(function (given) {
      expect(bindecker.binaryToDecimal(given)).
        toEqual(parseInt(given, 2).toString());
    });
  });

  it('produces empty string if it isnt Numberish', function () {
    // dontShowNaN is (String -> String)
    var not_numberish = [
      'NaN', "Number Six", 'eleven',
    ],  numberish = [
      '0', '1', '2', '10', '12', '345', '6789', '3.1415926',
      '1100', '10001', '100011', '11001100', '101011001', '1101010000101',
      '1', '2', '3', '2.71828', '31337',
    ];
    not_numberish.forEach(function (given) {
      expect(bindecker.dontShowNaN(given)).toEqual('');
    });
    numberish.forEach(function (given) {
      expect(bindecker.dontShowNaN(given)).toEqual(given);
    });
  });

  it('updates binary output value', function () {
    var cases = [
      '0', '1', '2', '12', '345', '6789',
    ];
    cases.forEach(function (given) {
      bindecker.updateBinary({target: {value: given}})
      expect(binOut.value).toEqual(bindecker.decimalToBinary(given));
    });
  });
  it('updates decimal output value', function () {
    var cases = [
      '0', '1', '10', '1100', '10001', '100011', '11001100', '101011001', 
      '1101010000101',
    ];
    cases.forEach(function (given) {
      bindecker.updateDecimal({target: {value: given}})
      expect(decOut.value).toEqual(bindecker.binaryToDecimal(given));
    });
  });
});
