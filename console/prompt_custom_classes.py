from keras import Sequential
from keras.preprocessing.text import Tokenizer
from prompt_toolkit.completion import Completion, Completer

from ingestion import textlist2cleantext
from predictions import predict_next_words


class MyCustomCompleter(Completer):
    def __init__(self, ngram_size: int, model: Sequential, tokenizer: Tokenizer, best_m_of_n : tuple = (5, 100)):
        self.tokenizer = tokenizer
        self.model = model
        self.ngram_size = ngram_size
        self.best_m_of_n = best_m_of_n

    def get_completions(self, document, complete_event):
        text_list = document.text.split(' ')
        if len(text_list) > self.ngram_size + 1:
            text_list = text_list[-(self.ngram_size + 1):]
        text_list = [_.lower() for _ in textlist2cleantext(text_list)]
        predicted_words = predict_next_words(self.model, self.tokenizer, text_list[:-1], self.ngram_size,
                                             n_preds=self.best_m_of_n[1])
        predicted_words_filt = [_ for _ in predicted_words if _.startswith(text_list[-1])][:self.best_m_of_n[0]]
        for predicted_word in predicted_words_filt:
            yield Completion(predicted_word, start_position=-len(text_list[-1]))
