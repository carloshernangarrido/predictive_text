# python 3.8
import os.path

from ingestion import pdf2textlist, textlist2cleantext
from models import build_model
from tokenization import tokenize


def main():
    path = 'corpus/source_files'
    filenames = ['Garrido et al. 2021.pdf', 'Garrido et al. 2018.pdf']
    filenames = [os.path.join(path, filename) for filename in filenames]
    text_list = pdf2textlist(filenames)
    clean_text = textlist2cleantext(text_list)
    X, y, tokenizer, vocab_size = tokenize(clean_text, os.path.join(path, 'tokenizer.pkl'))
    model = build_model(vocab_size)

    ...


if __name__ == '__main__':
    main()


