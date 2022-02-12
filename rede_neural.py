
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
#from tf.optimizers.Adam import Adam
from keras.callbacks import EarlyStopping

import sklearn
from sklearn import preprocessing
from sklearn.metrics import r2_score
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error




def criar_rede_neural(lista):


    model = Sequential()
    model.add(Dense(20, input_shape=(len(lista[0])-1,), activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(25, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(80, activation='relu'))
    model.add(Dropout(0.7))
    model.add(Dense(25, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(20, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(1,))
    model.compile(keras.optimizers.Adam(learning_rate=0.003), 'mean_squared_error')

    X = []
    y = []
    for i in range(0, len(lista)):
        X.append([])
        y.append([])
        for j in range(0,len(lista[i])-1):
            X[i].append(lista[i][j])
        y[i].append(lista[i][len(lista[i])-1])
    X = np.array(X)
    y = np.array(y)


    #X = lista
    #y = lista
    kf = KFold(n_splits=5)
    sum_score = 0
    sum_MSE   = 0
    for train_index, test_index in kf.split(X):
        #print("TRAIN:", train_index, "TEST:", test_index)
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]


        history = model.fit(X_train,y_train, epochs = 500, verbose = 0)


        y_test_pred = model.predict(X_test)
        #print(f"tamanho pred: {len(y_test_pred)}")

        score = r2_score(y_test, y_test_pred)
        MSE = mean_squared_error(y_test, y_test_pred, squared=False)
        #print(f"\n y_test : {y_test}\n")
        #print(f"\n y_test_pred : {y_test_pred}\n")
        sum_score += score
        sum_MSE += MSE
        print(f"\nscore : {score}\n")
        print(f"\nMSE : {MSE}\n")
    media_score = sum_score/5
    print(f"\nmedia score : {media_score}\n")
    media_MSE = sum_MSE/5
    print(f"\nmedia MSE : {media_MSE}\n")

    return model,media_score,media_MSE
