from rekognition_apis import RekognitionApis
from simple_storage_service import SimpleStorageServicce 
from get_frame import CaptureFrame

if __name__ == "__main__":
    lo_rekogn = RekognitionApis()
    lo_s3 = SimpleStorageServicce()
    #lo_getF = CaptureFrame()
    #lo_getF.capture()

    faceMatch = lo_rekogn.search_by_image(imageFile='cv2.jpg')
    if faceMatch:
        lo_s3.upload_file(faceMatch)
    try:
    while True:  # Iniciamos un loop infinito
        distance = lo_distanceSnsr.get_distance()
        if distance <= 100:
            print(distance)
            lo_rgb.blue_on()
            time.sleep(3)
            lo_rgb.blue_off()
            print("LLAMADO AL METODO")
            
        print(distance)  # Devolvemos la distancia (en centímetros) por pantalla
        # Pequeña pausa para no saturar el procesador de la Raspberry
        time.sleep(1)
    except KeyboardInterrupt:  # Si el usuario pulsa CONTROL+C...
        print("quit")  # Avisamos del cierre al usuario
        GPIO.cleanup()  # Limpiamos los pines GPIO y salimos
        print()