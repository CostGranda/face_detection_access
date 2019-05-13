#!/usr/bin/python
# -*- coding: latin-1 -*-
try:
    import RPi.GPIO as GPIO    #Importamos la librería GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!")
import time                #Importamos time (time.sleep)
from rekognition_apis import RekognitionApis
from simple_storage_service import SimpleStorageServicce 
from get_frame import CaptureFrame

GPIO.setmode(GPIO.BCM)     #Ponemos la placa en modo BCM
GPIO_TRIGGER = 20          #Usamos el pin GPIO 25 como TRIGGER
GPIO_ECHO    = 21           #Usamos el pin GPIO 7 como ECHO
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  #Configuramos Trigger como salida
GPIO.setup(GPIO_ECHO,GPIO.IN)      #Configuramos Echo como entrada
GPIO.output(GPIO_TRIGGER,False)    #Ponemos el pin 25 como LOW


try:
    while True:     #Iniciamos un loop infinito
        GPIO.output(GPIO_TRIGGER,True)   #Enviamos un pulso de ultrasonidos
        time.sleep(0.00001)              #Una pequeñña pausa
        GPIO.output(GPIO_TRIGGER,False)  #Apagamos el pulso
        start = time.time()              #Guarda el tiempo actual mediante time.time()
        while GPIO.input(GPIO_ECHO)==0:  #Mientras el sensor no reciba señal...
            start = time.time()          #Mantenemos el tiempo actual mediante time.time()
        while GPIO.input(GPIO_ECHO)==1:  #Si el sensor recibe señal...
            stop = time.time()           #Guarda el tiempo actual mediante time.time() en otra variable
        elapsed = stop-start             #Obtenemos el tiempo transcurrido entre envío y recepción
        distance = (elapsed * 34300)/2   #Distancia es igual a tiempo por velocidad partido por 2   D = (T x V)/2
        if distance <=100:
            print("LLAMADO AL METODO")
        print(distance)                  #Devolvemos la distancia (en centímetros) por pantalla
        time.sleep(1)                    #Pequeña pausa para no saturar el procesador de la Raspberry
except KeyboardInterrupt:                #Si el usuario pulsa CONTROL+C...
    print("quit")                        #Avisamos del cierre al usuario
    GPIO.cleanup()                       #Limpiamos los pines GPIO y salimos