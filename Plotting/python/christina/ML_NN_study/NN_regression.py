'''Trains a simple deep NN on the MNIST dataset.

Gets to 98.40% test accuracy after 20 epochs
(there is *a lot* of margin for parameter tuning).
2 seconds per epoch on a K520 GPU.
'''

### execute with OMP_NUM_THREADS=4 KERAS_BACKEND=tensorflow python NN_regression.py

from __future__ import print_function

import sys
newpath = []
print(sys.path)
for p in sys.path:
    if "local" in p:
        continue
    newpath += [p]
sys.path = newpath

import pandas as pd

import tensorflow
print(tensorflow.__path__)

import keras
print(keras.__path__)

from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop

from keras import backend as K
K.set_session(K.tf.Session(config=K.tf.ConfigProto(intra_op_parallelism_threads=4, inter_op_parallelism_threads=1)))

batch_size = 128
epochs = 50

# the data, split between train and test sets
csvfile = "/mnt/t3nfs01/data01/shome/creissel/tth/2017/sw/CMSSW_9_4_5_cand1/src/TTH/MEAnalysis/python/training.csv"
dataframe = pd.read_csv(csvfile, delim_whitespace=True)
dataset = dataframe.values
shape = dataset.shape

frac = 1/2.
X_train = dataset[:int(shape[0]*frac), :-1]
y_train = dataset[:int(shape[0]*frac), -1]
X_test = dataset[int(shape[0]*frac): , :-1]
y_test = dataset[int(shape[0]*frac): , -1]


# define model
model = Sequential()
model.add(Dense(100, activation='tanh', input_dim = X_train.shape[1], kernel_initializer='normal'))
model.add(Dense(1, kernel_initializer='normal', activation='sigmoid'))

model.summary()

model.compile(loss='mean_squared_error', optimizer='adam')

history = model.fit(X_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_data=(X_test, y_test))


"""

# evaluate model with standardized dataset
seed = 0
np.random.seed(seed)
estimators = []
estimators.append(('standardize', StandardScaler()))
estimators.append(('mlp', KerasRegressor(build_fn=model, epochs=50, batch_size=100, verbose=0)))
pipeline = Pipeline(estimators)


(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(60000, 784)
x_test = x_test.reshape(10000, 784)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

model = Sequential()
model.add(Dense(512, activation='relu', input_shape=(784,)))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(num_classes, activation='softmax'))

model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(),
              metrics=['accuracy'])

history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_data=(x_test, y_test))
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
"""
