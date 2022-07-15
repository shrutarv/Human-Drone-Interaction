from imu.interface_IMU import interface_IMU
from tensorflow import keras
from scipy.signal import resample
import numpy as np



RE = interface_IMU('D3:FE:9A:01:90:57')
model = keras.models.load_model('/home/violet/Master_Thesis/Human-Drone-Interaction/model_gyro_only')

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
        
        data_gyro = RE.get_imu_data()
        # Add your code here
        data_gyro_resampled = np.array([resample(data_gyro, 50, axis=0)])
        prediction = model.predict(data_gyro_resampled)
        gesture_idx = np.argmax(prediction)
        print(gestures[str(gesture_idx)])
        print('Confidence: ', np.max(prediction)*100,'%')


        
    except(KeyboardInterrupt):
        RE.imu_client.disconnect()
        print('IMU disconnected')
        print('Ending program')
        break