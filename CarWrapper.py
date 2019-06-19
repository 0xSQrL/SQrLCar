import obd
import obd.utils
import math
from threading import Thread
from serial.serialutil import SerialException
import time


class Constants:
    DEBUG = False
    GRAMS_AIR_TO_FUEL = 1./14.7
    GRAMS_TO_GALLON_FUEL = 1 / (454 * 6.701)
    MAF_CONVERSION = GRAMS_AIR_TO_FUEL * GRAMS_TO_GALLON_FUEL * 3600


class CarConnection:

    def __init__(self):
        self.connection = None
        self.disposed = False
        self.values = {
            obd.commands.SPEED: 15 * obd.Unit.mph,
            obd.commands.HYBRID_BATTERY_REMAINING: 50 * obd.Unit.percent,
            obd.commands.MAF: 10 * obd.Unit.gps
        }
        self.metrics = [
            obd.commands.SPEED,
            obd.commands.HYBRID_BATTERY_REMAINING,
            obd.commands.MAF
        ]
        if Constants.DEBUG:
            return
        self.retry_connection()

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while not self.disposed:
            time.sleep(0.2)
            for metric in self.metrics:
                self.try_query(metric)


    def retry_connection(self):
        if self.connection is not None and self.connection.is_connected() == obd.OBDStatus.NOT_CONNECTED:
            self.connection.close()
        try:
            self.connection = obd.OBD()
        except SerialException:
            print("No OBD device found")

    def get_speed_mph(self):
        if Constants.DEBUG:
            return 10.5
        return math.floor(self.values[obd.commands.SPEED].to("mph").magnitude * 5) / 5

    def get_running_time(self):
        if Constants.DEBUG:
            return 400
        return self.values[obd.commands.RUN_TIME].magnitude

    def get_battery(self):
        if Constants.DEBUG:
            return 0.69
        return self.values[obd.commands.HYBRID_BATTERY_REMAINING].magnitude

    def get_pressure(self):
        if Constants.DEBUG:
            return 98
        return self.values[obd.commands.BAROMETRIC_PRESSURE].magnitude

    def get_gas_percent(self):
        if Constants.DEBUG:
            return 0.72
        return self.values[obd.commands.FUEL_LEVEL].magnitude

    def get_fuel_economy(self):
        if Constants.DEBUG:
            return 0.72

        return self.get_speed_mph() / self.get_fuel_consumption()

    def get_fuel_consumption(self):
        if Constants.DEBUG:
            return 0.72

        return self.values[obd.commands.MAF].magnitude * Constants.MAF_CONVERSION

    def try_query(self, command, force=True):
        try:
            ret = self.connection.query(command, force=force)
            if ret.value is not None:
                self.values[command] = ret
                return ret
        except:
            print('err')
        self.retry_connection()
        if command in self.values:
            return self.values[command]
        return -1 * obd.Unit.miles

    def dispose(self):
        self.disposed = True
        if self.connection is not None and self.connection.is_connected() == obd.OBDStatus.NOT_CONNECTED:
            self.connection.close()

