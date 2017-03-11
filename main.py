import network, time
import neopixel, machine
np = neopixel.NeoPixel(machine.Pin(14), 1)

np[0] = (50,50,50)
np.write()

time.sleep(3)
np[0] = (255,255,255)
np.write()

w0 = network.WLAN(0)
stime = time.time()
while 1:
    w0.connect("GymGeek","Python27")
    time.sleep(1)
    if w0.isconnected():
        print("connected")
        break
    if stime + 15 < time.time():
        break

from candle_client import *

candle = Candle_client("172.16.34.50",15000, 10, [255, 50, 0])
candle.start()
