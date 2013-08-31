var WordCounter, 
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

WordCounter = (function () {
  'use strict';

  function WordCounter(targetElem, hideSElem) {
    this.targetElem = targetElem;
    this.hideSElem = hideSElem;
    this.showCount = __bind(this.showCount, this);
    this.isWord = __bind(this.isWord, this);
  }


  WordCounter.prototype.isWord = function(text) {
    // String -> Boolean
    // Produce true if given text starts with a letter or quote mark, false otherwise.
    return /^['"]?[a-zA-Z]+/.test(text);
  };

  WordCounter.prototype.countWords = function(text) {
    // String -> Integer
    // Produce the number of words in the given text.
    var words = text.split(/[\.\s\(\)]/).
                       filter(this.isWord);
    return words.length;
  };

  WordCounter.prototype.showCount = function(evt) {
    // Event -> ()
    // Sets the innerHTML of the target element to the word count 
    // of the value of the target of the event.
    var count = this.countWords(evt.target.value);
    this.targetElem.innerHTML = count;
    this.hideSElem.hidden = (count == 1) ? true : false;
  };

  return WordCounter;
}());


function setupProject() {
  'use strict';
  // () -> ()
  // Adds listeners that process value of the 'in' element 
  // and output to the 'out' element.
  // Called by body on load.
  var wordCounter,
      inputSource = document.getElementById('in'),
      targetElem = document.getElementById('out'),
      hideSElem = document.getElementById('hide-s');
  wordCounter = new WordCounter(targetElem, hideSElem);
  common.addInputChangeListeners(inputSource, wordCounter.showCount);
}
