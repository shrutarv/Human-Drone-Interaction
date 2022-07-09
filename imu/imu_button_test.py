from pymetawear.client import MetaWearClient
RE = MetaWearClient('D4:C5:36:C4:7B:78')

def switch_callback(data):
    """Handle a switch status integer (1 for pressed, 0 for released.)."""
    if data['value'] == 1:
        print("Switch pressed!")
    elif data['value'] == 0:
        print("Switch released!")

# Enable notifications and register a callback for them.
RE.switch.notifications(switch_callback)

while True:
    # press ctrl+c to interrupt program
    pass