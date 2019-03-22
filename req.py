try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    print("Cannot import RPi.GPIO! Is this a Raspberry?")
from time import sleep
import boto3
from dotenv import load_dotenv
import rtsp
import os

#Cargar variales de entorno
load_dotenv()
if __name__ == "__main__":
    imageFile='prueba.png'
    client=boto3.client('rekognition')
    with open(imageFile, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})
    print('Detected labels in ' + imageFile)
    for label in response['Labels']:
        print (label['Name'] + ' : ' + str(label['Confidence']))
    print('Done...')

    client = rtsp.Client(rtsp_server_uri = os.getenv('RTSP_SERVER_URI'))
# client.read().save("prueba.png")
# client.close()
# ffmpeg -y -i rtsp://admin:EWYJKZ@192.168.1.3:554/live -vframes 1 picture.png