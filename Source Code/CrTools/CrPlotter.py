# Created by Aleksey Gilenko
# December 2020

try:
    import matplotlib.pyplot as plt
    import time
except ImportError:
    dependencies = ["matplotlib.pyplot as plt", "time"]
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


##TODO Create a universal class, that creates up to 9 plots
# class Interactive_Plotter:
#     def __init__(self, rooms):
#         pass
#         rooms_count=len(rooms)
#         self.rooms=rooms
#         self.size_x=1
#         self.size_y=1
#         if rooms_count==2:
#             self.size_x=2
#             self.size_y=1
#         elif rooms_count==3:
#             self.size_x=3
#             self.size_y=1
#         elif rooms_count==4:
#             self.size_x=2
#             self.size_y=2
#         elif 6>=rooms_count>4:
#             self.size_x=3
#             self.size_y=2
#         else:
#             self.size_y=3
#             self.size_x=3

#         for room_index in range(len(rooms)):
#             eval("self."+str(rooms[room_index].name)+"=plt.subplot("+str(size_y)+", "+str(size_x)+", "+str(room_index+1))
#             eval("self."+str(rooms[room_index].name)+".title("+str(rooms[room_index].name)+")")
#             for sensor_index in range(len(rooms[room_index])):
#                 pass
