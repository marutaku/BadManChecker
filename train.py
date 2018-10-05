import keras.backend as K
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from keras.optimizers import Adam
from keras.utils import np_utils
from keras.utils.vis_utils import plot_model
from keras.callbacks import EarlyStopping

import numpy as np

npy_path = './face.npy'
categories = ['badman', 'goodman']
category_length = len(categories)
image_size = 32


def main():
    X_train, X_test, Y_train, Y_test = np.load(npy_path)
    X_train = X_train.astype('float') / 256
    X_test = X_test.astype('float') / 256
    Y_train = np_utils.to_categorical(Y_train, category_length)
    Y_test = np_utils.to_categorical(Y_test, category_length)
    model = model_train(X_train, Y_train)
    model_eval(model, X_test, Y_test)


def build_model(in_shape):
    model = Sequential()
    model.add(Conv2D(32, 7, 3,
                     border_mode='same',
                     input_shape=in_shape, name='input'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Conv2D(64, 5, 3, border_mode='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(64, 3, 3))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(category_length))
    model.add(Activation('softmax'))
    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])
    return model


def model_train(X, y):
    es = EarlyStopping(monitor='val_acc', patience=5, verbose=1)
    model = build_model(X.shape[1:])
    history = model.fit(X, y, batch_size=32, nb_epoch=30, validation_split=0.1, callbacks=[es])
    model.save_weights('face-model2.h5py')
    return model


def model_eval(model, X, y):
    score = model.evaluate(X, y)
    print('loss = ', score[0])
    print('accuracy = ', score[1])


if __name__ == "__main__":
    main()
