# Created by Aleksey Gilenko
# December 2020

import sys
try:
    from .CrErrors import PackagesNotInstalledError
except:
    raise BaseException
try:
    import Adafruit_DHT
    import Adafruit_MCP3008
    import matplotlib.pyplot as plt
    import time
except ImportError:
    dependencies = ["Adafruit_DHT","Adafruit_MCP3008","matplotlib.pyplot as plt","time","datetime", "json"]
    notimported=[]
    for library in dependencies:

        try:
            exec ("import "+str(library))
        except ImportError:
            notimported.append(library.split()[0])
        except Exception:
            print("Unknown error")

    if len(notimported)!=0:
        print("Issues with importing following libraries:\n")
        for i in notimported:
            print("    - "+i+"\n")
        print("Try download or reinstall them.")
        raise PackagesNotInstalledError
        sys.exit()


class DHT:

    def __init__(self, pin, type, start_time, avg_arr_size):
        #self.name=str("DHT11 on")
        self.pin=pin
        self.start_time=start_time
        self.avg_arr_size=avg_arr_size
        self.avg_t=[]
        self.avg_h=[]
        self.type=type
        self.temperature=0
        self.humidity=0

    def get_filtered(self):
        temp_humidity, temp_temperature = self.humidity, self.temperature
        self.humidity_raw, self.temperature_raw = Adafruit_DHT.read_retry(self.type, self.pin)
        self.time=time.time()-self.start_time

        if self.humidity_raw is not None and self.temperature_raw is not None and ((self.humidity_raw <100 and (abs(self.temperature_raw-temp_temperature)<=20) or len(self.avg_t)==0)):

            if(len(self.avg_h)<self.avg_arr_size-1):
                self.avg_h.append(self.humidity_raw)
                self.avg_t.append(self.temperature_raw)
                self.temperature=self.temperature_raw
                self.humidity=self.humidity_raw
            else:
                sum_t=self.temperature_raw
                sum_h=self.humidity_raw
                for j in self.avg_h:
                    sum_h+=j
                for j in self.avg_t:
                    sum_t+=j
                self.humidity=(sum_h/self.avg_arr_size)
                self.temperature=(sum_t/self.avg_arr_size)
                self.avg_h.append(self.humidity_raw)
                self.avg_t.append(self.temperature_raw)
                self.avg_h.pop(0)
                self.avg_t.pop(0)
            return {"temperature":self.temperature, "humidity":self.humidity, "time": self.time}

        else:
            self.temperature=temp_temperature
            self.humidity=temp_humidity
            return {"temperature":self.temperature, "humidity":self.humidity, "time": self.time}


    def get_raw(self):
        self.humidity, self.temperature = Adafruit_DHT.read_retry(self.type, self.pin)
        self.time=time.time()-self.start_time
        if self.humidity is not None and self.temperature is not None:
            return {"temperature":self.temperature, "humidity":self.humidity, "time": self.time}

        else:
            return {"temperature":0, "humidity":0, "time": self.time}


class MCP3008:
    def __init__(self, CLK, MISO, MOSI, CS):
        # self.CLK  = CLK 
        # self.MISO = MISO 
        # self.MOSI = MOSI 
        # self.CS   = CS
        self.mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
    def read_channel(self, channel):
        return self.mcp.read_adc(channel)



class MQ2:
    def __init__(self, MCP3008, channel, start_time, avg_arr_size):
        self.MCP=MCP3008
        self.channel=channel
        self.start_time=start_time
        self.avg_a=[]
        self.avg_arr_size=avg_arr_size
        self.air=0

    def get_filtered(self):
        self.air=self.MCP.read_channel(self.channel)
        if(len(self.avg_a)<self.avg_arr_size-1):
            self.avg_a.append(self.air)

        else:
            sum_a=self.air
            for j in self.avg_a:
                sum_a+=j
            self.air=(sum_a/self.avg_arr_size)
            self.avg_a.append(self.air)
            self.avg_a.pop(0)
        return {"air": self.air/10}
    def get_raw(self):
        return {"air": self.MCP.read_channel(self.channel)/10}



class Group:
    def __init__(self, name, sensors):
        self.name=name
        self.data={}
        self.sensors=sensors

    def get_filtered(self):
        self.data={}
        for sensor in self.sensors:        
            self.data.update(sensor.get_filtered())
        return self.data

    def get_raw(self):
        self.data={}
        for sensor in self.sensors:        
            self.data.update(sensor.get_raw())
        return self.data




