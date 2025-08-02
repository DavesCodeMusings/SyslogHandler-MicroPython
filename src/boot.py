from network import WLAN, STA_IF
from time import ticks_diff, ticks_ms
from config import WIFI_NAME, WIFI_PASS, WIFI_TIMEOUT

wlan = WLAN(STA_IF)
wlan.active(True)
print(f"Connecting to SSID {WIFI_NAME}...", end='')
wlan.connect(WIFI_NAME, WIFI_PASS)
start_time = ticks_ms()
while not wlan.isconnected():
    if (ticks_diff(ticks_ms(), start_time) > WIFI_TIMEOUT * 1000):
        print(".", end='')
if (wlan.isconnected()):
    print(f"\n{wlan.ifconfig()[0]}")
else:
    print("Timed out.")
