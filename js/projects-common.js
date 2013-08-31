var common = {
  addInputChangeListeners: function (inputSource, listener) {
    'use strict';
    // InputElem (Event -> Any) -> ()
    // Add listener to change events of the given input element.
    var events = [
      'change',
      'keypress',
      'input',
      'paste'
    ];
    events.forEach(function (evt) {
      inputSource.addEventListener(evt, listener);
    });
  }
};