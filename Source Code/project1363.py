# Import of neccessary libraries
import sys # System library
import RPi.GPIO as GPIO # Input/Output library

try:
    from CrTools.CrAlert import Alert_System # Unique alert system library
    from CrTools.CrErrors import PackagesNotInstalledError # library with custom errors
    from CrTools.CrSensors import DHT, MCP3008, MQ2, Group # Unique classes for sensors and organisation
    from CrTools.CrFiles import Writer # Unique class for logging and data saving
    from CrTools.CrOutput import Plotter3, LCD3 # Unique classes for showing data on screens
    import time # built-in library for working with real time

except ImportError:
    from .CrTools.CrAlert import Alert_System # Unique alert system library
    from .CrTools.CrErrors import PackagesNotInstalledError # library with custom errors
    from .CrTools.CrSensors import DHT, MCP3008, MQ2, Group # Unique classes for sensors and organisation
    from .CrTools.CrFiles import  Writer # Unique class for logging and data saving
    from .CrTools.CrOutput import Plotter3, LCD3 # Unique classes for showing data on screens

except PackagesNotInstalledError: # If some packages are missing
    sys.exit(1)

except BaseException: # Unexpexted error
    print("Error!!!")
    sys.exit(1)


##########################  SETUP #################################

writer=Writer("data.txt", "log.txt") # creating a writer
writer.write_message("Initialization...")

#####           Variables initialization                      #####


#                       ISO Bus pins                              #
CLK = 11
MISO = 9
MOSI = 10
CS = 22


#             Pins that sensors are connected to                  #
DHT11_1=4
DHT11_2=17
DHT11_3=27


#               Pins that LCD is connected to                     #
LCD_E=23
LCD_RS=18
LCD_DB4=24
LCD_DB5=25
LCD_DB6=8
LCD_DB7=7


#    Pins that simple periferial devices are connected to         #
buzzer_pin=5 # Buzzer pin
button_pin=6 # Button pin
led1=16 # Red led pin 1
led2=20 # Red led pin 2
led3=21 # Red led pin 3
led4=13 # Green led pin 1 
led5=19 # Green led pin 2
led6=26 # Green led pin 3


#                     System variables                            #
max_size_arr=10 # Max length of filtering array
start_time=0 # Start time
operation_number=1 # Operation number


#####                devices' Initialization                  #####
alert_sys=Alert_System(buzzer_pin, [led1,  led2, led3, led4, led5, led6], button_pin) # Initialization of Alert System
lcd=LCD3(LCD_RS, LCD_E, LCD_DB4, LCD_DB5, LCD_DB6, LCD_DB7) # Initialization of LCD
DHT11_1=DHT(DHT11_1, 11, start_time, max_size_arr) # Initialization of three DHT11
DHT11_2=DHT(DHT11_2, 11, start_time, max_size_arr)
DHT11_3=DHT(DHT11_3, 11, start_time, max_size_arr)
mcp=MCP3008(CLK, MISO, MOSI, CS) # Initialization of Analog-Digital converter 
MQ2_1=MQ2(mcp, 0, start_time, max_size_arr) # Initialization of two air sensors
MQ2_2=MQ2(mcp, 2, start_time, max_size_arr)

grp1=Group("Living room 1", [DHT11_1, MQ2_1]) # Grouping sensors for easy managment
grp2=Group("Living room 2", [DHT11_2, MQ2_2])
grp3=Group("Storage", [DHT11_3])
groups=[grp1, grp2, grp3]

sensors_data={
              grp1.name:{"temperature":[], "humidity":[],"air":[],"time":[]},
              grp2.name:{"temperature":[], "humidity":[],"air":[],"time":[]},
              grp3.name:{"temperature":[], "humidity":[],"air":[],"time":[]},
              }
plotter=Plotter3() # Initialization of real-time plotter
writer.write_message("Initialization complete") # Logging the successful initialization 


##########################  MAIN CYCLE ############################
try:

    while True:
        print(operation_number)
        for group in groups: # Scrolling through every group
            data=group.get_filtered() # Recieving information
            for param in list(data.keys()): 
                sensors_data[str(group.name)][param].append(data[param]) # Appending new information to existing dict
            alert_sys.submit_frame({group.name:data}) # Transmitting information to Alert System
            if operation_number>max_size_arr: # If calibration is over - write data to lcd
                lcd.write({group.name:data})
            plotter.update_from_dict(sensors_data) # Updating plot
        if operation_number%10==0: # If 10 operaions passed - write data to file and log it
            writer.write_data(sensors_data)
            writer.write_message(str(operation_number)+" measurments successfully passed and writen.")
            plotter.clean(sensors_data[str(grp3.name)]["time"][-1])
            sensors_data={str(grp1.name):{"temperature":[], "humidity":[],"air":[],"time":[]},grp2.name:{"temperature":[], "humidity":[],"air":[],"time":[]},grp3.name:{"temperature":[], "humidity":[],"air":[],"time":[]}}
        if operation_number==max_size_arr: # Every 10 operations - clear the LCD
            lcd.st()
        operation_number+=1
except KeyboardInterrupt:
    writer.write_message("Keyboard interrupt")
    alert_sys.stop()
    lcd.clear()
    GPIO.cleanup()
    print("Keyboard Interrupt")