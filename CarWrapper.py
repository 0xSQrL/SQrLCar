import obd
import obd.utils
import math


class Constants:
    DEBUG = True
    GRAMS_AIR_TO_FUEL = 1./14.7
    GRAMS_TO_GALLON_FUEL = 1 / (454 * 6.701)
    MAF_CONVERSION = GRAMS_AIR_TO_FUEL * GRAMS_TO_GALLON_FUEL * 3600


class CarConnection:

    def __init__(self):
        self.connection = None
        self.values = {}
        if Constants.DEBUG:
            return
        self.retry_connection()

    def retry_connection(self):
        if self.connection is not None and self.connection.is_connected() == obd.OBDStatus.NOT_CONNECTED:
            self.connection.close()
        self.connection = obd.OBD()

    def get_speed_mph(self):
        if Constants.DEBUG:
            return 10.5
        return math.floor(self.try_query(obd.commands.SPEED).value.to("mph").magnitude * 5) / 5

    def get_running_time(self):
        if Constants.DEBUG:
            return 400
        return self.try_query(obd.commands.RUN_TIME).value.magnitude

    def get_battery(self):
        if Constants.DEBUG:
            return 0.69
        return self.try_query(obd.commands.HYBRID_BATTERY_REMAINING).value.magnitude

    def get_pressure(self):
        if Constants.DEBUG:
            return 98
        return self.try_query(obd.commands.BAROMETRIC_PRESSURE).value.magnitude

    def get_gas_percent(self):
        if Constants.DEBUG:
            return 0.72
        return self.try_query(obd.commands.FUEL_LEVEL).value.magnitude

    def get_fuel_economy(self):
        if Constants.DEBUG:
            return 0.72

        return self.get_speed_mph() / self.get_fuel_consumption()

    def get_fuel_consumption(self):
        if Constants.DEBUG:
            return 0.72

        return self.try_query(obd.commands.MAF).value.magnitude * Constants.MAF_CONVERSION

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
