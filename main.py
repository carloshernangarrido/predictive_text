# python 3.8
import os.path
import pickle
from keras.models import load_model

from ingestion import pdf2textlist, textlist2cleantext
from models import build_model, fit_model
from predictions import make_some_predictions
from tokenization import tokenize

flags = {'build_and_fit': True,
         'tokenize': True}


def main():
    ngram_size = 2
    corpus_path = 'corpus/source_files'
    saved_models_path = 'saved_models'
    filenames = ['Garrido et al. 2021.pdf', 'Garrido et al. 2018.pdf']
    filenames = [os.path.join(corpus_path, filename) for filename in filenames]
    model_filename = os.path.join(saved_models_path, 'nextword1.h5')

    if flags['tokenize'] or flags['build_and_fit']:
        text_list = pdf2textlist(filenames)
        clean_text = textlist2cleantext(text_list)
        X, y, tokenizer, vocab_size = tokenize(clean_text, os.path.join(saved_models_path, 'tokenizer.pkl'), ngram_size)
    else:
        with open(os.path.join(saved_models_path, 'tokenizer.pkl'), 'rb') as file:
            tokenizer = pickle.load(file)
        vocab_size = len(tokenizer.word_index) + 1

    if flags['build_and_fit']:
        model = build_model(vocab_size, 0.01, ngram_size)
        model = fit_model(model, X, y, model_filename)
    else:
        model = load_model(model_filename)
    model.summary()

    make_some_predictions(model, tokenizer, ngram_size)
    ...


if __name__ == '__main__':
    main()


