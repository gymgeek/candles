import mpu6050, machine, neopixel, time

while 1:
    try:
        acl = mpu6050.accel()
        print("accel init");
        break
    except:
        print("accelinit iicerror")

np = neopixel.NeoPixel(machine.Pin(14), 1)
np[0] = (0, 255, 0)
np.write()
max_val = 30000
val = None
while 1:
    try:
        val = acl.get_values()
        break
    except:
        print("getval0 iicerror")

while 1:
    try:
        val = acl.get_values()
    except:
        print("getval1 iicerror")
    if abs(val["GyX"]) > max_val or abs(val["GyY"]) > max_val or abs(val["GyZ"]) > max_val:
        print("1:"+str(val["GyX"]) + " " + str(val["GyY"]) + " " + str(val["GyZ"]))
        try:
            val = acl.get_values()
        except:
            print("getval2 iicerror")
        if abs(val["GyX"]) > max_val or abs(val["GyY"]) > max_val or abs(val["GyZ"]) > max_val:
            print("2:"+str(val["GyX"]) + " " + str(val["GyY"]) + " " + str(val["GyZ"]))
            try:
                val = acl.get_values()
            except:
                print("getval3 iicerror")
            if abs(val["GyX"]) > max_val or abs(val["GyY"]) > max_val or abs(val["GyZ"]) > max_val:
                print("3:"+str(val["GyX"]) + " " + str(val["GyY"]) + " " + str(val["GyZ"]))
                try:
                    val = acl.get_values()
                except:
                    print("getval4 iicerror")
                if abs(val["GyX"]) > max_val or abs(val["GyY"]) > max_val or abs(val["GyZ"]) > max_val:
                    print("4:"+str(val["GyX"]) + " " + str(val["GyY"]) + " " + str(val["GyZ"]))
                    np[0] = (255, 0, 0)
                    np.write()
                    time.sleep(2)
                    try:
                        acl.get_values()
                    except:
                        pass
                    np[0] = (0, 255, 0)
                    np.write()
