from HondaCivic2015Hybrid import HondaCivic
from http.server import HTTPServer, BaseHTTPRequestHandler
import json


Car = HondaCivic()

class TestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.path)
        if self.path == "/data":
            car = {
                "gas": Car.get_gas_percent(),
                "speed": Car.get_speed_mph(),
                "battery": Car.get_battery()
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
        if self.path == '/favicon.ico':
            self.send_error(404, "nope")


server = HTTPServer(('', 8000), TestHandler)
server.serve_forever()



