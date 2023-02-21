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
    return split( term ).pop();
  }
  function extractLastWords( currentText ) {
    var afterWithout = currentText.substr(0, currentText.lastIndexOf(" "));
    return split(afterWithout
      .replace(/[^[A-Za-z0-9ÁÉÍÓÚáéíóú]\s\']|_/g, "")
      .replace(/\s+/g, " ")
      .toLowerCase())
      .slice(-ngram_size);
  }

  function updateAvailableTags( currentText ) { // predicts next word on change
    var last_words = extractLastWords(currentText);
    // console.log('*** current text:', currentText);
    // console.log('*** current text:', last_words);
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
      source: function( request, response ) { // delegate back to autocomplete, but extract the last term
        
        let lastChar = request.term.substring(request.term.length - 1, request.term.length);
        if (lastChar == ' '){
          updateAvailableTags(request.term)
        }

        // Overrides the default autocomplete filter function to search only from the beginning of the string
        $.ui.autocomplete.filter_startWith = function (array, matchingWord) {
          var matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex(matchingWord), "i");

          var completeList = $.grep(array, function (value) {
            // return matcher.test(value.label || value.value || value);
            return matcher.test(value);
          });
          var shortenedList = completeList.slice(0, n_best_preds);
          // console.log('complete', completeList);
          // console.log('shortened', shortenedList);
          return shortenedList;
        };
        if (extractLast( request.term ) == extractLastWords( request.term ).slice(-1)[0]){
          var matchingWord = "";
        }
        else{
          var matchingWord = extractLast( request.term );
        };
        response( $.ui.autocomplete.filter_startWith( availableTags, matchingWord ) );
      },
      focus: function( event, ui ) { // replace with the focused suggestion
        var lastIndex_s = this.value.lastIndexOf(" ");
        var lastIndex_n = this.value.lastIndexOf("\n");
        if (lastIndex_s > lastIndex_n){
          if(this.value[lastIndex_s-1] == "."){
            this.value = this.value.substring(0, lastIndex_s + 1) 
            + (ui.item.value.substring(0, 1)).toUpperCase() + ui.item.value.substring(1);
          }
          else{
            this.value = this.value.substring(0, lastIndex_s + 1) 
            + ui.item.value.substring(0);
          }
        }
        else{
          this.value = this.value.substring(0, lastIndex_n + 1) 
            + (ui.item.value.substring(0, 1)).toUpperCase() + ui.item.value.substring(1);
        };
        return false;
      },
      select: function( event, ui ) {
        return false;
      }
    });
} );
