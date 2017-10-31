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
                self.__serial = serial.Serial(result[1], 9600, timeout=0.050)
                break

            result = commands.getstatusoutput('ls /dev/ttyACM*')
            if (result[0] == 0):
                self.__serial = serial.Serial(result[1], 9600, timeout=0.050)
                break

    def sendMessage(self, msg):
        self.__serial.write(msg + "\r\n")
        
    def sendMessage(self, msg):
        self.__serial.write(msg + "\r\n")

    def readMessage(self):
        return self.__serial.readline()

    def inWaiting(self):
	return self.__serial.in_waiting

