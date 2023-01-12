import numpy as np
from keras import Sequential
from keras.layers import Embedding, LSTM, Dense
from keras.optimizers import Adam

from keras.callbacks import ModelCheckpoint
from keras.callbacks import ReduceLROnPlateau
from keras.callbacks import TensorBoard


def build_model(vocab_size: int, learning_rate: float = 0.001, ngram_size: int = 2) -> Sequential:
    model = Sequential()
    model.add(Embedding(vocab_size, 100, input_length=ngram_size))
    model.add(LSTM(10, return_sequences=True))
    model.add(LSTM(100))
    model.add(Dense(100, activation="relu"))
    model.add(Dense(vocab_size, activation="softmax"))
    model.compile(loss="categorical_crossentropy", optimizer=Adam(learning_rate=learning_rate), metrics='accuracy')
    return model


def fit_model(model: Sequential, X: np.ndarray, y: np.ndarray, model_filename) -> Sequential:
    # Callbacks
    logdir = 'logsnextword1'
    checkpoint = ModelCheckpoint(model_filename, monitor='loss', verbose=1,
                                 save_best_only=True, mode='auto')
    reduce = ReduceLROnPlateau(monitor='loss', factor=0.2, patience=3, min_lr=0.0001, verbose=1)
    tensorboard_Visualization = TensorBoard(log_dir=logdir)

    model.fit(X, y, epochs=150, batch_size=64, callbacks=[checkpoint, reduce, tensorboard_Visualization])
    return model
