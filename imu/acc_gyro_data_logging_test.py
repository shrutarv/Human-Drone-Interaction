# usage: python3 stream_acc_gyro_bmi160.py [mac1] [mac2] ... [mac(n)]
from __future__ import print_function
from mbientlab.metawear import MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *
from time import sleep
from threading import Event
import platform
import sys

if sys.version_info[0] == 2:
    range = xrange

class State:
    # init state
    def __init__(self, device):
        self.device = device
        self.samples = 0
        self.accCallback = FnVoid_VoidP_DataP(self.acc_data_handler)
        self.gyroCallback = FnVoid_VoidP_DataP(self.gyro_data_handler)
        
    # acc callback function
    def acc_data_handler(self, ctx, data):
        print("ACC: %s -> %s" % (self.device.address, parse_value(data)))
        self.samples+= 1
                
    # gyro callback function
    def gyro_data_handler(self, ctx, data):
        print("GYRO: %s -> %s" % (self.device.address, parse_value(data)))
        self.samples+= 1

# init

# connect to IMU
metawear_mac = 'D4:C5:36:C4:7B:78'
#metawear_mac = 'D4:C5:36:C4:7B:78'
d = MetaWear(metawear_mac)
d.connect()
print("Connected to " + d.address + " over " + ("USB" if d.usb.is_connected else "BLE"))
states =State(d)

# configure all metawears

print("Configuring device")
libmetawear.mbl_mw_settings_set_connection_parameters(states.device.board, 7.5, 7.5, 0, 6000)
sleep(1.5)

# config acc
#libmetawear.mbl_mw_acc_set_odr(s.device.board, 50.0) # Generic call
libmetawear.mbl_mw_acc_bmi160_set_odr(states.device.board, AccBmi160Odr._50Hz) # BMI 160 specific call
libmetawear.mbl_mw_acc_bosch_set_range(states.device.board, AccBoschRange._4G)
libmetawear.mbl_mw_acc_write_acceleration_config(states.device.board)

# config gyro
libmetawear.mbl_mw_gyro_bmi160_set_range(states.device.board, GyroBoschRange._1000dps);
libmetawear.mbl_mw_gyro_bmi160_set_odr(states.device.board, GyroBoschOdr._50Hz);
libmetawear.mbl_mw_gyro_bmi160_write_config(states.device.board);

# get acc signal and subscribe
acc = libmetawear.mbl_mw_acc_get_acceleration_data_signal(states.device.board)
libmetawear.mbl_mw_datasignal_subscribe(acc, None, states.accCallback)

# get gyro signal and subscribe
gyro = libmetawear.mbl_mw_gyro_bmi160_get_rotation_data_signal(states.device.board)
libmetawear.mbl_mw_datasignal_subscribe(gyro, None, states.gyroCallback)

# start acc
libmetawear.mbl_mw_acc_enable_acceleration_sampling(states.device.board)
libmetawear.mbl_mw_acc_start(states.device.board)

# start gyro
libmetawear.mbl_mw_gyro_bmi160_enable_rotation_sampling(states.device.board)
libmetawear.mbl_mw_gyro_bmi160_start(states.device.board)

# sleep 10 s
sleep(1.0)

# breakdown metawears

# stop acc
libmetawear.mbl_mw_acc_stop(states.device.board)
libmetawear.mbl_mw_acc_disable_acceleration_sampling(states.device.board)

# stop gyro
libmetawear.mbl_mw_gyro_bmi160_stop(states.device.board)
libmetawear.mbl_mw_gyro_bmi160_disable_rotation_sampling(states.device.board)

# unsubscribe acc
acc = libmetawear.mbl_mw_acc_get_acceleration_data_signal(states.device.board)
libmetawear.mbl_mw_datasignal_unsubscribe(acc)

# unsubscribe gyro
gyro = libmetawear.mbl_mw_gyro_bmi160_get_rotation_data_signal(states.device.board)
libmetawear.mbl_mw_datasignal_unsubscribe(gyro)

# disconnect
libmetawear.mbl_mw_debug_disconnect(states.device.board)

# download recap
print("Total Samples Received")
print("%s -> %d" % (states.device.address, states.samples))