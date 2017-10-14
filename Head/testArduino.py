import serial
ser = serial.Serial('/dev/ttyACM0', 9600)
while 1 :
    msg = ser.readline()
    print msg