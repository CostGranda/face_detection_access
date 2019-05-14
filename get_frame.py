from cv2 import VideoCapture, imwrite 
import settings
from os import getenv

class CaptureFrame():
    def __init__(self):
        self.capture = VideoCapture(getenv('RTSP_SERVER_URI'))
        self.image = getenv('SAVED_IMAGE')

    def get_image(self):
        """Get the frame from the cam and save it locally for possible upload to s3.
        Returns:
            Boolean
        """
        # Returns false if there isn't frame.
        retval, frame = self.capture.read()
        print(self.image)
        if retval:
            imwrite(self.image, frame)
        return retval