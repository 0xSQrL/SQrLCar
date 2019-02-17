from HondaCivic2015Hybrid import HondaCivic
from http.server import HTTPServer, BaseHTTPRequestHandler
import cv2
import json
import time
import numpy

Car = HondaCivic()
video_device = cv2.VideoCapture(0)
video_device.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_device.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

class TestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.path)
        if self.path == "/data":
            unused, image = video_device.read()
            file_loc = "images/"+str(time.time())+".jpg"
            cv2.imwrite(file_loc, image)
            car = {
                "gas": Car.get_gas_percent(),
                "speed": Car.get_speed_mph(),
                "battery": Car.get_battery(),
                "image": file_loc,
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytearray(json.dumps(car), 'utf-8'))
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            f = open("CarView.html")
            self.wfile.write(bytearray(f.read(), 'utf-8'))
            f.close()
        if self.path.startswith("/images/"):
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            f = open(self.path[1:])
            self.wfile.write(bytearray(f.read(), 'utf-8'))
            f.close()
        if self.path == '/favicon.ico':
            self.send_error(404, "nope")


server = HTTPServer(('', 8000), TestHandler)
server.serve_forever()

