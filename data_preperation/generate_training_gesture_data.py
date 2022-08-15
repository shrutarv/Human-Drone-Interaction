import sys
sys.path.append('/home/violet/Master_Thesis/Human-Drone-Interaction/')
from imu.interface_IMU import interface_IMU
import numpy as np
from scipy.signal import resample

LE = 'D3:FE:9A:01:90:57'
RE = 'D4:C5:36:C4:7B:78'

num_data_points = 50    # No. of data points in each recorded sample 
num_features = 6    # No. of features recorded from imu
gesture_save_directory = '/home/violet/Master_Thesis/Human-Drone-Interaction/data_preperation/recorded_gestures/'

imu = interface_IMU(RE)

while True:
    try:
        print('Ready to record gestures.')
        if not input("Press 'y' to continue or Ctrl+C to end program.\n")=='y':
            print('Invalid input')
            continue
        try:
            gesture_name = input('Enter name of the gesture: ')
            num_samples = int(input('No. of samples to be recorded: '))

        except(ValueError):
            print('Invalid input')
            continue

        gesture = np.zeros((num_samples, num_data_points, num_features))
        for i in range(num_samples):
            sample_logged = False
            print('Ready to accept gesture')
            while not sample_logged:
                imu.acc_raw_data = []
                imu.gyro_raw_data = []
                if imu.switch_pressed:
                    imu.start_streaming()
                    while not sample_logged:
                        if not imu.switch_pressed:
                            imu.stop_streaming()
                            sample_logged = True
                        
            data_acc, data_gyro = imu.get_data()
            data_merged = np.concatenate((data_acc, data_gyro),axis=1)
            gesture[i] = resample(data_merged, num_data_points, axis=0)
        np.save(gesture_save_directory+gesture_name+'.npy',gesture)

    except(KeyboardInterrupt):
        imu.imu_client.disconnect()
        print('IMU disconnected')
        print('Ending program')
        break

