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
from keras.layers import GRU
from keras.utils import to_categorical

gesture_data_path = '/home/violet/Master_Thesis/Human-Drone-Interaction/data_preperation/gesture_data.npy'

try: # Load data from file if exists
    gesture_data = np.load(gesture_data_path)

except: # Load data from mat files and save if no saved file found

    print('Saved data not found. Loading from mat files...')

    from copy import deepcopy
    import scipy.io as sio
    from scipy.signal import resample
    from numpy import vstack

    #Extract the data from mat file and save as numpy array

    tester_L=("D2","F1","J4","R1","S3","W2","Y2")
    tester_R=("B1","B2","C1","C2","D1","J1","J2","J3","J5","M1","M2","M3","R2","S1","S2","T1","T2","U1","W1","Y1","Y3")
    tester=("D2","F1","J4","R1","S3","W2","Y2","B1","B2","C1","C2","D1","J1","J2","J3","J5","M1","M2","M3","R2","S1","S2","T1","T2","U1","W1","Y1","Y3")
    gesture_index=("00","01","02","03","14","15","16","17")

    mat_data_L = {}
    for k in tester_L:   
        for j in gesture_index:
            for i in range(1, 11):
                filename  = "g{}_{}_t{:02d}".format(j,k,i)
                mat_data_L[filename] = sio.loadmat('/home/violet/Master_Thesis/6DMG/matL/'+filename+'.mat')    
    del i,j,k

    mat_data_R = {}
    for k in tester_R:   
        for j in gesture_index:
            for i in range(1, 11):
                filename  = "g{}_{}_t{:02d}".format(j,k,i)
                mat_data_R[filename] = sio.loadmat('/home/violet/Master_Thesis/6DMG/matR/'+filename+'.mat')
    del i,j,k
                                                
    # merge matl and matr

    mat_data = dict(list(mat_data_L.items())+list(mat_data_R.items()))

    # Data preprocessing
    # Resample data to 50 samples 

    num_samples = 50
    mat_data_resampled = deepcopy(mat_data)
    for i in gesture_index:
        for j in tester:   
            for k in range(1, 11):
                keyname  = "g{}_{}_t{:02d}".format(i,j,k)
                #saving only accelerometer and gyroscope data
                mat_data_resampled[keyname]['gest'] = resample(mat_data_resampled[keyname]['gest'][8:14,:], num_samples, axis=1)


    # #Rescale data to range -1 to 1
    # mat_data_rescaled = deepcopy(mat_data_resampled)

    # for i in gesture_index:
    #     for j in tester:   
    #         for k in range(1, 11):
    #             keyname  = "g{}_{}_t{:02d}".format(i,j,k)
    #             mat_data_rescaled[keyname]['gest'] = rescale_xyz(mat_data_rescaled[keyname]['gest'])
    # del i,j,k

    # convert the data into 3d array - the dimensions of the array are [samples, time steps, features].

    final_arr = np.zeros((1,50,6))
    idxx = 0
    for i in gesture_index:
        for j in tester:   
            for k in range(1, 11):
                
                filename  = "g{}_{}_t{:02d}".format(i,j,k)
                temp = mat_data_resampled[filename]["gest"]
                temp = np.array([temp.transpose()])
                final_arr = vstack((final_arr,temp))
                
                idxx+=1
                
    gesture_data = final_arr[1:,:,:]
    # Save the array as a file
    np.save(gesture_data_path,gesture_data)

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

# Save the array as a file
gesture_data_rescaled_path = '/home/violet/Master_Thesis/Human-Drone-Interaction/data_preperation/gesture_data_rescaled.npy'
np.save(gesture_data_rescaled_path,gesture_data_rescaled)

# prepare class categories for 1-hot encoding
class_output=np.zeros((2240,1))
class_output[0:280]=0   #gesture0 - swipe left
class_output[280:560]=1 # gesture1 - swipe right
class_output[560:840]=2 # gesture1 - swipe up
class_output[840:1120]=3 # gesture1 - swipe down
class_output[1120:1400]=4 # gesture1 - H cw crl
class_output[1400:1680]=5 # gesture1 - H ccw crl
class_output[1680:1960]=6 # gesture1 - V cw crl
class_output[1960:2240]=7 # gesture1 - V ccw crl

# one hot encoding 
one_hot_output = to_categorical(class_output, num_classes=8, dtype="float64")

# split the data to train and test

trainX, testX, trainy, testy = train_test_split(gesture_data_rescaled, one_hot_output, test_size=0.30, train_size=0.70, shuffle=True)

#fit and evaluate the LSTM model

verbose, epochs, batch_size = 1, 25, 64
n_timesteps, n_features, n_outputs = trainX.shape[1], trainX.shape[2], trainy.shape[1]
model = Sequential()
model.add(GRU(80, input_shape=(n_timesteps,n_features)))
model.add(Dropout(0.5))
model.add(Dense(80, activation='relu'))
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
model.save('/home/violet/Master_Thesis/Human-Drone-Interaction/model_acc_gyro')

# Prediction test
test_gesture = np.array([gesture_data_rescaled[0]])
pred_arr = model.predict(test_gesture)
print(pred_arr)