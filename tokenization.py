import pickle
from typing import Tuple

import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical


def tokenize(data: str, tokenizer_filename, ngram_size: int = 1) -> Tuple:
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts([data])

    # saving the tokenizer for predict function.
    with open(tokenizer_filename, 'wb') as file:
        pickle.dump(tokenizer, file)

    sequence_data = tokenizer.texts_to_sequences([data])[0]
    vocab_size = len(tokenizer.word_index) + 1

    sequences = []
    for i in range(1, len(sequence_data)+1-ngram_size):
        words = sequence_data[i-1: i+ngram_size]
        sequences.append(words)
    sequences = np.array(sequences)

    X, y_num = [], []
    for i in sequences:
        X.append(i[0:ngram_size])
        y_num.append(i[ngram_size])
    X = np.array(X)
    y_num = np.array(y_num)
    # X_words = np.array([[tokenizer.index_word[x] for x in x_] for x_ in X])
    # y_words = np.array([tokenizer.index_word[y_] for y_ in y_num])
    y = to_categorical(y_num, num_classes=vocab_size)

    return X, y, tokenizer, vocab_size
