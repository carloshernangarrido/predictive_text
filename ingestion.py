import string
from typing import List

from PyPDF2 import PdfReader


def pdf2textlist(filenames: List[str]) -> List[str]:
    text_list = []
    for filename in filenames:
        reader = PdfReader(filename)
        text_list_ = [page.extract_text() for page in reader.pages]
        text_list += text_list_
    return text_list


def textlist2cleantext(text_list: List[str]) -> str:
    data = ' '.join(text_list)
    data = data.replace('-\n', '').replace('\n', ' ').replace('  ', ' ').replace('\r', '').replace('\ufeff', '').\
        replace('ﬁ', 'fi')
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))  # map punctuation to space
    data = data.translate(translator)
    # Avoid repeating word
    # z = []
    # for i in data.split():
    #     if i not in z:
    #         z.append(i)
    # data = ' '.join(z)
    data = ' '.join([word for word in data.split(' ') if word.isalpha()])
    return data