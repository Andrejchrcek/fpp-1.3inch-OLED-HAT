import config
import time
import numpy as np

Device_SPI = config.Device_SPI
Device_I2C = config.Device_I2C

LCD_WIDTH   = 128 #LCD width
LCD_HEIGHT  = 64  #LCD height

class SH1106(object):
    def __init__(self):
        self.width = LCD_WIDTH
        self.height = LCD_HEIGHT
        self.RPI = config.RaspberryPi()
        self._dc = self.RPI.GPIO_DC_PIN
        # TENTO RIADOK JE ZAKOMENTOVANÝ, ABY NEPOUŽÍVAL RESET PIN
        # self._rst = self.RPI.GPIO_RST_PIN
        self.Device = self.RPI.Device

    def command(self, cmd):
        if(self.Device == Device_SPI):
            self.RPI.digital_write(self._dc,False)
            self.RPI.spi_writebyte([cmd])
        else:
            self.RPI.i2c_writebyte(0x00, cmd)

    def Init(self):
        if (self.RPI.module_init() != 0):
            return -1
        """Initialize dispaly"""
        # TENTO RIADOK JE ZAKOMENTOVANÝ, ABY NEVOLAL FUNKCIU RESET
        # self.reset()
        
        self.command(0xAE);#--turn off oled panel
        self.command(0x02);#---set low column address
        # ... (zvyšok inicializácie zostáva rovnaký) ...
        self.command(0x10);
        self.command(0x40);
        self.command(0x81);
        self.command(0xA0);
        self.command(0xC0);
        self.command(0xA6);
        self.command(0xA8);
        self.command(0x3F);
        self.command(0xD3);
        self.command(0x00);
        self.command(0xd5);
        self.command(0x80);
        self.command(0xD9);
        self.command(0xF1);
        self.command(0xDA);
        self.command(0x12);
        self.command(0xDB);
        self.command(0x40);
        self.command(0x20);
        self.command(0x02);

        self.command(0xA4);
        self.command(0xA6);
        time.sleep(0.1)
        self.command(0xAF);

    def set_contrast(self, contrast):
        self.command(0x81)
        self.command(contrast)
    
    # CELÁ FUNKCIA RESET JE ZAKOMENTOVANÁ, LEBO JE ZBYTOČNÁ A NEBEZPEČNÁ
    # def reset(self):
        # """Reset the display"""
        # self.RPI.digital_write(self._rst,True)
        # time.sleep(0.1)
        # self.RPI.digital_write(self._rst,False)
        # time.sleep(0.1)
        # self.RPI.digital_write(self._rst,True)
        # time.sleep(0.1)
    
    def getbuffer(self, image):
        buf = [0xFF] * ((self.width//8) * self.height)
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        pixels = image_monocolor.load()
        if(imwidth == self.width and imheight == self.height):
            for y in range(imheight):
                for x in range(imwidth):
                    if pixels[x, y] == 0:
                        buf[x + (y // 8) * self.width] &= ~(1 << (y % 8))
        return buf
            
    def ShowImage(self, pBuf):
        for page in range(0,8):
            self.command(0xB0 + page)
            self.command(0x02); 
            self.command(0x10); 
            if(self.Device == Device_SPI):
                self.RPI.digital_write(self._dc,True)
            for i in range(0,self.width):
                if(self.Device == Device_SPI):
                    self.RPI.spi_writebyte([~pBuf[i+self.width*page]]); 
                else :
                    self.RPI.i2c_writebyte(0x40, ~pBuf[i+self.width*page])
                        
    def clear(self):
        _buffer = [0xff]*(self.width * self.height//8)
        self.ShowImage(_buffer)
