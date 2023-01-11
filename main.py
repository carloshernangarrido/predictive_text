# python 3.8
import os.path
import pickle

from ingestion import pdf2textlist, textlist2cleantext
from models import build_model, fit_model
from tokenization import tokenize

flags = {'build_and_fit': True,
         }


def main():
    corpus_path = 'corpus/source_files'
    saved_models_path = 'saved_models'
    filenames = ['Garrido et al. 2021.pdf', 'Garrido et al. 2018.pdf']
    filenames = [os.path.join(corpus_path, filename) for filename in filenames]

    text_list = pdf2textlist(filenames)
    clean_text = textlist2cleantext(text_list)
    X, y, tokenizer, vocab_size = tokenize(clean_text, os.path.join(saved_models_path, 'tokenizer.pkl'))

    if flags['build_and_fit']:
        model = build_model(vocab_size, learning_rate=0.01)
        print(" *** Before training *** ")
        model.summary()
        model = fit_model(model, X, y)
        with open(os.path.join(saved_models_path, 'model.pkl'), 'wb') as file:
            pickle.dump(model, file)
    else:
        with open(os.path.join(saved_models_path, 'model.pkl'), 'wb') as file:
            model = pickle.load(file)
    print(" *** After training *** ")
    model.summary()


    ...


if __name__ == '__main__':
    main()


