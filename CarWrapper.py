import obd
import obd.utils
import math
from threading import Thread
from serial.serialutil import SerialException
import time
import numpy


class Constants:
    GRAMS_AIR_TO_FUEL = 1./14.7
    GRAMS_TO_GALLON_FUEL = 1 / (454 * 6.701)
    MAF_CONVERSION = GRAMS_AIR_TO_FUEL * GRAMS_TO_GALLON_FUEL * 3600


class CarConnection:

    def __init__(self):
        self.connection = None
        self.disposed = False
        self.values = {
            obd.commands.SPEED: 15 * obd.Unit.mph,
            obd.commands.HYBRID_BATTERY_REMAINING: 5.1234 * obd.Unit.percent,
            obd.commands.MAF: 10 * obd.Unit.gps
        }
        self.metrics = [
            obd.commands.SPEED,
            obd.commands.HYBRID_BATTERY_REMAINING,
            obd.commands.MAF
        ]
        self.gas_used = 0
        self.last_gas_query = time.time()
        self.battery_history = []
        self.retry_connection()

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while not self.disposed:
            time.sleep(0.2)
            last_battery = 0
            for metric in self.metrics:
                if metric == obd.commands.HYBRID_BATTERY_REMAINING:
                    last_battery = self.values[obd.commands.HYBRID_BATTERY_REMAINING].magnitude

                success = self.try_query(metric)

                if success and metric == obd.commands.MAF:
                    tmp_time = time.time()
                    time_dif = tmp_time - self.last_gas_query
                    self.gas_used += self.values[obd.commands.MAF].magnitude * time_dif
                    self.last_gas_query = tmp_time

                if metric == obd.commands.HYBRID_BATTERY_REMAINING:
                    battery_diff = self.values[obd.commands.HYBRID_BATTERY_REMAINING].magnitude - last_battery
                    print(len(self.battery_history))
                    self.battery_history.append(battery_diff)
                    if len(self.battery_history) > 20:
                        self.battery_history.pop(0)

    def retry_connection(self):
        if self.connection is not None and self.connection.is_connected() == obd.OBDStatus.NOT_CONNECTED:
            self.connection.close()
        try:
            self.connection = obd.OBD()
        except SerialException:
            print("No OBD device found")

    def get_speed_mph(self):
        return math.floor(self.values[obd.commands.SPEED].to("mph").magnitude * 5) / 5

    def get_running_time(self):
        return self.values[obd.commands.RUN_TIME].magnitude

    def get_battery(self):
        return self.values[obd.commands.HYBRID_BATTERY_REMAINING].magnitude

    def get_battery_change(self):
        return numpy.average(self.battery_history)

    def get_pressure(self):
        return self.values[obd.commands.BAROMETRIC_PRESSURE].magnitude

    def get_gas_percent(self):
        return self.values[obd.commands.FUEL_LEVEL].magnitude

    def get_fuel_economy(self):
        speed = self.get_speed_mph()
        consumption = self.get_fuel_consumption()
        if consumption == 0:
            return 0
        return speed / consumption

    def get_fuel_consumption(self):
        return self.values[obd.commands.MAF].magnitude * Constants.MAF_CONVERSION

    def get_fuel_consumed(self):
        return self.gas_used * Constants.GRAMS_AIR_TO_FUEL * Constants.GRAMS_TO_GALLON_FUEL

    def try_query(self, command, force=True):
        try:
            ret = self.connection.query(command, force=force)
            if ret.value is not None:
                self.values[command] = ret.value
                return True
        except AttributeError:
            print('Failed to query {}'.format(command))

        self.retry_connection()
        return False

    def dispose(self):
        self.disposed = True
        if self.connection is not None and self.connection.is_connected() == obd.OBDStatus.NOT_CONNECTED:
            self.connection.close()

