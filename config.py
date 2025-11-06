# -*- coding:utf-8 -*-

import time
# import spidev  <-- ZMAZANÉ
from gpiozero import DigitalOutputDevice, DigitalInputDevice
from smbus import SMBus

# --- Pin definition ZMAZANÉ ---
# (RST, DC, CS, BL piny boli len pre SPI)

# SPI device <-- ZMAZANÉ
Device_I2C = 1

class RaspberryPi:
    # --- __init__ zjednodušený len pre I2C ---
    def __init__(self, i2c=SMBus(1)):
        self.INPUT = False
        self.OUTPUT = True
        self.np = None
        self.i2c = i2c
        self.Device = Device_I2C
        
        # --- TOTO BOL PROBLÉM, JE TO PREČ ---
        # self.GPIO_DC_PIN = self.gpio_mode(DC_PIN, self.OUTPUT)
        
    def digital_write(self, pin, value):
        if value:
            pin.on()
        else:
            pin.off()

    def digital_read(self, pin):
        return pin.value

    def delay_ms(self, delaytime):
        time.sleep(delaytime / 1000.0)

    # --- spi_writebyte ZMAZANÉ ---

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

    # --- module_init zjednodušený len pre I2C ---
    def module_init(self):
        self.address = 0x3c
        return 0

    # --- module_exit zjednodušený len pre I2C ---
    def module_exit(self):
        # self.digital_write(self.GPIO_DC_PIN,False) <-- ZMAZANÉ (lebo DC pin neexistuje)
        self.i2c.close()
