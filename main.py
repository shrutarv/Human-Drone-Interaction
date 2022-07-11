from imu.interface_IMU import interface_IMU


RE = interface_IMU('D3:FE:9A:01:90:57')

log_done = False
while True:
    try:
        while not log_done:
            if RE.switch_pressed:
                RE.start_logging()
                while not log_done:
                    if not RE.switch_pressed:
                        RE.stop_logging()
                        log_done = True
        
        data = RE.get_imu_data()
        # Add your code here

        
    except(KeyboardInterrupt):
        RE.imu_client.disconnect()
        print('IMU disconnected')
        print('Ending program')
        break