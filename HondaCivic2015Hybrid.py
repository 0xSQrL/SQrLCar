import obd
import obd.utils
import math


class HondaCivic:
    GAS_TANK_GALLONS = 10.0
    MILES_PER_GALLON = 41.0
    DEBUG = True

    def __init__(self):
        self.connection = None
        if HondaCivic.DEBUG:
            return
        self.retry_connection()

    def retry_connection(self):
        if self.connection is not None and self.connection.is_connected() == obd.OBDStatus.NOT_CONNECTED:
            self.connection.close()
        self.connection = obd.OBD()

    def get_speed_mph(self):
        if HondaCivic.DEBUG:
            return 10.5
        return math.floor(self.try_query(obd.commands.SPEED).value.to("mph").magnitude * 5) / 5

    def get_running_time(self):
        if HondaCivic.DEBUG:
            return 400
        return self.try_query(obd.commands.RUN_TIME).value.magnitude

    def get_battery(self):
        if HondaCivic.DEBUG:
            return 0.69
        return self.try_query(obd.commands.HYBRID_BATTERY_REMAINING).value.magnitude

    def get_pressure(self):
        if HondaCivic.DEBUG:
            return 98
        return self.try_query(obd.commands.BAROMETRIC_PRESSURE).value.magnitude

    def get_gas_percent(self):
        if HondaCivic.DEBUG:
            return 0.72
        return self.try_query(obd.commands.FUEL_LEVEL).value.magnitude

    def get_gas_gallons(self):
        if HondaCivic.DEBUG:
            return 8.2
        return self.get_gas_percent() * HondaCivic.GAS_TANK_GALLONS

    def get_range(self):
        if HondaCivic.DEBUG:
            return 400.7
        return self.get_gas_gallons() * HondaCivic.MILES_PER_GALLON
        
    def try_query(self, command, force=True):
        try:
            ret = self.connection.query(command, force=force)
            if ret.value is not None:
                return ret
        except:
            print('err')
        self.retry_connection()
        return -1 * obd.Unit.miles
