from imu.interface_IMU import interface_IMU
from tensorflow import keras
from scipy.signal import resample
import numpy as np



RE = interface_IMU('D3:FE:9A:01:90:57') #LE
#RE = interface_IMU('D4:C5:36:C4:7B:78')
model = keras.models.load_model('/home/violet/Master_Thesis/Human-Drone-Interaction/model_acc_only')

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
def rescale_xyz(arr):
    xyz_max = max(arr.reshape(-1,1))[0]
    arr_scaled = arr/xyz_max
    return arr_scaled

while True:
    try:
        log_done = False
        print('Ready to accept gesture')
        while not log_done:
            if RE.switch_pressed:
                RE.start_logging()
                while not log_done:
                    if not RE.switch_pressed:
                        RE.stop_logging()
                        log_done = True
        
        data_acc = RE.get_imu_data()
        # Add your code here
        data_acc_resampled = resample(data_acc, 50, axis=0)
        data_acc_rescaled = np.array([rescale_xyz(data_acc_resampled)])
        prediction = model.predict(data_acc_rescaled)
        gesture_idx = np.argmax(prediction)
        print(gestures[str(gesture_idx)])
        print('Confidence: ', np.max(prediction)*100,'%')


        
    except(KeyboardInterrupt):
        RE.imu_client.disconnect()
        print('IMU disconnected')
        print('Ending program')
        break