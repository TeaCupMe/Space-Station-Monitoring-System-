# Created by Aleksey Gilenko
# December 2020

try:
    import RPi.GPIO as GPIO
except ImportError:
    dependencies = ["RPi.GPIO as GPIO"]
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

class Alert_System:
    def __init__(self, buzzer_pin, alert_pins, button_pin):
        self.button_pin=button_pin
        self.buzzer_pin=buzzer_pin
        self.alert_pins=alert_pins
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(buzzer_pin, GPIO.OUT)
        self.buzzer_pwm=GPIO.PWM(buzzer_pin, 200)
        GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_pin, GPIO.RISING, callback=self.calm_it, bouncetime=20)
        self.hh=50
        self.lh=0
        self.ht=30
        self.lt=10
        self.buzzer_pwm.start(0)
        for pin in self.alert_pins:
            GPIO.setup(pin, GPIO.OUT)
    def submit_frame(self, data):
        if "Living room 1" in list(data.keys()) and not ((self.lt < data["Living room 1"]["temperature"] < self.ht) and (self.lh < data["Living room 1"]["humidity"] < self.hh)):
            GPIO.output(self.alert_pins[0], 1)
            self.buzzer_pwm.ChangeDutyCycle(70)
        elif "Living room 2" in list(data.keys()) and not ((self.lt < data["Living room 2"]["temperature"] < self.ht) and (self.lh < data["Living room 2"]["humidity"] < self.hh)):
            GPIO.output(self.alert_pins[1], 1)
            self.buzzer_pwm.ChangeDutyCycle(70)
        elif "Storage" in list(data.keys()) and not ((self.lt < data["Storage"]["temperature"] < self.ht) and (self.lh < data["Storage"]["humidity"] < self.hh)):
            GPIO.output(self.alert_pins[2], 1)
            self.buzzer_pwm.ChangeDutyCycle(70)
    def calm_it(self,a):
        for pin in self.alert_pins:
            GPIO.output(pin, 0)
        self.buzzer_pwm.ChangeDutyCycle(0)
    def stop(self):
        self.buzzer_pwm.stop()