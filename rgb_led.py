import RPi.GPIO as GPIO
from time import sleep

class RGB_Led():
    def __init__(self, r, g, b=1):
        self.red = r
        self.green = g
        self.blue = b
        self.setup()
    
    def red_on(self):
        GPIO.output(self.red,1)
        
    def red_off(self):
        GPIO.output(self.red,0)
        
    def green_on(self):
        GPIO.output(self.green,1)
        
    def green_off(self):
        GPIO.output(self.green,0)
       
    def setup(self):
        GPIO.setup(self.red,GPIO.OUT)
        GPIO.output(self.red,0)
        GPIO.setup(self.green,GPIO.OUT)
        GPIO.output(self.green,0)
