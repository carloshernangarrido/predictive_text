// --- Autocomplete para Título --- //
$( function() {
  var availableTags = [
    "hola",
    "cómo",
    "estás",
  ];
  function split( val ) {
    // return val.split( /,\s*/ );
    return val.split(" ");
  }
  function extractLast( term ) {
    return split( term ).pop();
  }

  $( "#tags" )
    // don't navigate away from the field on tab when selecting an item
    .on( "keydown", function( event ) {
      if ( event.keyCode === $.ui.keyCode.TAB &&
          $( this ).autocomplete( "instance" ).menu.active ) {
        event.preventDefault();
      }
    })
    .autocomplete({
      minLength: 0,
      source: function( request, response ) {
        // delegate back to autocomplete, but extract the last term
        response( $.ui.autocomplete.filter(
          availableTags, extractLast( request.term ) ) );
      },
      focus: function( event, ui ) {
        var terms = split( this.value );
        // remove the current input
        terms.pop();
        // add the selected item
        terms.push( ui.item.value );
        // add placeholder to get the space at the end
        // terms.push("");
        this.value = terms.join(" ");
        return false;
      },
      select: function( event, ui ) {
        return false;
      }
    });
} );



// --- Autocomplete para Firma --- //
$( function() {
  var availableTags = [
    "Hernán",
    "Garrido",
    "Andrea",
    "Comerci"
  ];
  function split( val ) {
    // return val.split( /,\s*/ );
    return val.split(" ");
  }
  function extractLast( term ) {
    return split( term ).pop();
  }

  $( "#tags_firma" )
    // don't navigate away from the field on tab when selecting an item
    .on( "keydown", function( event ) {
      if ( event.keyCode === $.ui.keyCode.TAB &&
          $( this ).autocomplete( "instance" ).menu.active ) {
        event.preventDefault();
      }
    })
    .autocomplete({
      minLength: 0,
      source: function( request, response ) {
        // delegate back to autocomplete, but extract the last term
        response( $.ui.autocomplete.filter(
          availableTags, extractLast( request.term ) ) );
      },
      focus: function( event, ui ) {
        var terms = split( this.value );
        // remove the current input
        terms.pop();
        // add the selected item
        terms.push( ui.item.value );
        // add placeholder to get the space at the end
        // terms.push("");
        this.value = terms.join(" ");
        return false;
      },
      select: function( event, ui ) {
        return false;
      }
    });
} );



// --- Autocomplete para Contenido --- //
// setings
const n_preds = 1000;
const n_best_preds = 5;

// Load the model
const model = await tf.loadLayersModel('./models/nextword1_libro_blanco_min4.h5/model.json');

// Load the tokenizer
var word2index_json = './models/nextword1_libro_blanco_min4.h5/tokenizer_word2index.json'
var index2word_json = './models/nextword1_libro_blanco_min4.h5/tokenizer_index2word.json'
async function loadTokenizer(vocabPath) {
  const response = await fetch(vocabPath);
  const data = await response.json();
  return(data); 
}
const word2index = await loadTokenizer(word2index_json);
const index2word = await loadTokenizer(index2word_json);
const ngram_size = model.input.shape[1];

// Autocompleter
$( function() {
  var availableTags = ['Estudio'];
  function split( val ) {
    return val.replace(/^\s+|\s+$/g, '').split(/\s+/);
  }
  function extractLast( term ) {
    term = term.replace(/[^\w\s'ÁÉÍÓÚáéíóú]/g, "").replace(/\s+/g, " ").toLowerCase();
    return split( term ).pop();
  }
  function extractLastWords( currentText ) {
    currentText = currentText.replace(/[^\w\s'ÁÉÍÓÚáéíóú]/g, "").replace(/\s+/g, " ").toLowerCase();
    var afterWithout = currentText.substr(0, currentText.lastIndexOf(" "));
    let afterWithoutList = split(afterWithout).slice(-ngram_size);
    console.log(afterWithout);
    console.log(afterWithoutList);
    return afterWithoutList;
  }

  function updateAvailableTags( currentText ) { // predicts next word on change
    var last_words = extractLastWords(currentText);
    var last_sequence = last_words.map(function(word) {
      word = word2index[word];
      return(word);
    });
    if(last_sequence.length == ngram_size){
      var last_sequence_tensor = tf.tensor(last_sequence).reshape([-1, ngram_size]);
      var pred_seq = model.predict(last_sequence_tensor).dataSync();
      var pred_sorting = Array.from(Array(pred_seq.length).keys())
        .sort((a, b) => pred_seq[a] > pred_seq[b] ? -1 : (pred_seq[b] < pred_seq[a]) | 0);
      var pred_words = pred_sorting.map(function(word) {
        word = index2word[word];
        return(word);
      });
      availableTags = pred_words.slice(0, n_preds);
    }    
  }

  var cursorPos;
  var cursorPosLast;
  var endingText, startingText;
  $( "#tags_contenido" )
    // don't navigate away from the field on tab when selecting an item
    .on( "keydown", function( event ) {
      if ( event.keyCode === $.ui.keyCode.TAB &&
          $( this ).autocomplete( "instance" ).menu.active ) {
            event.preventDefault();
      }
    })
    .autocomplete({
      minLength: 0,
      delay: 10,
      search: function( event, ui ){
        cursorPos = $(this).prop('selectionStart');
      },
      source: function( request, response ) { // delegate back to autocomplete, but extract the last term

        let lastChar = request.term.substring(cursorPos - 1, cursorPos);
        if (lastChar == ' ' || lastChar == '\n'){
          cursorPosLast = cursorPos;
          startingText = request.term.substring(0, cursorPosLast);
          endingText = request.term.substring(cursorPosLast);
          updateAvailableTags(startingText);
        }

        // Overrides the default autocomplete filter function to search only from the beginning of the string
        $.ui.autocomplete.filter_startWith = function (array, matchingWord) {
          var matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex(matchingWord), "i");

          var completeList = $.grep(array, function (value) {
            return matcher.test(value);
          });
          var shortenedList = completeList.slice(0, n_best_preds);
          return shortenedList;
        };
        if (extractLast( request.term.substring(0, cursorPos) ) == extractLastWords( request.term.substring(0, cursorPos) ).slice(-1)[0]){
          var matchingWord = "";
        }
        else{
          var matchingWord = extractLast( request.term.substring(0, cursorPos) );
        };
        console.log(matchingWord)
        response( $.ui.autocomplete.filter_startWith( availableTags, matchingWord ) );
      },
      focus: function( event, ui ) { // replace with the focused suggestion
        var lastIndex_s = this.value.substring(0, cursorPosLast).lastIndexOf(" ");
        var lastIndex_n = this.value.substring(0, cursorPosLast).lastIndexOf("\n");
        if (lastIndex_s > lastIndex_n){ // period space
          if(this.value[lastIndex_s-1] == "."){
            this.value = startingText + (ui.item.value.substring(0, 1)).toUpperCase() + ui.item.value.substring(1) + endingText;
            this.selectionStart = (startingText + ui.item.value).length;
            this.selectionEnd = this.selectionStart;
          }
          else{ // space
            this.value = startingText + ui.item.value + endingText;
            this.selectionStart = (startingText + ui.item.value).length;
            this.selectionEnd = this.selectionStart;
          }
        }
        else{ // full stop
          this.value = startingText + (ui.item.value.substring(0, 1)).toUpperCase() + ui.item.value.substring(1) + endingText;
          this.selectionStart = (startingText + ui.item.value).length;
          this.selectionEnd = this.selectionStart;
        };
        return false;
      },
      select: function( event, ui ) {
        return false;
      }
    });
} );
