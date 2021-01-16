import matplotlib.pyplot as plt
import json
file=open("data.txt", "r")
lines=file.readlines()
Room1={"temp":[], "hum":[], "time":[], "air":[]}
Room2={"temp":[], "hum":[], "time":[], "air":[]}
Room3={"temp":[], "hum":[], "time":[]}
for line_raw in lines:
    line=json.loads(line_raw)
    Room1["temp"].extend(line["Living room 1"]["temperature"])
    Room1["hum"].extend(line["Living room 1"]["humidity"])
    Room1["time"].extend(line["Living room 1"]["time"])
    Room1["air"].extend(line["Living room 1"]["air"])
    
    Room2["temp"].extend(line["Living room 2"]["temperature"])
    Room2["hum"].extend(line["Living room 2"]["humidity"])
    Room2["time"].extend(line["Living room 2"]["time"])
    Room2["air"].extend(line["Living room 2"]["air"])
    
    Room3["temp"].extend(line["Storage"]["temperature"])
    Room3["hum"].extend(line["Storage"]["humidity"])
    Room3["time"].extend(line["Storage"]["time"])
    
plt.plot(Room1["time"], Room1["temp"], label="Room1 Temperature")
plt.plot(Room1["time"], Room1["hum"], label="Room1 Humidity")
plt.plot(Room1["time"], Room1["air"], label="Room1 Air")

plt.plot(Room2["time"], Room2["temp"], label="Room2 Temperature")
plt.plot(Room2["time"], Room2["hum"], label="Room2 Humidity")
plt.plot(Room2["time"], Room2["air"], label="Room2 Air")

plt.plot(Room3["time"], Room3["temp"], label="Room3 Temperature")
plt.plot(Room3["time"], Room3["hum"], label="Room3 Humidity")

plt.legend()
plt.show()



