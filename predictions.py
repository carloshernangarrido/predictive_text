# Importing the Libraries
import numpy as np
# import msvcrt
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completion, Completer

from ingestion import textlist2cleantext


def predict_next_words(model, tokenizer, text_list, ngram_size: int = 2, n_preds: int = 5):
    """
        In this function we are using the tokenizer and models trained
        and we are creating the sequence of the text entered and then
        using our model to predict and return the the predicted word.
    """
    text_list = text_list[-ngram_size:]
    if len(text_list) < ngram_size:
        return []
    for word in text_list:
        if word not in tokenizer.word_index.keys():
            return []
    sequence = tokenizer.texts_to_sequences(text_list)
    sequence = np.array(sequence).reshape((-1, ngram_size))

    p = model.predict(sequence, verbose=0)[0]
    preds = p.argsort()[-n_preds::][::-1]
    predicted_words = [tokenizer.index_word[pred] for pred in preds]
    return predicted_words


def make_some_predictions(model, tokenizer, ngram_size):
    """
        We are testing our model and we will run the model
        until the user decides to stop the script.
        While the script is running we try and check if
        the prediction can be made on the text. If no
        prediction can be made we just continue.
    """
    class MyCustomCompleter(Completer):
        def get_completions(self, document, complete_event):
            text_list = document.text.split(' ')
            if len(text_list) > ngram_size + 1:
                text_list = text_list[-(ngram_size + 1):]
            text_list = [_.lower() for _ in textlist2cleantext(text_list)]
            predicted_words = predict_next_words(model, tokenizer, text_list[:-1], ngram_size, n_preds=100)
            predicted_words_filt = [_ for _ in predicted_words if _.startswith(text_list[-1])]
            for predicted_word in predicted_words_filt:
                yield Completion(predicted_word, start_position=-len(text_list[-1]))
    text = prompt('> ', completer=MyCustomCompleter(), complete_in_thread=True, multiline=True)
    print(f'You said: {text}')

