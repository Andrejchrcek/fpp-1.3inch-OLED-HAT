# -*- coding:utf-8 -*-

import time
import spidev
from gpiozero import DigitalOutputDevice, DigitalInputDevice
from smbus import SMBus

# Pin definition
RST_PIN         = 25
DC_PIN          = 24
CS_PIN          = 8
BL_PIN          = 18

# SPI device, bus = 0, device = 0
Device_SPI = 0
Device_I2C = 1

class RaspberryPi:
    def __init__(self, spi=spidev.SpiDev(0,0), i2c=SMBus(1), spi_speed=10000000):
        self.INPUT = False
        self.OUTPUT = True
        self.np = None
        self.RST_PIN = RST_PIN
        self.DC_PIN = DC_PIN
        self.CS_PIN = CS_PIN
        self.BL_PIN = BL_PIN
        self.SPEED = spi_speed
        self.spi = spi
        self.i2c = i2c
        self.Device = Device_I2C
        
    def digital_write(self, pin, value):
        if value:
            pin.on()
        else:
            pin.off()

    def digital_read(self, pin):
        return pin.value

    def delay_ms(self, delaytime):
        time.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        self.spi.writebytes(data)

    def i2c_writebyte(self, reg, value):
        self.i2c.write_byte_data(self.address, reg, value)

    def gpio_mode(self, Pin, Mode, pull_up_down=None, active_state=True):
        if Mode:
            return DigitalOutputDevice(Pin, active_high=True, initial_value=False)
        else:
            if pull_up_down == 'pull_up':
                return DigitalInputDevice(Pin, pull_up=True, active_state=active_state)
            else:
                return DigitalInputDevice(Pin, pull_up=False, active_state=active_state)

    def module_init(self):
        if self.Device == Device_SPI:
            self.spi.max_speed_hz = self.SPEED
            self.spi.mode = 0b00
            
            # TENTO RIADOK JE ZAKOMENTOVANÝ, ABY ZNOVA NEOVLÁDAL RESET PIN
            # self.GPIO_RST_PIN = self.gpio_mode(RST_PIN,self.OUTPUT)
            
            self.GPIO_DC_PIN = self.gpio_mode(DC_PIN,self.OUTPUT)
            self.GPIO_CS_PIN = self.gpio_mode(CS_PIN,self.OUTPUT)
            self.GPIO_BL_PIN = self.gpio_mode(BL_PIN,self.OUTPUT)
            self.digital_write(self.GPIO_CS_PIN,True)
            self.digital_write(self.GPIO_DC_PIN,True)
            return 0
        else:
            self.address = 0x3c
            
            # TENTO RIADOK JE ZAKOMENTOVANÝ, ABY ZNOVA NEOVLÁDAL RESET PIN
            # self.GPIO_RST_PIN = self.gpio_mode(RST_PIN,self.OUTPUT)
            
            self.GPIO_DC_PIN = self.gpio_mode(DC_PIN,self.OUTPUT)
            return 0

    def module_exit(self):
        if self.Device == Device_SPI:
            
            # TENTO RIADOK JE TIEŽ ZAKOMENTOVANÝ
            # self.digital_write(self.GPIO_RST_PIN,False)
            
            self.digital_write(self.GPIO_DC_PIN,False)
            self.spi.close()
        else:
            
            # A AJ TENTO POSLEDNÝ RIADOK S RESET PINOM
            # self.digital_write(self.GPIO_RST_PIN,False)
            
            self.digital_write(self.GPIO_DC_PIN,False)
            self.i2c.close()
