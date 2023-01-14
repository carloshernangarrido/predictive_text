import string
from typing import List
import docx2txt
from PyPDF2 import PdfReader


def pdfdocx2textlist(filenames: List[str]) -> List[str]:
    text_list = []
    for filename in filenames:
        if filename.endswith('.pdf'):
            reader = PdfReader(filename)
            text_list_ = [page.extract_text() for page in reader.pages]
            text_list.append(' '.join(text_list_))
        elif filename.endswith('.docx'):
            text_list.append(docx2txt.process(filename))

    return text_list


def textlist2cleantext(text_list: List[str]) -> List[str]:
    data_list = []
    for data in text_list:
        data = data.replace('-\n', '').replace('\n', ' ').replace('  ', ' ').replace('\r', '').replace('\ufeff', '').\
            replace('ﬁ', 'fi')
        translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))  # map punctuation to space
        data = data.translate(translator)
        data = ' '.join([word for word in data.split(' ') if word.isalpha()])
        data_list.append(data)
    return data_list
