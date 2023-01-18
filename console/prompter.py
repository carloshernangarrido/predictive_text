from prompt_toolkit import prompt
from prompt_toolkit.lexers import PygmentsLexer

from pygments.lexer import RegexLexer
from pygments.token import Name

from console.prompt_custom_classes import MyCustomCompleter


def make_some_predictions(model, tokenizer, ngram_size):
    """
        We are testing our model and we will run the model
        until the user decides to stop the script.
        While the script is running we try and check if
        the prediction can be made on the text. If no
        prediction can be made we just continue.
    """

    vocabulary = list(tokenizer.word_index.keys())
    with open("es.txt", "r", encoding="utf8") as f:
        dictionary = f.read().splitlines()
    dictionary = [entry.split('/')[0] + r'(s)?' if entry.endswith('/S') else entry for entry in dictionary]
    dictionary = [entry.split('/')[0] + r'(es)?' if entry.endswith('/eS') else entry for entry in dictionary]

    # vocabulary += dictionary
    class CustomDictionaryLexer(RegexLexer):
        name = "Dictionary"
        tokens = {
            'root': [(r'(\b' + r'\b|\b(?i)'.join(vocabulary) + r'\b)', Name.Tag),
                     (r'(\b' + r'\b|\b(?i)'.join(dictionary) + r'\b)', Name.Variable)]
        }
        ...

    completer = MyCustomCompleter(ngram_size, model, tokenizer)
    lexer = PygmentsLexer(CustomDictionaryLexer)
    text = prompt('> ', completer=completer, lexer=lexer, complete_in_thread=True, multiline=True)
    print(f'You said: {text}')
