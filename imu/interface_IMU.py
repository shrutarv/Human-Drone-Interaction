from pymetawear.client import MetaWearClient

class interface_IMU:
    def __init__(self, mac_addr) -> None:
        '''
        Connect to IMU
        '''
        self.imu_client = MetaWearClient(mac_addr)


        

    def monitor_imu(self):
        '''
        Start monitoring IMU
        '''
        def switch_callback(data):
            """Handle a switch status integer (1 for pressed, 0 for released.)."""
            if data['value'] == 1:
                self.start_logging()
            
            elif data['value'] == 0:
                self.stop_logging()
        self.imu_client.switch.notifications(switch_callback)

    
    def start_logging(self):
        print('started data logging')
        self.imu_client.accelerometer.set_settings(data_rate=50, data_range=8)
        self.imu_client.accelerometer.start_logging()
        self.imu_client.gyroscope.set_settings(data_rate=50)
        self.imu_client.gyroscope.start_logging()

    def stop_logging(self):
        print('completed data logging')
        self.imu_client.accelerometer.stop_logging()
        self.imu_client.gyroscope.stop_logging()

    def download_data(self):
        print("Downloading data...")
        download_done = False
        n = 0
        data = None
        while (not download_done) and n < 3:
            try:
                data_acc = self.imu_client.accelerometer.download_log()
                # data_gyro = self.imu_client.gyroscope.download_log()
                download_done = True
            except PyMetaWearDownloadTimeout:
                print("Download of log interrupted. Trying to reconnect...")
                self.imu_client.disconnect()
                self.imu_client.connect()
                n += 1
        return data_acc, data_gyro
    
    def get_imu_data(self):
        data_acc, data_gyro = self.download_data()
        return data_acc, data_gyro