import mpu6050, machine, neopixel, time
import codes
import socket


class Candle_client:
    def __init__(self, server_ip, acllimitval, shakeslimitcount, color,port=2260):
        self.acl = None
        while 1:
            try:
                self.acl = mpu6050.accel()
                print("accel init")
                break
            except:
                print("accelinit iicerror")

        self.np = neopixel.NeoPixel(machine.Pin(14), 1)
        self.np[0] = (10, 0, 0)
        self.np.write()
        self.ip = server_ip
        self.port= port
        self.acllimitval = acllimitval
        self.shakeslimitcount = shakeslimitcount
        self.shakescount = 0
        self.val = None
        self.color = color

        self.gravity = 16900
        self.last_magnitude = 0

        self.vibrator = machine.Pin(12,machine.Pin.OUT)
        self.vibrator.value(0)

        self.np[0] = (0,0,255)
        self.np.write()
        time.sleep(0.5)
        self.server_socket=socket.socket()
        starttime = time.time()

        self.started = 99999999
        
        while 1:
            self.np.write()
            try:
                self.server_socket.connect((self.ip, self.port))
                self.np[0] = (0,255,0)
                print("connected")
                self.np.write()
                self.server_socket.setblocking(0)
                break
            except:
                self.np[0] = (255,0,0)
                time.sleep(2)
            if starttime + 5 < time.time():
                self.started = time.time()
                break

        self.np.write()

    def getval(self):
        while 1:
            try:
                self.val = self.acl.get_values()
                self.val["AcY"] += self.gravity
                break
            except:
                #print("getval0 iicerror")
                pass

    def valbeyonlimits(self):
        self.getval()

        magnitude = (self.val["AcX"] ** 2 + self.val["AcY"] ** 2 + self.val["AcZ"] ** 2) ** 0.5

        change = abs(magnitude - self.last_magnitude)

        self.last_magnitude = magnitude


#        jerk = ((x - last_x)**2 + (y - last_y)**2 + (z - last_z)**2)**0.5

        print("change:",change)

        if change > self.acllimitval:
            return True
        return False

    def gameover(self):
        try:
            self.server_socket.send(codes.byte_lost)
        except:
            pass
        # fail silenty
        # like a ninja    


    def remapcol(self):

        retcol = []
        multiplier = (1 - (self.shakescount / self.shakeslimitcount)) ** 4
        if multiplier < 0:
            multiplier = 0

        for col in self.color:
            retcol.append(int(col * multiplier))

        return retcol

    def start(self):
        self.server_socket.setblocking(0)
        self.getval()
        self.last_acceleration = self.val

        while 1:
            
            received = None
            try:
                
                received = self.server_socket.recv(1)
                print("received: ",received)
            except:
                pass

            if received == codes.byte_red:
                print("red")
                self.np[0] = (255,0,0)
            elif received == codes.byte_orange:
                print("orange")
                self.np[0] = (255,55,0)
            elif received == codes.byte_green:
                print("green")
                self.np[0] = (0,255,0)
                self.vibrator.value(1)
            elif received == codes.byte_start:
                print("start")
                self.np[0] = (0,0,255)
                self.vibrator.value(0)
                self.started = time.time()
            elif received == codes.byte_win:
                print("win")
                while 1:
                    self.vibrator.value(1)
                    self.np[0] = (255,255,255)
                    self.np.write()
                    time.sleep(0.2)
                    self.np[0] = (0,0,255)
                    self.np.write()
                    time.sleep(0.2)
                    self.np[0] = (0,255,0)
                    self.np.write()
                    time.sleep(0.2)
                    self.np[0] = (255,0,0)
                    self.np.write()
                    time.sleep(0.2)
            elif received == codes.byte_lost:
                print("lost")
                while 1:
                    self.vibrator.value(1)
                    self.np[0] = (255,0,0)
                    self.np.write()
                    time.sleep(1)
                    self.np[0] = (0,0,0)
                    self.np.write()
                    time.sleep(0.5)
                    
            else:
                if self.started < time.time():
                    self.np[0] = self.remapcol()

            self.np.write()
            
            #print(self.shakescount)
            if self.valbeyonlimits():
                self.shakescount += 1
            else:
                if self.shakescount > 0:
                    self.shakescount -= 1


            print(self.shakescount)

            if self.shakescount > self.shakeslimitcount:
                self.gameover()
                self.shakescount = 0


            



