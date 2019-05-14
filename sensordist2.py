#!/usr/bin/python
# -*- coding: latin-1 -*-
try:
    import RPi.GPIO as GPIO  # Importamos la librería GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!")
import time  # Importamos time (time.sleep)
from rekognition_apis import RekognitionApis
from simple_storage_service import SimpleStorageServicce
from get_frame import CaptureFrame
from rgb_strip import RGB_Strip

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

lo_distanceSnsr = DistanceSensor(20, 21)
lo_rgb = RGB_Strip(17,22,24)
try:
    while True:  # Iniciamos un loop infinito
        distance = lo_distanceSnsr.get_distance()
        if distance <= 100:
            print(distance)
            lo_rgb.blue_on()
            time.sleep(3)
            lo_rgb.blue_off()
            print("LLAMADO AL METODO")
            #time.sleep(2)
        print(distance)  # Devolvemos la distancia (en centímetros) por pantalla
        # Pequeña pausa para no saturar el procesador de la Raspberry
        time.sleep(1)
except KeyboardInterrupt:  # Si el usuario pulsa CONTROL+C...
    print("quit")  # Avisamos del cierre al usuario
    GPIO.cleanup()  # Limpiamos los pines GPIO y salimos