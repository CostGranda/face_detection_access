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
        sleep(5)
        self.red_off()
        
    def red_off(self):
        GPIO.output(self.red,0)
        
    def green_on(self):
        GPIO.output(self.green,1)
        sleep(5)
        self.green_off()
        
    def green_off(self):
        GPIO.output(self.green,0)
       
    def setup(self):
        GPIO.setup(self.red,GPIO.OUT)
        GPIO.output(self.red,0)
        GPIO.setup(self.green,GPIO.OUT)
        GPIO.output(self.green,0)

                
        
GPIO.setmode(GPIO.BCM)
RED = 27
GREEN = 5
BLUE = 26

try:
  while (True): 
        GPIO.output(RED,1)
        sleep(1)
        GPIO.output(RED,0)
        sleep(1)
        GPIO.output(GREEN,1)
        sleep(1)
        GPIO.output(GREEN,0)
        sleep(1)
        GPIO.output(BLUE,1)
        sleep(1)
        GPIO.output(BLUE,0)
        sleep(1)
        #GPIO.output(GREEN,int(request[1]))
        #GPIO.output(BLUE,int(request[2]))
except KeyboardInterrupt:
    GPIO.cleanup()