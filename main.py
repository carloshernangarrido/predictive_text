# python 3.8
import os.path
import pickle
import warnings

from keras.models import load_model
import tensorflowjs as tfjs
import json


from ingestion import pdfdocx2textlist, textlist2cleantext
from models import build_model, fit_model
from console.prompter import make_some_predictions
from tokenization import tokenize

flags = {'build_and_fit': False,
         'tokenize': False,  # ignored if 'build_and_fit'
         'load_previous_checkpoint': False,
         'save_js': True}


def main():
    ngram_size = 3
    min_length_of_pred = 4
    corpus_path = 'corpus/source_files'
    saved_models_path = 'saved_models'
    model_name = 'nextword1_libro_blanco_min4.h5'
    # filenames = ['Garrido et al. 2021.pdf', 'Garrido et al. 2018.pdf', '01 - El Gran Mago.docx']
    filenames = ['Libro_Blanco_Anatomia_Patologica_2019.pdf']
    filenames = [os.path.join(corpus_path, filename) for filename in filenames]
    model_filename = os.path.join(saved_models_path, model_name)
    tfjs_target_dir = os.path.join(saved_models_path, 'js', model_name)

    if flags['tokenize'] or flags['build_and_fit']:
        text_list = pdfdocx2textlist(filenames)
        clean_text = textlist2cleantext(text_list)
        X, y, tokenizer, vocab_size = \
            tokenize(clean_text, os.path.join(saved_models_path, 'tokenizer.pkl'), ngram_size,
                     min_length_of_pred=min_length_of_pred)
    else:
        with open(os.path.join(saved_models_path, 'tokenizer.pkl'), 'rb') as file:
            tokenizer = pickle.load(file)
        vocab_size = len(tokenizer.word_index) + 1

    if flags['build_and_fit']:
        if flags['load_previous_checkpoint']:
            model = load_model(model_filename)
        else:
            model = build_model(vocab_size, 0.01, ngram_size)
        model = fit_model(model, X, y, model_filename)
    else:
        model = load_model(model_filename)
        if model.input.shape[1] != ngram_size:
            ngram_size = model.input.shape[1]
            warnings.warn(f'ngram_size was set to {ngram_size}')
    model.summary()

    if flags['save_js']:
        tfjs.converters.save_keras_model(model, tfjs_target_dir)
        with open(os.path.join(tfjs_target_dir, 'tokenizer_word2index.json'), 'w') as file:
            json.dump(tokenizer.word_index, file)
        with open(os.path.join(tfjs_target_dir, 'tokenizer_index2word.json'), 'w') as file:
            json.dump(tokenizer.index_word, file)

    make_some_predictions(model, tokenizer, ngram_size)
    ...


if __name__ == '__main__':
    main()


