from cv2 import VideoCapture, imwrite 
from os import getenv
import settings

class CaptureFrame():
    def __init__(self):
        self.capture = VideoCapture(getenv('RTSP_SERVER_URI'))
        self.image = getenv('SAVED_IMG')

    def get_image(self):
        """Get the frame from the cam and save it locally for possible upload to s3.
        Returns:
            Boolean
        """
        # Returns false if there isn't frame.
        retval, frame = self.capture.read()
        if retval:
            imwrite(self.image, frame)
        return retval