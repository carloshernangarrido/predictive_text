from prompt_toolkit import prompt
from prompt_toolkit.lexers import PygmentsLexer

from pygments.lexer import RegexLexer
from pygments.token import Name, Error

from console.prompt_custom_classes import MyCustomCompleter


def make_some_predictions(model, tokenizer, ngram_size):
    """
        We are testing our model and we will run the model
        until the user decides to stop the script.
        While the script is running we try and check if
        the prediction can be made on the text. If no
        prediction can be made we just continue.
    """

    class CustomDictionaryLexer(RegexLexer):
        vocabulary = tokenizer.word_index.keys()
        # with open("es.txt", "r") as f:
        #     dictionary = f.readlines()
        name = "Dictionary"
        tokens = {
            'root': [(r"\b(?i)" + word + r"\b", Name.Tag) for word in vocabulary] # + [(r"\b" + word + r"\b", Name.Label) for word in dictionary],
        }

    completer = MyCustomCompleter(ngram_size, model, tokenizer)
    lexer = PygmentsLexer(CustomDictionaryLexer)
    text = prompt('> ', completer=completer, lexer=lexer, complete_in_thread=True, multiline=True)
    print(f'You said: {text}')
