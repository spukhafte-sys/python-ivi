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

from .. import ivi

class sunEC1X(ivi.Driver):
    "Sun Systems EC1x environmental chamber"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'SUN EC1x')

        super(sunEC1X, self).__init__(*args, **kwargs)

        self._driver_operation_cache = False
        self._identity_description = 'Sun Systems EC1x Environment Chamber'
        self._identity_identifier = ''
        self._identity_revision = ''
        self._identity_vendor = ''
        self._identity_instrument_manufacturer = 'Sun Systems'
        self._identity_instrument_model = ''
        self._identity_instrument_firmware_revision = ''
        self._identity_supported_instrument_models = ['EC1x',]

        self._add_property('chamber_temperature', self._get_temperature)
        self._add_property('chamber_temperature_setpoint', self._get_temperature_setpoint, self._set_temperature_setpoint )
#       self._add_property('user_temperature', self._get_user_temperature)

#       self._add_property('part_temperature_decimal_config', self._get_part_temperature_decimal_config)
#       self._add_property('temperature_unit', self._get_temperature_unit_config)
#       self._temperature_decimal_config = 1 #default to 500 means 50.0degC
#       self._humidity_decimal_config = 1 #default to 500 means 50.0%RH
#       self._part_temperature_decimal_config = 1 #default to 500 means 50.0degC
#       self._temperature_unit = 1 #default to degC
    
    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."

        super(sunEC1X, self)._initialize(resource, id_query, reset, **keywargs)

        # interface clear
        if not self._driver_operation_simulate:
            self._clear()

        # check ID
        if id_query and not self._driver_operation_simulate:
            id = self.identity.instrument_model
            id_check = self._instrument_id
            id_short = id[:len(id_check)]
            if id_short != id_check:
                raise Exception("Instrument ID mismatch, expecting %s, got %s", id_check, id_short)

        # reset
        if reset:
            self.utility_reset()

    def _load_id_string(self):
        if self._driver_operation_simulate:
            self._identity_instrument_manufacturer = "Not available while simulating"
            self._identity_instrument_model = "Not available while simulating"
            self._identity_instrument_serial_number = "Not available while simulating"
            self._identity_instrument_firmware_revision = "Not available while simulating"
        else:
            self._identity_instrument_manufacturer = "Agilent Technologies"
            self._identity_instrument_model = self._ask("ID?")
            self._identity_instrument_serial_number = self._ask("SER?")
            self._identity_instrument_firmware_revision = self._ask("REV?")
            self._set_cache_valid(True, 'identity_instrument_manufacturer')
            self._set_cache_valid(True, 'identity_instrument_model')
            self._set_cache_valid(True, 'identity_instrument_serial_number')
            self._set_cache_valid(True, 'identity_instrument_firmware_revision')

    def _get_identity_instrument_manufacturer(self):
        if self._get_cache_valid():
            return self._identity_instrument_manufacturer
        self._load_id_string()
        return self._identity_instrument_manufacturer

    def _get_identity_instrument_model(self):
        if self._get_cache_valid():
            return self._identity_instrument_model
        self._load_id_string()
        return self._identity_instrument_model

    def _get_identity_instrument_serial_number(self):
        if self._get_cache_valid():
            return self._identity_instrument_serial_number
        self._load_id_string()
        return self._identity_instrument_serial_number

    def _get_identity_instrument_firmware_revision(self):
        if self._get_cache_valid():
            return self._identity_instrument_firmware_revision
        self._load_id_string()
        return self._identity_instrument_firmware_revision

    def _get_temperature(self):
        if not self._driver_operation_simulate: 
            resp=int(self._read_register(100))
            if self._temperature_decimal_config==1:
                temperature=float(resp)/10
            else:
                temperature=float(resp)
            return temperature
        return 0

    def _get_temperature_setpoint(self):
        resp=int(self._read_register(300))
        #print(resp)
        #print(self._temperature_decimal_config)
        if self._temperature_decimal_config==1:
            temperature=float(resp)/10
        else:
            temperature=float(resp)
        return temperature
        
    def _set_temperature_setpoint(self, value):
        if self._temperature_decimal_config==1:
            temperature=int(float(value)*10)
        else:
            temperature=int(value)        
          
        if not self._driver_operation_simulate: 
            self._write_register(300, temperature)
