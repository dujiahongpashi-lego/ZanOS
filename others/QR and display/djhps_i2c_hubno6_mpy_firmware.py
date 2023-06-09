from machine import Pin
import time

class DJHPS_SoftI2C:
    def tick(self,anz):
        pass
        #time.sleep_us(anz*self.int_clk) 

    def __init__(self,SDAPIN,SCLPIN,bitrate = 3200):
        print('DJHPS SoftI2C Init.')
        if(SDAPIN != SCLPIN):
            self.SCL = SCLPIN
            self.SDA = SDAPIN

        else:
            print ("SDA = GPIO"+str(self.SDA)+"  SCL = GPIO"+str(self.SCL))

        #configer SCL
        self.SCL.value(1)
        self.SDA.value(1)

        if bitrate == 100: # TODO 目前设置波特率功能不生效。只能全速
            self.int_clk = 0.0000025
        elif bitrate == 400:
            self.int_clk = 0.000000625
        elif bitrate == 1000:
            self.int_clk = 1
        elif bitrate == 3200:
            self.int_clk = 1
        
        print('DJHPS SoftI2C set CLK as', self.int_clk)

    def Start(self):
        #SCL
        #  ______
        #  |     |______
        #SDA
        #  ___
        #  |  |_________

        self.SDA.init(self.SDA.OUT) #cnfigure SDA as output

        self.SDA.value(1)
        self.SCL.value(1)
        #self.tick(1)
        self.SDA.value(0)
        #self.tick(1)
        self.SCL.value(0)
        #self.tick(2)


    def ReadAck(self):
        self.SDA.init(self.SDA.IN)
        readbuffer =0
        for i in range(8):
            self.SCL.value(1)
            #self.tick(2)
            readbuffer |= (self.SDA.value()<< 7) >> i
            self.SCL.value(0)
            #self.tick(2)

        self.SDA.init(self.SDA.OUT)
        self.SDA.value(0)
        self.SCL.value(1)
        #self.tick(2)
        self.SCL.value(0)
        self.SDA.value(0)
        #self.tick(2)
        return readbuffer

    def ReadNack(self):
        self.SDA.init(self.SDA.IN)
        readbuffer =0
        for i in range(8):
            self.SCL.value(1)
            #self.tick(2)
            readbuffer |= (self.SDA.value()<< 7) >> i
            self.SCL.value(0)
            #self.tick(2)

        self.SDA.init(self.SDA.OUT)
        self.SDA.value(1)
        self.SCL.value(1)
        #self.tick(2)
        self.SCL.value(0)
        self.SDA.value(0)
        #self.tick(2)
        return readbuffer

    def WriteByte(self,byte):
        if byte > 0xff:
            return -1
        #print byte
        self.SDA.init(self.SDA.OUT)
        for i in range(8):
            #MSB First
            if (byte << i) & 0x80 == 0x80:
                self.SDA.value(1)
                self.SCL.value(1)
                #self.tick(2)
                self.SCL.value(0)
                self.SDA.value(0)
                #self.tick(2)
            else:
                self.SDA.value(0)
                self.SCL.value(1)
                #self.tick(2)
                self.SCL.value(0)
                #self.tick(2)

        self.SDA.init(self.SDA.IN)
        self.SCL.value(1)
        ##self.tick(1)
        #Get The ACK
        #if self.SDA.value():
        #    print("ACK")
        #else:
        #    print("NACK")
        #self.tick(2)
        self.SCL.value(0)
        #self.tick(2)


    def Stop(self):
        #SCL
        #  _____________
        #  |
        #SDA
        #     __________
        #   __|
        self.SDA.init(self.SDA.OUT) #cnfigure SDA as output

        self.SDA.value(0)
        self.SCL.value(1)
        #self.tick(1)
        self.SDA.value(1)
        #self.tick(3)
        
    def writeto(self, addr, buf):
        self.writevto(addr, buf)
        
    def writevto(self, addr, vector):
        self.Start()
        self.WriteByte(addr << 1) # 7位addr + R/W# 设0 -- writemode
        for e in vector:
            if type(e) == int:
                self.WriteByte(e)
            elif type(e) == bytes:
                self.WriteByte(int.from_bytes(e,'big'))
            elif type(e) == bytearray:
                for oneByte in e:
                    self.WriteByte(oneByte)
        self.Stop()

