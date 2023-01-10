# python 3.8
import os.path

from ingestion import pdf2textlist, textlist2cleantext


def main():
    path = 'corpus/source_files'
    filenames = ['Garrido et al. 2021.pdf', 'Garrido et al. 2018.pdf']
    filenames = [os.path.join(path, filename) for filename in filenames]
    text_list = pdf2textlist(filenames)
    clean_text = textlist2cleantext(text_list)
    print(f'Hi')


if __name__ == '__main__':
    main()


