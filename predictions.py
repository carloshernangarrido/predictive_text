# Importing the Libraries
import numpy as np
from keras.utils import pad_sequences


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
    sequence = pad_sequences([sequence], maxlen=ngram_size)[0]

    sequence = np.array(sequence).reshape((-1, ngram_size))

    p = model.predict(sequence, verbose=0)[0]
    preds = p.argsort()[-n_preds::][::-1]
    predicted_words = [tokenizer.index_word[pred] for pred in preds]
    return predicted_words

