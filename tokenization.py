import pickle
from typing import Tuple, List

import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical


def tokenize(data_list: List[str], tokenizer_filename, ngram_size: int = 2, min_length_of_pred: int = 1) -> Tuple:
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(data_list)

    # saving the tokenizer for predict function.
    with open(tokenizer_filename, 'wb') as file:
        pickle.dump(tokenizer, file)

    sequence_data = []
    for seq in tokenizer.texts_to_sequences(data_list):
        sequence_data += seq
    vocab_size = len(tokenizer.word_index) + 1

    sequences = []
    for i in range(1, len(sequence_data)+1-ngram_size):
        words = sequence_data[i-1: i+ngram_size]
        sequences.append(words)
    sequences = np.array(sequences)

    X, y_num = [], []
    for seq in sequences:
        if len(tokenizer.index_word[seq[ngram_size]]) >= min_length_of_pred:
            X.append(seq[0:ngram_size])
            y_num.append(seq[ngram_size])
    X = np.array(X)
    y_num = np.array(y_num)
    X_words = np.array([[tokenizer.index_word[x] for x in x_] for x_ in X])
    y_words = np.array([tokenizer.index_word[y_] for y_ in y_num])
    y = to_categorical(y_num, num_classes=vocab_size)

    return X, y, tokenizer, vocab_size
