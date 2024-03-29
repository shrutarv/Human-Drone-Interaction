from pymetawear.client import MetaWearClient
from pymetawear.exceptions import PyMetaWearException, PyMetaWearDownloadTimeout

from time import sleep
import numpy as np

class interface_IMU:
    def __init__(self, mac_addr) -> None:
        '''
        This class creates a client to connect to IMU. It has methods to start and stop recording data and then download it.
        '''
        self.imu_client = MetaWearClient(mac_addr)
        self.monitor_imu()
        
        self.acc_raw_data = []
        self.gyro_raw_data = []

        #setup accelerometer and gyroscope
        self.imu_client.accelerometer.set_settings(data_rate=50)
        self.imu_client.accelerometer.high_frequency_stream = False
        self.imu_client.gyroscope.set_settings(data_rate=50)

        self.switch_pressed = None

    def monitor_imu(self):
        '''
        Start monitoring IMU
        '''
        def switch_callback(data):
            """Handle a switch status integer (1 for pressed, 0 for released.)."""
            if data['value'] == 1:
                self.switch_pressed = True
                # print('on')            

            elif data['value'] == 0:
                self.switch_pressed = False
                # print('off')
        
        #Subscribe to imu button notifications
        self.imu_client.switch.notifications(switch_callback)

    
#     def start_logging(self):
#         self.imu_client.accelerometer.start_logging()
#         print('started data logging')

#     def stop_logging(self):
#         self.imu_client.accelerometer.stop_logging()
#         print('completed data logging')

    def convert_data(self,data):
        converted_data = np.zeros((len(data),3))
        for i in range(len(data)):
        #exchanging the naming to match with 6DMG dataset
            converted_data[i,0] = data[i]['value'].x #x 
            converted_data[i,1] = data[i]['value'].y #y
            converted_data[i,2] = data[i]['value'].z #z
        return converted_data


    # def download_data(self):
    #     print("Downloading data...")
    #     download_done = False
    #     n = 0
    #     data = None
    #     while (not download_done) and n < 3:
    #         try:
    #             data = self.imu_client.accelerometer.download_log()
    #             data_gyro = self.convert_data(data)

    #             download_done = True
    #         except PyMetaWearDownloadTimeout:
    #             print("Download of log interrupted. Trying to reconnect...")
    #             self.imu_client.disconnect()
    #             self.imu_client.connect()
    #             n += 1
    #     return data_gyro
    
    # def get_imu_data(self):
    #     data_acc = self.download_data()
    #     return data_acc

    def start_streaming(self):
        def acc_callback(data):
            #print("Acc:",data) # [{0}] - X: {1}, Y: {2}, Z: {3}".format(data[0], *data[1]))
            self.acc_raw_data.append(data) 

        def gyro_callback(data):
            #print("gyro:",data) # [{0}] - X: {1}, Y: {2}, Z: {3}".format(data[0], *data[1]))
            self.gyro_raw_data.append(data)


        print("Subscribing to gyroscope signal notifications...")
        self.imu_client.gyroscope.notifications(gyro_callback)
        print("Subscribing to accelerometer signal notifications...")
        self.imu_client.accelerometer.notifications(acc_callback)

    def stop_streaming(self):
        self.imu_client.gyroscope.notifications(None)
        self.imu_client.accelerometer.notifications(None)

    def get_data(self):
        acc_data = self.convert_data(self.acc_raw_data)
        gyro_data = self.convert_data(self.gyro_raw_data)
        # Match the lengths of both the data
        if(acc_data.shape[0]>gyro_data.shape[0]):
            acc_data = acc_data[0:gyro_data.shape[0],:]
        else:
            gyro_data = gyro_data[0:acc_data.shape[0],:]
        return(acc_data, gyro_data)