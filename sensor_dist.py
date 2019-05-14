#!/usr/bin/python
# -*- coding: latin-1 -*-
try:
    import RPi.GPIO as GPIO  # Importamos la librería GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!")
import time  # Importamos time (time.sleep)

class DistanceSensor():
    def __init__(self, trigg_pin, echo_pin):
        # Usamos el pin GPIO como TRIGGER
        self.GPIO_TRIGGER = trigg_pin
        # Usamos el pin GPIO como ECHO
        self.GPIO_ECHO = echo_pin
        self.setup()

    def setup(self):
        # Ponemos la placa en modo BCM
        GPIO.setmode(GPIO.BCM)
        # Configuramos Trigger como salida
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        # Configuramos Echo como entrada
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)  
        # Ponemos el pin 25 como LOW
        GPIO.output(self.GPIO_TRIGGER, False)  
    
    def get_distance(self):
        GPIO.output(self.GPIO_TRIGGER, True)  # Enviamos un pulso de ultrasonidos
        time.sleep(0.00001)  # Una pequeñña pausa
        GPIO.output(self.GPIO_TRIGGER, False)  # Apagamos el pulso
        start = time.time()  # Guarda el tiempo actual mediante time.time()
        # Mientras el sensor no reciba señal...
        while GPIO.input(self.GPIO_ECHO) == 0:
            start = time.time()  # Mantenemos el tiempo actual mediante time.time()
        while GPIO.input(self.GPIO_ECHO) == 1:  # Si el sensor recibe señal...
            stop = time.time()  # Guarda el tiempo actual mediante time.time() en otra variable
        elapsed = stop-start  # Obtenemos el tiempo transcurrido entre envío y recepción
        # Distancia es igual a tiempo por velocidad partido por 2   D = (T x V)/2
        distance = (elapsed * 34300)/2
        return distance
