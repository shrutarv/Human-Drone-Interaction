import time

from pymetawear.client import MetaWearClient
from pymetawear.exceptions import PyMetaWearException, PyMetaWearDownloadTimeout
RE = 'D4:C5:36:C4:7B:78'
LE = 'D3:FE:9A:01:90:57'
c = MetaWearClient(LE)

# Set data rate to 50 Hz and measuring range to +/- 8g
c.accelerometer.set_settings(data_rate=50.0, data_range=8)

# Log data for 2 seconds.
c.accelerometer.start_logging()
print("Logging accelerometer data...")

time.sleep(2.0)

c.accelerometer.stop_logging()
print("Finished logging.")

#%%

# Download the stored data from the MetaWear board.
print("Downloading data...")
download_done = False
n = 0
data = None
while (not download_done) and n < 3:
    try:
        data = c.accelerometer.download_log()
        download_done = True
    except PyMetaWearDownloadTimeout:
        print("Download of log interrupted. Trying to reconnect...")
        c.disconnect()
        c.connect()
        n += 1
if data is None:
    raise PyMetaWearException("Download of logging data failed.")

print("Disconnecting...")
c.disconnect()