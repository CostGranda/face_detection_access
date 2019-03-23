from cv2 import VideoCapture, imwrite 
from dotenv import load_dotenv
from os import getenv

load_dotenv()

cap =  VideoCapture(getenv('RTSP_SERVER_URI'))
ret,frame = cap.read()
cv2.imwrite('cv2.png', frame)