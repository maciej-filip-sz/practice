var BinDecker,
  __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

BinDecker = (function() {
  'use strict';
  function BinDecker(binaryInput, decimalInput) {
    this.binaryInput = binaryInput;
    this.decimalInput = decimalInput;
    this.updateBinary = __bind(this.updateBinary, this);
    this.updateDecimal = __bind(this.updateDecimal, this);
  }

  BinDecker.prototype.decimalToBinary = function(decStr) {
    // String -> String
    // Convert the given decimal number string to a binary number string.
    return parseInt(decStr, 10).toString(2);
  };

  BinDecker.prototype.binaryToDecimal = function(binStr) {
    // String -> Integer | NaN
    // Convert the given binary number string to a decimal number string.
    return parseInt(binStr, 2).toString(10);
  };

  BinDecker.prototype.dontShowNaN = function(str) {
    // String -> String
    // Produce the given string if it is a representation of a number, 
    // or an empty string otherwise.
    return isNaN(str) ? '' : str;
  };

  BinDecker.prototype.updateBinary = function(evt) {
    // Event -> ()
    // Set the binary input element value to the event target value converted
    // from decimal to binary.
    this.binaryInput.value = this.dontShowNaN(
      this.decimalToBinary(evt.target.value)
    );
  };

  BinDecker.prototype.updateDecimal = function(evt) {
    // Event -> ()
    // Set the decimal input element value to the event target value converted
    // from binary to decimal.
    this.decimalInput.value = this.dontShowNaN(
      this.binaryToDecimal(evt.target.value)
    );
  };

  return BinDecker;
})();


function setupProject() {
  'use strict';

  // () -> ()
  // Adds listeners to both input fields. Each field updates the other
  // with a converted version of its value.
  // Called by body on load.
  var binary = document.getElementById('binary'),
      decimal = document.getElementById('decimal'),
      bindecker = new BinDecker(binary, decimal);

  common.addInputChangeListeners(binary, bindecker.updateDecimal);
  common.addInputChangeListeners(decimal, bindecker.updateBinary);
}

