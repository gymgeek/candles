import mpu6050, machine, neopixel, time


class Candle_sample:
    def __init__(self, acllimitval, shakeslimitcount, color):
        self.acl = None
        while 1:
            try:
                self.acl = mpu6050.accel()
                print("accel init");
                break
            except:
                print("accelinit iicerror")

        self.np = neopixel.NeoPixel(machine.Pin(14), 1)
        self.np[0] = (10, 0, 0)
        self.np.write()
        self.acllimitval = acllimitval
        self.shakeslimitcount = shakeslimitcount
        self.shakescount = 0
        self.val = None
        self.color = color

        self.vibrator = machine.Pin(12,machine.Pin.OUT)
        self.vibrator.value(0)

    def getval(self):
        while 1:
            try:
                self.val = self.acl.get_values()
                break
            except:
                print("getval0 iicerror")

    def valbeyonlimits(self):
        self.getval()
        x = self.val["GyX"]
        y = self.val["GyY"]
        z = self.val["GyZ"]

        velocity = (x**2 + y**2 + z**2)**0.5
        print("veloc:",velocity)
        if velocity > self.acllimitval:
            return True
        # if abs() > self.acllimitval or abs(self.val["GyY"]) > self.acllimitval or abs(
        #        self.val["GyZ"]) > self.acllimitval:
        #    print("1:" + str(self.val["GyX"]) + " " + str(self.val["GyY"]) + " " + str(self.val["GyZ"]))
        #    return True
        return False

    def gameover(self):
        self.np[0] = (5, 0, 0)
        self.np.write()
        self.vibrator.value(1)
        time.sleep(2)
        self.vibrator.value(0)


    def remapcol(self):
        retcol = []
        for col in self.color:
            retcol.append(int((col / self.shakeslimitcount) * (self.shakeslimitcount - self.shakescount)))
        return retcol

    def start(self):
        while 1:
            print(self.shakescount)
            if self.valbeyonlimits():
                self.shakescount += 1
            else:
                if self.shakescount > 0:
                    self.shakescount -= 1
            if self.shakescount > self.shakeslimitcount:
                self.gameover()
                self.shakescount = 0

            self.np[0] = self.remapcol()
            self.np.write()


candle = Candle_sample(5000, 10, [255, 50, 0])
