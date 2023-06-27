"""

Python Interchangeable Virtual Instrument Library
Driver for Test Equity Model 140

Copyright (c) 2014-2023 Fred Fierling

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import time
from .. import ivi

class sunEC1X(ivi.Driver):
    "Sun Systems EC1x environmental chamber"

    SERIAL_NUMBER = 'AA21741'
    STATUS_HEATER = 4
    STATUS_COOLER = 5

    def __init__(self, *args, cache=False, **kwargs):
        if cache:
            raise InvalidOptionValueException('Cache not supported by driver (use cache=False)')

        self.__dict__.setdefault('_instrument_id', 'SUN ')

        super(sunEC1X, self).__init__(*args, id_query=True, **kwargs)

        self._identity_description = 'Sun Electronic Systems EC1x Environment Chamber'
        self._identity_identifier = ''
        self._identity_revision = ''
        self._identity_vendor = ''
        self._identity_supported_instrument_models = ['EC1x',]

        self._add_property('identity.instrument_serial_number',
                self._get_identity_instrument_serial_number)
        self._add_property('cooler_enabled', self._get_cooler_enabled, self._set_cooler_enabled)
        self._add_property('heater_enabled', self._get_heater_enabled, self._set_heater_enabled)
        self._add_property('chamber_temperature', self._get_temperature, )
        self._add_property('chamber_temperature_setpoint',
                self._get_temperature_setpoint, self._set_temperature_setpoint)
        self._add_property('chamber_rate',
                self._get_chamber_rate, self._set_chamber_rate)
        self._add_property('user_temperature', self._get_user_temperature)
        self._add_property('temperature_unit', self._get_temperature_unit)
        self._add_property('upper_temperature_limit', self._get_upper_temperature_limit,
                self._set_upper_temperature_limit)
        self._add_property('lower_temperature_limit', self._get_lower_temperature_limit,
                self._set_lower_temperature_limit)
        self._add_property('hour_meter', self._get_hour_meter, )

    def _initialize(self, resource=None, id_query=False, reset=False, **keywargs):
        "Opens an I/O session to the instrument."

        super(sunEC1X, self)._initialize(resource, id_query, reset, **keywargs)

        # interface clear
        if not self._driver_operation_simulate:
            self._clear()

        # check ID
        if self._driver_operation_simulate:
            self._identity_instrument_manufacturer = "Not available while simulating"
            self._identity_instrument_model = "Not available while simulating"
            self._identity_instrument_serial_number = "Not available while simulating"
            self._identity_instrument_firmware_revision = "Not available while simulating"
        else:
            if id_query:
                self._write('ON')
                id = self._ask('VER?')
                id_check = self._instrument_id
                if id.startswith(id_check):
                    id = id.split(' ')
                    self._identity_instrument_manufacturer = 'Sun Electronic Systems Inc.'
                    self._identity_instrument_model = id[1]
                    self._identity_instrument_serial_number = self.SERIAL_NUMBER
                    self._identity_instrument_firmware_revision = id[2].split('Ver')[1]
                    self._write('TIME=%s' % time.strftime('%H:%M:%S'))
                else:
                    raise Exception("Instrument ID mismatch, expecting %s, got %s",
                            id_check, id[:len(id_check)])
        # reset
        if reset:
            self.utility_reset()

    def _utility_reset(self):
        self._write('ON')
        self._write('STOPE9')
        self._write('ON')

    def _utility_reset_with_defaults(self):
        self.utility_reset()

    def _get_identity_instrument_manufacturer(self):
        return self._identity_instrument_manufacturer

    def _get_identity_instrument_model(self):
        return self._identity_instrument_model

    def _get_identity_instrument_serial_number(self):
        return self._identity_instrument_serial_number

    def _get_identity_instrument_firmware_revision(self):
        return self._identity_instrument_firmware_revision

    def _get_temperature(self):
        if self._driver_operation_simulate: 
            return 0
        else:
            return(float(self._ask('TEMP?')))

    def _get_user_temperature(self):
        if self._driver_operation_simulate: 
            return 0
        else:
            return(float(self._ask('USER?')))

    def _get_temperature_setpoint(self):
        if self._driver_operation_simulate: 
            return 0
        else:
            response = self._ask('SET?')
            try:
                response = float(response)
                return(response)
            except:
                return None
        
    def _set_temperature_setpoint(self, value):
        if not self._driver_operation_simulate: 
            self._write(f'SET={value}')
        return True

    def _get_chamber_rate(self):
        if self._driver_operation_simulate: 
            return 0
        else:
            return(float(self._ask('RATE?')))
        
    def _set_chamber_rate(self, value):
        if not self._driver_operation_simulate: 
            self._write(f'RATE={value}')
        return True

    def _get_heater_enabled(self):
        if self._driver_operation_simulate: 
            return True
        else:
            return(self._ask('STATUS?')[self.STATUS_HEATER] == 'Y')

    def _set_heater_enabled(self, value):
        if not self._driver_operation_simulate: 
            self._write('HON' if value else 'HOFF')
        return True

    def _get_cooler_enabled(self):
        if self._driver_operation_simulate: 
            return True
        else:
            return(self._ask('STATUS?')[self.STATUS_COOLER] == 'Y')

    def _set_cooler_enabled(self, value):
        if not self._driver_operation_simulate: 
            self._write('CON' if value else 'COFF')
        return True

    def _get_temperature_unit(self):
        if self._driver_operation_simulate: 
            return 0
        else:
            scale = (self._ask('SCALE#1?') + self._ask('SCALE#2?')).split('DEG')
            if len(scale) == 3:
                ret = scale[1][-1]
                if scale[1] != scale[2]:
                    ret += scale[2][-1]
                
                return(ret)
            else:
                raise UnexpectedResponseException()

    def _get_upper_temperature_limit(self):
        if self._driver_operation_simulate: 
            return 0
        else:
            return(float(self._ask('UTL?')))
        
    def _set_upper_temperature_limit(self, value):
        if not self._driver_operation_simulate: 
            self._write(f'UTL={value}')
        return True

    def _get_lower_temperature_limit(self):
        if self._driver_operation_simulate: 
            return 0
        else:
            return(float(self._ask('LTL?')))
        
    def _set_lower_temperature_limit(self, value):
        if not self._driver_operation_simulate: 
            self._write(f'LTL={value}')
        return True
        
    def _get_hour_meter(self):
        if self._driver_operation_simulate: 
            return 0
        else:
            return(float(self._ask('TIMEE?')))
