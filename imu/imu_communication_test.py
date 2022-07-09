# pymetawear

from pymetawear.client import MetaWearClient
RE = MetaWearClient('D4:C5:36:C4:7B:78')
# LE = ('D3:FE:9A:01:90:57')

pattern = RE.led.load_preset_pattern('blink', repeat_count=10)
RE.led.write_pattern(pattern, 'g')
RE.led.play()