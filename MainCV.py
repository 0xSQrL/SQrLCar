from CarWrapper import CarConnection

import cv2
import math
from CameraStream import CameraStream
from CSVLogger import CSVLogger
import time
import os
from threading import Thread


def convert_bw(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def put_text(frame, text, x, y):
    font_size = 1
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, text, (x, y), font, font_size, (0, 0, 0), 10, cv2.LINE_AA, False)
    cv2.putText(frame, text, (x, y), font, font_size, (255, 255, 255), 2, cv2.LINE_AA, False)

def put_diagnostics(image, car, x, y):
    offset = 0
    spacing = 40
    put_text(image, "{0:.1f} mph".format(car.get_speed_mph()), x, y + offset * spacing)
    offset += 1
    put_text(image, "{0:4.1f}% {1:+.2f}".format(car.get_battery(), Car.get_battery_change()), x, y + offset * spacing)
    offset += 1
    put_text(image, "{0:.2f} gal/h".format(car.get_fuel_consumption()), x, y + offset * spacing)
    offset += 1
    put_text(image, "{0:.6f} gallons".format(car.get_fuel_consumed()), x, y + offset * spacing)
    offset += 1
    put_text(image, "{0:.0f} mpg".format(car.get_fuel_economy()), x, y + offset * spacing)
    offset += 2
    put_text(image, time.strftime("%m/%d/%y %H:%M:%S"), x, y + offset * spacing)


def save_image(image, throwaway):
    cur_time = time.time()
    file_loc = "images/{}-{}.jpg".format(
        time.strftime("%y-%m-%d %H-%M-%S"),
        str(cur_time - int(cur_time))[2:4])
    cv2.imwrite(file_loc, image)


if not os.path.exists("logs"):
    os.mkdir("logs")
if not os.path.exists("images"):
    os.mkdir("images")
Car = CarConnection()
logger = CSVLogger(filepath="logs", headers=[
    'Time',
    'Speed (MPH)',
    'Battery',
    'Fuel Consumption'
])

Car.start()
left = CameraStream(src=0, width=640, height=480)
#right = CameraStream(src=0, width=640, height=480)
left.start()
#right.start()

cv2.namedWindow("Camera", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Camera", cv2.WND_PROP_FULLSCREEN, True)

frame_rate = math.floor(1000/30)
count = 5

while True:
    image = left.frame
    #image2 = right.frame
    put_diagnostics(image, Car, 10, 220)
    count -= 1
    if count <= 0:
        Thread(target=save_image, args=(image, None)).start()
        count = 5
    logger.log_data([
            time.time(),
            Car.get_speed_mph(),
            Car.get_battery(),
            Car.get_fuel_consumption()
    ])
    cv2.imshow("Camera", image)
    #cv2.imshow("Camera2", image2)
    if cv2.waitKey(frame_rate) & 0xFF == ord('q'):
        break

left.release()
#right.release()
Car.dispose()
logger.dispose()
