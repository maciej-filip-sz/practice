var Reverser,
  __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

Reverser = (function() {
  'use strict';

  function Reverser(reversedInput) {
    this.reversedInput = reversedInput;
    this.updateReversed = __bind(this.updateReversed, this);
  }

  Reverser.prototype.reverse = function(someString) {
    // String -> String
    // Produce a string of characters from the given string ordered
    // from last to first
    var reversed = "";
    for (var i = someString.length - 1; i >= 0; i--) {
        reversed += someString[i];
    };
    return reversed;
  };

  Reverser.prototype.updateReversed = function(evt) {
    // Event -> ()
    // Set the value of the target input element to the reversed value of the 
    // event target.
    return this.reversedInput.value = this.reverse(evt.target.value);
  };

  return Reverser;
})();


function setupProject() {
  'use strict';
  // () -> ()
  // Adds listeners to both input fields. Each field updates the other
  // with a reversed version of its value.
  // Called by body on load.
  var source = document.getElementById('in'),
      target = document.getElementById('out'),
      reverser = new Reverser(target),
      unreverser = new Reverser(source);
  
  common.addInputChangeListeners(source, reverser.updateReversed);
  common.addInputChangeListeners(target, unreverser.updateReversed);
}

