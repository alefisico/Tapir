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
import os
import glob
import numpy as np

import tensorflow
print(tensorflow.__path__)

import keras
print(keras.__path__)

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.utils import plot_model

from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, BatchNormalization, LeakyReLU
from keras.optimizers import RMSprop

from keras import backend as K
K.set_session(K.tf.Session(config=K.tf.ConfigProto(intra_op_parallelism_threads=4, inter_op_parallelism_threads=1)))

# prepare data for training
def prepare_data(fpath):

    os.chdir(fpath)

    count = 0
    for npfile in glob.glob("*_training.csv"):
        filepath = os.path.join(fpath, npfile)
        print(filepath)
        if count == 0:
            d = pd.read_csv(filepath, delim_whitespace=True)
        else:
            d = d.append(pd.read_csv(filepath, delim_whitespace=True), ignore_index = True)
        count += 1

    # do log transform for joint likelihood ratio
    d['JLR'] = d['JLR'].apply(lambda x : np.log(x))

    print(d)
    print(d.shape)
    dataset = d.values
    print(dataset.shape)

    os.chdir(sys.path[0])
    np.save("dataset.npy", dataset)


# set-up and train DNN
def training(nparray):

    batch_size = 128
    epochs = 100

    # load data, split between train and test sets
    dataset = np.load(nparray)

    frac = 1/2.
    X = dataset[:, :-1]
    y = dataset[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = frac, test_size = (1-frac))

    fig = plt.figure()
    plt.hist(y, bins = 25)
    plt.title("target distribution")
    plt.xlabel("joint likelihood ratio")
    plt.ylabel("number of entries")
    fig.savefig("target.pdf")

    # define model
    model = Sequential()
    model.add(Dense(200, input_dim = X_train.shape[1]))
    model.add(BatchNormalization())
    model.add(LeakyReLU(alpha=1.0))
    model.add(Dense(200))
    model.add(LeakyReLU(alpha=1.0))
    model.add(Dense(100))
    model.add(LeakyReLU(alpha=1.0))
    model.add(Dense(100))
    model.add(LeakyReLU(alpha=1.0))
#    model.add(Dense(128, activation='elu'))
#    model.add(Dropout(0.5))
#    model.add(Dense(128, activation='elu', input_dim = X_train.shape[1], kernel_initializer='normal'))
#    model.add(Dropout(0.5))
#    model.add(Dense(128, activation='elu', input_dim = X_train.shape[1], kernel_initializer='normal'))
#    model.add(Dropout(0.5))
    model.add(Dense(1))

    model.summary()
    plot_model(model, to_file='model.png')

    adam = keras.optimizers.Adam(lr=0.00001)
    model.compile(loss='mean_squared_error', optimizer=adam)

    history = model.fit(X_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_data=(X_test, y_test))

    # test functions 
    fig = plt.figure()
    n, bins, patches = plt.hist(y_train, bins = 25, alpha = 0.6)
    plt.hist(model.predict(X_train), bins = bins, alpha = 0.6)
    plt.legend(["true", "predict"], loc='upper right')
    plt.title("target distribution")
    plt.xlabel("joint likelihood ratio")
    plt.ylabel("number of entries")
    fig.savefig("target.pdf")

    fig = plt.figure()
    plt.scatter(y_train, model.predict(X_train))
    plt.ylabel("predicted")
    plt.xlabel("true")
    plt.xlim([-8,8])
    plt.ylim([-8,8])
    fig.savefig("corr.pdf")

    fig = plt.figure()
    plt.plot(history.history["loss"])   
    plt.plot(history.history["val_loss"]) 
    plt.title("model loss")
    plt.ylabel("loss")
    plt.xlabel("epoch")
    plt.legend(["train", "test"], loc='upper right')
    fig.savefig("loss.pdf")  
 
    #model.save("DNN_classifier.h5")
    print(model.predict(X_train))
    print(y_train)




if __name__ == "__main__":

    fpath = "/mnt/t3nfs01/data01/shome/creissel/tth/2017/gc/meanalysis/GC8f13483f493b/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/"
    prepare_data(fpath)
    training("dataset.npy")

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
