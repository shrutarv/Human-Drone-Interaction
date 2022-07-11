from imu.interface_IMU import interface_IMU


RE = interface_IMU('D3:FE:9A:01:90:57')

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
        print(data_acc)#'acc{}'.format(data_acc.shape())
        # Add your code here

        
    except(KeyboardInterrupt):
        RE.imu_client.disconnect()
        print('IMU disconnected')
        print('Ending program')
        break