from CarWrapper import CarConnection

import cv2
import math
from CameraStream import CameraStream


def convert_bw(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def put_text(frame, text, x, y):
    font_size = 1
    cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, font_size, (0, 0, 0), 6, cv2.LINE_AA, False)
    cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 255, 255), 2, cv2.LINE_AA, False)


Car = CarConnection()
Car.start()
left = CameraStream(src=0, width=640, height=480)
#right = CameraStream(src=0, width=640, height=480)
left.frame_operation = convert_bw
left.start()
#right.start()

cv2.namedWindow("Camera", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Camera", cv2.WND_PROP_FULLSCREEN, True)

while True:
    image = left.frame
    #image2 = right.frame
    put_text(image, "{0:.1f} mph".format(Car.get_speed_mph()), 10, 200)
    put_text(image, "{0:.1f}% {1:+.4f}".format(Car.get_battery(), Car.get_battery_change()), 10, 240)
    put_text(image, "{0:.2f} gal/h".format(Car.get_fuel_consumption()), 10, 280)
    put_text(image, "{0:.0f} mpg".format(Car.get_fuel_economy()), 10, 320)
    cv2.imshow("Camera", image)
    #cv2.imshow("Camera2", image2)
    if cv2.waitKey(math.floor(1000/30)) & 0xFF == ord('q'):
        break

left.release()
#right.release()
Car.dispose()
