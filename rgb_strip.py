import pigpio
from time import sleep
R=17
G=22
B=24
pi = pigpio.pi()
pi.set_PWM_dutycycle(R, 255)
sleep(10)
pi.set_PWM_dutycycle(R, 0)
pi.stop()