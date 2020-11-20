import numpy as np
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import pandas as pd
from keras.models import Sequential, load_model
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

dataframe = pd.read_csv('us.csv', usecols=[1])
dataset = dataframe.values
dataset = dataset.astype('float32')

scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)

def create_dataset(dataset, timestep ): # step length
    dataX, dataY = [], []
    for i in range(len(dataset)-timestep -1):
        a = dataset[i:(i+timestep)]
        dataX.append(a)
        dataY.append(dataset[i + timestep])
    return np.array(dataX), np.array(dataY)

timestep  = 1
trainX, trainY = create_dataset(dataset, timestep)
trainX = np.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))

# create and fit the LSTM network
model = Sequential()
model.add(LSTM(4, input_shape=(None,1)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(trainX, trainY, epochs=100, batch_size=1, verbose=2)
model.save("LSTM.h5")

trainPredict = model.predict(trainX)
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform(trainY)
plt.figure(figsize=(10, 8))
plt.plot(trainY[10:])
plt.plot(trainPredict)
plt.title('Result on training set')
plt.xlabel('days')
plt.ylabel('nums of people')
plt.legend(['train', 'trainPredict'], loc='best')
plt.show()