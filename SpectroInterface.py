import serial
from time import sleep

class SpectroInterface(object):
    def __init__(self):
        self.ser = serial.Serial()
        self.ser.baudrate = 115200
        # Note this is for linux
        # self.ser.port = "COM4" # for Windows assuming arduino is connected on COM4
        self.ser.port = "/dev/ttyUSB0"
        self.ser.open()

    def get_spectrometer_data(self):
        if(not self.ser.isOpen()):
            self.ser.open()
        response = self.ser.write(b'c')
        if(response):
            result = self.ser.readline()
            d_o = list(map(lambda i: int(i), result.decode('ascii').split(',')[:-1]))
            return(d_o)

    def laser_on(self):
        if(not self.ser.isOpen()):
            self.ser.open()
        response = self.ser.write(b'a')
        return(response)

    def laser_off(self):
        if(not self.ser.isOpen()):
            self.ser.open()
        response = self.ser.write(b'o')
        return(response)

    def led_on(self):
        if(not self.ser.isOpen()):
            self.ser.open()
        response = self.ser.write(b'e')
        return(response)

    def led_off(self):
        if(not self.ser.isOpen()):
            self.ser.open()
        response = self.ser.write(b'r')
        return(response)

    def get_normal_data(self):
        result = self.get_spectrometer_data()
        return(result)

    def get_laser_data(self):
        self.laser_on()
        result = self.get_spectrometer_data()
        self.laser_off()
        return(result)

    def get_led_data(self):
        self.led_on()
        result = self.get_spectrometer_data()
        self.led_off()
        return(result)

