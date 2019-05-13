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

    print()