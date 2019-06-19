from CarWrapper import CarConnection

import cv2
import math
from CameraStream import CameraStream
import numpy


def convert_bw(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def put_text(frame, text, x, y):
    cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 4, cv2.LINE_AA, False)
    cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA, False)


Car = CarConnection()

left = CameraStream(src=1, width=640, height=480)
right = CameraStream(src=0, width=640, height=480)
left.frame_operation = convert_bw
left.start()
#right.start()

cv2.namedWindow("Camera", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Camera", cv2.WND_PROP_FULLSCREEN, True)

while True:
    image = left.frame
    image2 = right.frame
    put_text(image, str(Car.get_speed_mph()) + " mph", 100, 200)
    put_text(image, str(Car.get_battery()) + "%", 100, 240)
    put_text(image, str(Car.get_fuel_consumption()) + " gal/h", 100, 280)
    put_text(image, str(Car.get_fuel_economy()) + " mpg", 100, 320)
    cv2.imshow("Camera", image)
    #cv2.imshow("Camera2", image2)
    if cv2.waitKey(math.floor(1000/30)) & 0xFF == ord('q'):
        break

left.release()
right.release()
