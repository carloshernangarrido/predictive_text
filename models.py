from keras import Sequential
from keras.layers import Embedding, LSTM, Dense


def build_model(vocab_size: int) -> Sequential:
    model = Sequential()
    model.add(Embedding(vocab_size, 10, input_length=1))
    model.add(LSTM(1000, return_sequences=True))
    model.add(LSTM(1000))
    model.add(Dense(1000, activation="relu"))
    model.add(Dense(vocab_size, activation="softmax"))
    return model
