import commands
import serial
import socket

class Serial:
    def __init__(self):
        self.__waitForSerial()

    def __waitForSerial(self):
        while (1):
            result = commands.getstatusoutput('ls /dev/ttyUSB*')
            if (result[0] == 0):
                self.__serial = serial.Serial(result[1], 115200, timeout=0.050)
                break

            result = commands.getstatusoutput('ls /dev/ttyACM*')
            if (result[0] == 0):
                self.__serial = serial.Serial(result[1], 115200, timeout=0.050)
                break

    def sendMessage(self, msg):
        self.__serial.write(msg + "\r\n")
        while (1):
            data = self.__serial.readline()
            if (data == ''): self.__serial.write(msg + "\r\n")
            else: return data
