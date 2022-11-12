from imu.interface_IMU import interface_IMU
from tensorflow import keras
from scipy.signal import resample
import numpy as np
from matplotlib import pyplot
import matplotlib.pyplot as plt
from os import getlogin
from drone.interface_drone import InterfaceDrone

model = keras.models.load_model(f'/home/{getlogin()}/Human-Drone-Interaction/model_acc_gyro')

drone = InterfaceDrone()

RE = interface_IMU('D4:C5:36:C4:7B:78') # LE: 'D3:FE:9A:01:90:57'

gestures = {
    '0':'swipe_left',
    '1':'swipe_right',
    '2':'swipe_up',
    '3':'swipe_down',
    '4':'H cw crl',
    '5':'H ccw crl',
    '6':'V cw crl',
    '7':'V ccw crl',   
}

gesture_command = {
    '0':'Left',
    '1':'Right',
    '2':'Up',
    '3':'Down',
    '4':'CW_Circle',
    '5':'CCW_Circle',
    '6':'V cw crl',
    '7':'V ccw crl',    
}

def rescale_xyz(arr):
    xyz_max = max(arr.reshape(-1,1))[0]
    arr_scaled = arr/xyz_max
    return arr_scaled

######## Main ##############
drone.takeoff()

while True:
    try:
        log_done = False
        print('Ready to accept gesture')
        while not log_done:
            RE.acc_raw_data = []
            RE.gyro_raw_data = []
            if RE.switch_pressed:
                #RE.start_logging()
                RE.start_streaming()
                while not log_done:
                    if not RE.switch_pressed:
                        #RE.stop_logging()
                        RE.stop_streaming()
                        log_done = True
        
        #data_acc = RE.get_imu_data()
        
        data_acc, data_gyro = RE.get_data()

        data_merged = np.concatenate((data_acc, data_gyro),axis=1)

        # Add your code here
        data_resampled = resample(data_merged, 50, axis=0)
        data_rescaled = np.array([rescale_xyz(data_resampled)])
        prediction = model.predict(data_rescaled)
        gesture_idx = np.argmax(prediction)
        prediction_awg = np.average(prediction,axis=0)
        #print(data_rescaled.shape)
        print(gestures[str(gesture_idx)])
        confidence = np.max(prediction)*100
        print('Confidence: ', confidence,'%')
        if confidence>70:
            drone.perform_gesture(gesture_command.get(str(gesture_idx)))
        else:
            print("Gesture confidence too low. Aborting movement")

        #fig, axs = plt.subplots(2)
        #axs[0].plot(data_rescaled[0,:,:3])
        #axs[0].set_title('acc')
        #axs[1].plot(data_rescaled[0,:,3:])
        #axs[1].set_title('gyro')
        #plt.show()
    
    except(KeyboardInterrupt):
        RE.imu_client.disconnect()
        drone.land()
        print('IMU disconnected')
        print('Ending program')
        break