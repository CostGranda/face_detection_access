from rekognition_apis import RekognitionApis

if __name__ == "__main__":
    # client = rtsp.Client(rtsp_server_uri = os.getenv('RTSP_SERVER_URI'))
    # client.read().save("prueba.png")
    # client.close()
    lo_rekogn = RekognitionApis()
    lo_rekogn.list_faces()