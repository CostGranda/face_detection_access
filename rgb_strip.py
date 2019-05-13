try:
    import pigpio
except RuntimeError as E:
    print("Cannot load the pigpio module")

class RGB_Strip():

    def __init__(self, r, g, b):
        """
        Receives the GPIO Pin's to manipulate
        """
        self.R = r #RED LEDS
        self.G = g #GREEN LEDS
        self.B = b #BLUE LEDS
        # Maximum Brightnes
        self.ON = 255
        # Minimum Brightnes
        self.OFF = 0
        # Neecsita el demonio inicicalizado (pigpiod)
        self.pi = pigpio.pi()

    def red_on(self):
        self.pi.set_PWM_dutycycle(self.R, self.ON)

    def green_on(self):
        self.pi.set_PWM_dutycycle(self.G, self.ON)

    def blue_on(self):
        self.pi.set_PWM_dutycycle(self.B, self.ON)

    def red_off(self):
        self.pi.set_PWM_dutycycle(self.R, self.OFF)

    def green_off(self):
        self.pi.set_PWM_dutycycle(self.G, self.OFF)

    def blue_off(self):
        self.pi.set_PWM_dutycycle(self.B, self.OFF)

    def all_on(self):
        self.pi.set_PWM_dutycycle(self.R, self.ON)
        self.pi.set_PWM_dutycycle(self.G, self.ON)
        self.pi.set_PWM_dutycycle(self.B, self.ON)

    def all_off(self):
        self.pi.set_PWM_dutycycle(self.R, self.OFF)
        self.pi.set_PWM_dutycycle(self.G, self.OFF)
        self.pi.set_PWM_dutycycle(self.B, self.OFF)

    def stop(self):
        """
        Free GPIO PINS 
        """
        self.pi.stop()   