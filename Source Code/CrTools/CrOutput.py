# Created by Aleksey Gilenko
# December 2020

try:
    import matplotlib.pyplot as plt
    import time
    import RPLCD
    import RPi.GPIO as GPIO
    from RPLCD import cleared, cursor
except ImportError:
    dependencies = ["matplotlib.pyplot as plt", "time", "RPLCD", "RPi.GPIO as GPIO"]
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
        print("Try download or reinstall them and again after")

class Plotter():
    def __init__(self):
        pass
    def draw_graph(self, file):
        pass
class LCD3:
    def __init__(self, rs, e, db4, db5, db6, db7):
        self.lcd = RPLCD.CharLCD(cols=16, numbering_mode=GPIO.BCM, rows=2, pin_rs=18, pin_e=23, pins_data=[24,25,8,7])
        self.lcd.cursor_pos = 
        (0, 0) 
        self.lcd.write_string('Initialization..')
        time.sleep(2)
        self.lcd.clear()
        time.sleep(0.5)
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string(u'Calibration       in progress...')
        #self.unichr=self.lcd.unichr
        
    def clear(self):
        self.lcd.clear()
    def st(self):
        self.lcd.clear()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string('Temp:')
        self.lcd.cursor_pos = (1, 1)
        self.lcd.write_string('Hum:')
        self.lcd.cursor_pos = (0, 7)
        self.lcd.write_string('C')
        self.lcd.cursor_pos = (1, 7)
        self.lcd.write_string('%')
        self.lcd.cursor_pos = (0, 11)
        self.lcd.write_string('C')
        self.lcd.cursor_pos = (1, 11)
        self.lcd.write_string('%')
        self.lcd.cursor_pos = (0, 15)
        self.lcd.write_string('C')
        self.lcd.cursor_pos = (1, 15)
        self.lcd.write_string('%')
    def write(self, data):
        if "Living room 1" in list(data.keys()):
            self.lcd.cursor_pos = (0, 5)
            self.lcd.write_string(str(int(data["Living room 1"]["temperature"])))
            self.lcd.cursor_pos = (1, 5)
            self.lcd.write_string(str(int(data["Living room 1"]["humidity"])))
        if "Living room 2" in list(data.keys()):
            self.lcd.cursor_pos = (0, 9)
            self.lcd.write_string(str(int(data["Living room 2"]["temperature"])))
            self.lcd.cursor_pos = (1, 9)
            self.lcd.write_string(str(int(data["Living room 2"]["humidity"])))
        if "Storage" in list(data.keys()):
            self.lcd.cursor_pos = (0, 13)
            self.lcd.write_string(str(int(data["Storage"]["temperature"])))
            self.lcd.cursor_pos = (1, 13)
            self.lcd.write_string(str(int(data["Storage"]["humidity"])))
class Plotter3:
    def __init__(self):
        
        self.ax = plt.subplot(1, 3, 1)
        #self.ax.title("Living Room 1")
        self.bx = plt.subplot(1, 3, 2)
        #self.bx.title("Living Room 2")
        self.cx = plt.subplot(1, 3, 3)
        self.ax.set_xlim(time.time()-2, time.time()+55)
        self.ax.set_ylim(-10, 100)
        self.R1T,=self.ax.plot(0,0, label="Temnperature")
        self.R1H,=self.ax.plot(0,0, label="Humidity")
        self.R1A,=self.ax.plot(0,0, label="Air")
        self.ax.legend()
        self.ax.set_title("Living room 1")
        self.bx.set_xlim(time.time()-2, time.time()+55)
        self.bx.set_ylim(-10, 100)
        self.R2T,=self.bx.plot(0,0, label="Temnperature")
        self.R2H,=self.bx.plot(0,0, label="Humidity")
        self.R2A,=self.bx.plot(0,0, label="Air")
        self.bx.legend()
        self.bx.set_title("Living room 2")
        self.cx.set_xlim(time.time()-2, time.time()+55)
        self.cx.set_ylim(-10, 100)
        self.R3T,=self.cx.plot(0,0, label="Temnperature")
        self.R3H,=self.cx.plot(0,0, label="Humidity")
        self.cx.legend()
        self.cx.set_title("Storage")
        #self.cx.title("Storage")
        # plt.ion()
        # self.R1={"temp":[], "hum":[], "time":[], "air":[]}
        # self.R2={"temp":[], "hum":[], "time":[], "air":[]}
        # self.R3={"temp":[], "hum":[], "time":[]}



    def update_from_dict(self, data):
        self.R1T.set_data(data["Living room 1"]["time"], data["Living room 1"]["temperature"])
        self.R1H.set_data(data["Living room 1"]["time"], data["Living room 1"]["humidity"])
        self.R1A.set_data(data["Living room 1"]["time"], data["Living room 1"]["air"])
        self.R2T.set_data(data["Living room 2"]["time"], data["Living room 2"]["temperature"])
        self.R2H.set_data(data["Living room 2"]["time"], data["Living room 2"]["humidity"])
        self.R2A.set_data(data["Living room 2"]["time"], data["Living room 2"]["air"])
        self.R3T.set_data(data["Storage"]["time"], data["Storage"]["temperature"])
        self.R3H.set_data(data["Storage"]["time"], data["Storage"]["humidity"])
        plt.pause(0.05)
    def clean(self, stime):
        self.ax.set_xlim(stime-2, stime+55)
        self.ax.set_ylim(-10, 100)
        self.bx.set_xlim(stime-2, stime+55)
        self.bx.set_ylim(-10, 100)
        self.cx.set_xlim(stime-2, stime+55)
        self.cx.set_ylim(-10, 100)
        
        pass
