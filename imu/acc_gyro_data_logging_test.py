import time
from pymetawear.discover import select_device
from pymetawear.client import MetaWearClient

address = 'D4:C5:36:C4:7B:78'
c = MetaWearClient(str(address), debug=True)
print("New client created: {0}".format(c))


def acc_callback(data):
    """Handle a (epoch, (x,y,z)) accelerometer tuple."""
    print("Acc:",data) # [{0}] - X: {1}, Y: {2}, Z: {3}".format(data[0], *data[1]))

def gyro_callback(data):
    """Handle a (epoch, (x,y,z)) gyroscope tuple."""
    print("gyro:",data) # [{0}] - X: {1}, Y: {2}, Z: {3}".format(data[0], *data[1]))

print("Write gyroscope settings...")
c.gyroscope.set_settings(data_rate=50.0, data_range=1000.0)
print("Write accelerometer settings...")
c.accelerometer.set_settings(data_rate=50.0, data_range=4.0)

print("Subscribing to gyroscope signal notifications...")
c.gyroscope.notifications(gyro_callback)
print("Subscribing to accelerometer signal notifications...")
c.accelerometer.high_frequency_stream = False
c.accelerometer.notifications(acc_callback)

time.sleep(5.0)

print("Unsubscribe to notification...")
c.gyroscope.notifications(None)
c.accelerometer.notifications(None)

time.sleep(5.0)

c.disconnect()