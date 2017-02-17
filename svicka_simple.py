import mpu6050, machine, neopixel, time


class Candle_simple:
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

    def getval(self):
        while 1:
            try:
                self.val = self.acl.get_values()
                break
            except:
                print("getval0 iicerror")

    def valbeyonlimits(self):
        self.getval()
        if abs(self.val["GyX"]) > self.acllimitval or abs(self.val["GyY"]) > self.acllimitval or abs(
                self.val["GyZ"]) > self.acllimitval:
            print("1:" + str(self.val["GyX"]) + " " + str(self.val["GyY"]) + " " + str(self.val["GyZ"]))
            return True
        return False

    def gameover(self):
        self.np[0] = (20, 0, 0)
        self.np.write()
        time.sleep(2)
        # todo vibrate


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


candle = Candle_simple(5000, 10, [255, 50, 0])
