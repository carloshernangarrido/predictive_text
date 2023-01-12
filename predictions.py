# Importing the Libraries
import numpy as np
import msvcrt


def predict_next_words(model, tokenizer, text_list, ngram_size: int = 2):
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
    sequence = np.array(sequence).reshape((-1, ngram_size))

    p = model.predict(sequence, verbose=0)[0]
    preds = p.argsort()[-5::][::-1]
    predicted_words = [tokenizer.index_word[pred] for pred in preds]
    return predicted_words


def make_some_predictions(model, tokenizer, ngram_size):
    """
        We are testing our model and we will run the model
        until the user decides to stop the script.
        While the script is running we try and check if
        the prediction can be made on the text. If no
        prediction can be made we just continue.
    """

    print("Enter your line: ")
    text_list = []
    word = ''
    last_space = False
    predicted_words = ['']
    while True:
        if msvcrt.kbhit():
            char = msvcrt.getche().decode(encoding='cp1252')
            if char != ' ':
                last_space = False
                word += char
            elif char == ' ' and last_space:
                if len(predicted_words) != 0:
                    text_list.append(predicted_words[0])
                    print(predicted_words[0])
                text_list.append(predicted_words[0])
                predicted_words = predict_next_words(model, tokenizer, text_list, ngram_size)
                if len(predicted_words) != 0:
                    print(predicted_words)
            else:
                last_space = True
                text_list.append(word)
                word = ''
                predicted_words = predict_next_words(model, tokenizer, text_list, ngram_size)
                if len(predicted_words) != 0:
                    print(predicted_words)
                if text_list[-1] == 'q':
                    print("Ending The Program.....")
                    break

    print(text_list)

    # while True:
    #     text = input("Enter your line: ")
    #
    #     if text == "stop the script":
    #         print("Ending The Program.....")
    #         break
    #     else:
    #         try:
    #             text_list = text.split(" ")
    #             while '' in text_list:
    #                 text_list.remove('')
    #             predicted_words = predict_next_words(model, tokenizer, text_list, ngram_size)
    #             print(predicted_words)
    #         except KeyError:
    #             continue
