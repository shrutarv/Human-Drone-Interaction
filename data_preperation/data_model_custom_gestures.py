# Import necessary packages
import numpy as np
from matplotlib import pyplot
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from numpy import mean
from numpy import std
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM

gesture_data_path = '/home/violet/Master_Thesis/Human-Drone-Interaction/data_preperation/recorded_gestures/'

try: # Load data from file if exists
    gesture_data = np.load(gesture_data_path+'gesture_data_custom.npy')

except: # Load data from mat files and save if no saved file found

    print('Saved data not found. Loading from original files...')

    from scipy.signal import resample

    #Extract the data from mat file and save as numpy array

    gesture_names = ['swipe_right','swipe_left','swipe_up','swipe_down','swipe_forward','swipe_backward','h_cw_circle','h_ccw_circle','v_cw_circle','triangle']


    # convert the data into 3d array - the dimensions of the array are [samples, time steps, features].

    final_arr = np.zeros((1,50,6))
    for gesture in gesture_names:
        temp = np.load(gesture_data_path+gesture+'.npy')
        final_arr = np.concatenate((final_arr,temp),axis=0)
                    
    gesture_data = final_arr[1:,:,:]
    # Save the array as a file
    np.save(gesture_data_path+'gesture_data_custom.npy',gesture_data)

# Rescale function
def rescale(arr):
    xyz_max = max(np.abs(arr).reshape(-1,1))[0]
    arr_rescaled = arr/xyz_max
    return arr_rescaled

# Rescale data
num_samples = gesture_data.shape[0]
gesture_data_rescaled = np.zeros(gesture_data.shape)
for i in range(num_samples):
    gesture_data_rescaled[i] = rescale(gesture_data[i])

# # Save the array as a file
# gesture_data_rescaled_path = '/home/violet/Master_Thesis/Human-Drone-Interaction/data_preperation/gesture_data_rescaled.npy'
# np.save(gesture_data_rescaled_path,gesture_data_rescaled)

# prepare class categories for 1-hot encoding
class_output=np.zeros((gesture_data_rescaled.shape[0],1))
class_output[0:10]=0  # gesture0 - swipe right
class_output[10:20]=1 # gesture1 - swipe left
class_output[20:30]=2 # gesture1 - swipe up
class_output[30:40]=3 # gesture1 - swipe down
class_output[40:50]=4 # gesture1 - swipe forward
class_output[50:60]=5 # gesture1 - swipe backward
class_output[60:70]=6 # gesture1 - h_cw_circle
class_output[70:80]=7 # gesture1 - h_ccw_circle
class_output[80:90]=8 # gesture1 - v_cw_circle
class_output[90:100]=9 # gesture1 - triangle

# one hot encoding 
one_hot_output = to_categorical(class_output, num_classes=10, dtype="float64")

# split the data to train and test

trainX, testX, trainy, testy = train_test_split(gesture_data_rescaled, one_hot_output, test_size=0.30, train_size=0.70, shuffle=True)

#fit and evaluate the LSTM model

verbose, epochs, batch_size = 1, 20, 5
n_timesteps, n_features, n_outputs = trainX.shape[1], trainX.shape[2], trainy.shape[1]
model = Sequential()
model.add(LSTM(10, input_shape=(n_timesteps,n_features)))
model.add(Dropout(0.5))
model.add(Dense(10, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(n_outputs, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# fit network
history = model.fit(trainX, trainy, epochs=epochs, validation_split=0.33 ,batch_size=batch_size, verbose=verbose)
#print('model loss',history.history['loss'])
#print('model accuracy',history.history['accuracy'])
#print('model val_loss',history.history['val_loss'])
#print('model val_accuracy',history.history['val_accuracy'])
pyplot.plot(history.history['loss'])
pyplot.plot(history.history['val_loss'])
pyplot.title('comparing model training vs validation loss')
pyplot.ylabel('loss')
pyplot.xlabel('epoch number')
pyplot.legend(['train loss', 'validation loss'], loc='upper right')
pyplot.show() 
# evaluate model)
_, accuracy = model.evaluate(testX, testy, batch_size=batch_size, verbose=verbose)
accuracy= accuracy*100.0
print('Accuracy: ',accuracy,'%')

# save the model
model.save('/home/violet/Master_Thesis/Human-Drone-Interaction/model_acc_gyro_custom')