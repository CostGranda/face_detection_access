from rekognition_apis import RekognitionApis
from simple_storage_service import SimpleStorageServicce 
from get_frame import CaptureFrame
from sensor_dist import DistanceSensor()
from rgb_strip import RGB_Strip

import settings
from os import getenv  # Get environment variale
from time import sleep


if __name__ == "__main__":
    # Clase de reconocimiento
    lo_rekogn = RekognitionApis()
    # Clase de S3 para subir la foto
    lo_s3 = SimpleStorageServicce()
    # Clase de la camara
    lo_getF = CaptureFrame()
    # Clase de distancia
    lo_distanceSnsr = DistanceSensor(20, 21)
    # Clase rgb strip 
    lo_rgb = RGB_Strip()

    try:
        while True:  # Iniciamos un loop infinito
            distance = lo_distanceSnsr.get_distance()
            if distance <= 100:
                ret = lo_getF.get_image()
                print(distance)
                if ret:
                    # Search for similarity score
                    faceMatch = lo_rekogn.search_by_image(imageFile=getenv('SAVED_IMAGE'))
                    if faceMatch:
                        lo_rgb.green_on()
                        lo_s3.upload_file(faceMatch)
                        sleep(5)
                        lo_rgb.green_off()
                    else:
                        lo_rgb.red_on()
                        sleep(3)
                        lo_rgb.red_off()
            # Pequeña pausa para no saturar el procesador de la Raspberry
            time.sleep(1)
    except KeyboardInterrupt:  # Si el usuario pulsa CONTROL+C...
        print("Quitting...")  # Avisamos del cierre al usuario
        lo_distanceSnsr.clean()  # Limpiamos los pines GPIO y salimos
        lo_rgb.stop()
        print()