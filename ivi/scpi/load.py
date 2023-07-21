"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2012-2017 Alex Forencich
Copyright (c) 2023 Fred Fierling

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

import math

from .. import ivi
from .. import load
from . import common

LoadModeMapping = {
        'constant_current': 'CURRENT',
        'constant_voltage': 'VOLTAGE',
        'constant_resistance': 'RESISTANCE',
        'constant_power': 'POWER',
        'dynamic': 'DYNAMIC',
        'led': 'LED',
        'constant_impedance': 'IMPEDANCE',
        }

MeasurementRangeMapping = {
        'dc_volts': 'VOLT:DC:RANGE',
        'dc_current': 'CURR:DC:RANGE',
        }

MeasurementAutoRangeMapping = {
        'dc_volts': 'VOLT:DC:RANGE:AUTO',
        'dc_current': 'CURR:DC:RANGE:AUTO',
        }

TriggerSourceMapping = {
        'bus': 'BUS',
        'external': 'EXT',
        'immediate': 'IMM'}

class Base(common.IdnCommand, common.ErrorQuery, common.Reset,
        common.SelfTest, common.Memory,
        load.Base, ivi.Driver,
        ):
    "Generic SCPI electronic load driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')

        # early define of _do_scpi_init
        self.__dict__.setdefault('_do_scpi_init', True)

        super(Base, self).__init__(*args, **kwargs)

        self._self_test_delay = 40

        self._identity_description = "Generic SCPI electronic load driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = ""
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 4
        self._identity_specification_minor_version = 1
        self._identity_supported_instrument_models = ['LOAD']

    def _initialize(self, resource = None, id_query = False, reset = False, **kwargs):
        "Opens an I/O session to the instrument."

        super(Base, self)._initialize(resource, id_query, reset, **kwargs)

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
            self.utility.reset()

    def _utility_disable(self):
        pass

    def _utility_lock_object(self):
        pass

    def _utility_unlock_object(self):
        pass

    def _clear(self):
        self._write('*CLS')

    def _remote(self):
        self._write('SYST:REM')

    def _local(self):
        self._wirte('SYST:LOC')

    def _get_channel(self):  # TODO Untested
        if not self._driver_operation_simulate:
            value = self._ask(":CHAN?").upper().strip()
            if value in ChannelNameMapping:
                self._channel = int(ChannelNameMapping[value])
        return self._channel

    def _set_channel(self, value):  # TODO Untested
        value = str(value).upper()
        if not self._driver_operation_simulate:
            self._write(":CHAN '{value}'")
        self._channel = value

    # Base class handles channel name

    def _get_mode(self):
        if not self._driver_operation_simulate:
            value = self._ask(":SOUR:MODE?").upper().strip('"')
            value = [k for k,v in LoadModeMapping.items() if v==value][0]
            self._channel_mode[self._channel] = value
        return self._channel_mode[self._channel]

    def _set_mode(self, value):
        if value in LoadModeMapping:
            if not self._driver_operation_simulate:
                self._write(":SOUR:MODE '{LoadModeMapping[value]}'")
        else:
            raise ivi.ValueNotSupportedException()
        self._channel_mode[self._channel] = value

    def _get_input_enabled(self):
        if not self._driver_operation_simulate:
            value = self._ask(":INP?").upper().strip('"')
            self._channel_input_enabled[self._channel] = bool(int(value))
        return self._channel_input_enabled[self._channel]

    def _set_input_enabled(self, value):
        if not self._driver_operation_simulate:
            self._channel_input_enabled[self._channel] = self._write(
                    f":INP {1 if value else 0}")
        return self._channel_input_enabled[self._channel]

    def _get_input_shorted(self):
        if not self._driver_operation_simulate:
            value = self._ask(":INP:SHOR?").upper().strip('"')
            self._channel_input_shorted[self._channel] = bool(int(value))
        return self._channel_input_shorted[self._channel]

    def _set_input_shorted(self, value):
        if not self._driver_operation_simulate:
            self._channel_input_shorted[self._channel] = self._write(
                    f":INP:SHOR {1 if value else 0}")
        return self._channel_input_shorted[self._channel]

    def _get_voltage_constant(self):
        if not self._driver_operation_simulate:
            return float(self._ask(":VOLT?"))

    def _set_voltage_constant(self, value):
        if not self._driver_operation_simulate:
            if isinstance(value, str):
                value = value.upper()
                if value == 'MIN' or value == 'MAX':
                    self._write(f":VOLT {value}")
            else:
                self._write(f":VOLT {float(value)}")

    def _get_voltage_range(self):
        if not self._driver_operation_simulate:
            return float(self._ask(":VOLT:RANG?"))

    def _set_voltage_range(self, value):
        if not self._driver_operation_simulate:
            if isinstance(value, str):
                value = value.upper()
                if value == 'MIN' or value == 'MAX':
                    self._write(f":VOLT:RANG {value}")
            else:
                self._write(f":VOLT:RANG {float(value)}")

    def _get_voltage_on(self):
        if not self._driver_operation_simulate:
            return float(self._ask(":VOLT:ON?"))

    def _set_voltage_on(self, value):
        if not self._driver_operation_simulate:
            if isinstance(value, str):
                value = value.upper()
                if value == 'MIN' or value == 'MAX':
                    self._write(f":VOLT:ON {value}")
            else:
                self._write(f":VOLT:ON {float(value)}")

    def _get_voltage_off(self):
        if not self._driver_operation_simulate:
            return float(self._ask(":VOLT:OFF?"))

    def _set_voltage_off(self, value):
        if not self._driver_operation_simulate:
            if isinstance(value, str):
                value = value.upper()
                if value == 'MIN' or value == 'MAX':
                    self._write(f":VOLT:OFF {value}")
            else:
                self._write(f":VOLT:OFF {float(value)}")

    def _get_current_constant(self):
        if not self._driver_operation_simulate:
            return float(self._ask(":CURR?"))

    def _set_current_constant(self, value):
        if not self._driver_operation_simulate:
            if isinstance(value, str):
                value = value.upper()
                if value == 'MIN' or value == 'MAX':
                    self._write(f":CURR {value}")
            else:
                self._write(f":CURR {float(value)}")

    def _get_current_range(self):
        if not self._driver_operation_simulate:
            return float(self._ask(":CURR:RANG?"))

    def _set_current_range(self, value):
        if not self._driver_operation_simulate:
            if isinstance(value, str):
                value = value.upper()
                if value == 'MIN' or value == 'MAX':
                    self._write(f":CURR:RANG {value}") # TODO throw exception on bad value
            else:
                self._write(f":CURR:RANG {float(value)}")

    def _get_current_slew(self):
        if not self._driver_operation_simulate:
            return float(self._ask(":CURR:SLEW?"))

    def _set_current_slew(self, value):
        if not self._driver_operation_simulate:
            if isinstance(value, str):
                value = value.upper()
                if value == 'MIN' or value == 'MAX':
                    self._write(f":CURR:SLEW {value}")
            else:
                self._write(f":CURR:SLEW {float(value)}")

    def _get_current_slew_rise(self):
        if not self._driver_operation_simulate:
            return float(self._ask(":CURR:SLEW:RISE?"))

    def _set_current_slew_rise(self, value):
        if not self._driver_operation_simulate:
            if isinstance(value, str):
                value = value.upper()
                if value == 'MIN' or value == 'MAX':
                    self._write(f":CURR:SLEW:RISE {value}")
            else:
                self._write(f":CURR:SLEW:RISE {float(value)}")

    def _get_current_slew_fall(self):
        if not self._driver_operation_simulate:
            return float(self._ask(":CURR:SLEW:FALL?"))

    def _set_current_slew_fall(self, value):
        if not self._driver_operation_simulate:
            if isinstance(value, str):
                value = value.upper()
                if value == 'MIN' or value == 'MAX':
                    self._write(f":CURR:SLEW:FALL {value}")
            else:
                self._write(f":CURR:SLEW:FALL {float(value)}")

    def _get_current_protection(self):
        if not self._driver_operation_simulate:
            return float(self._ask(":CURR:PROT?"))

    def _set_current_protection(self, value):
        if not self._driver_operation_simulate:
            if isinstance(value, str):
                value = value.upper()
                if value == 'MIN' or value == 'MAX':
                    self._write(f":CURR:PROT {value}")
            else:
                self._write(f":CURR:PROT {float(value)}")

    def _get_power_constant(self):
        if not self._driver_operation_simulate:
            return float(self._ask(":POW?"))

    def _set_power_constant(self, value):
        if not self._driver_operation_simulate:
            if isinstance(value, str):
                value = value.upper()
                if value == 'MIN' or value == 'MAX':
                    self._write(f":POW {value}")
            else:
                self._write(f":POW {float(value)}")

    def _get_power_protection(self):
        if not self._driver_operation_simulate:
            return float(self._ask(":POW:PROT?"))

    def _set_power_protection(self, value):
        if not self._driver_operation_simulate:
            if isinstance(value, str):
                value = value.upper()
                if value == 'MIN' or value == 'MAX':
                    self._write(f":POW:PROT {value}")
            else:
                self._write(f":POW:PROT {float(value)}")

    def _get_resistance_constant(self):
        if not self._driver_operation_simulate:
            value = self._ask(":RES?")
            return float('inf' if value.endswith('INF0') else value)

    def _set_resistance_constant(self, value):
        if not self._driver_operation_simulate:
            if isinstance(value, str):
                value = value.upper()
                if value == 'MIN' or value == 'MAX':
                    self._write(f":RES {value}")
            else:
                self._write(f":RES {float(value)}")

    # Measurement functions
    def _measure_voltage(self):
        if not self._driver_operation_simulate:
            return float(self._ask(":MEAS:VOLT?"))

    def _measure_min_voltage(self):
        if not self._driver_operation_simulate:
            return float(self._ask(":MEAS:VOLT:MIN?"))

    def _measure_max_voltage(self):
        if not self._driver_operation_simulate:
            return float(self._ask(":MEAS:VOLT:MAX?"))

    def _measure_ptp_voltage(self):
        if not self._driver_operation_simulate:
            return float(self._ask(":MEAS:VOLT:PTP?"))

    def _measure_current(self):
        if not self._driver_operation_simulate:
            return float(self._ask(":MEAS:CURR?"))

    def _measure_min_current(self):
        if not self._driver_operation_simulate:
            return float(self._ask(":MEAS:CURR:MIN?"))

    def _measure_max_current(self):
        if not self._driver_operation_simulate:
            return float(self._ask(":MEAS:CURR:MAX?"))

    def _measure_ptp_current(self):
        if not self._driver_operation_simulate:
            return float(self._ask(":MEAS:CURR:PTP?"))

    def _measure_power(self):
        if not self._driver_operation_simulate:
            return float(self._ask(":MEAS:POW?"))

    def _measure_resistance(self):
        if not self._driver_operation_simulate:
            value = self._ask(":MEAS:RES?")  # TODO deal with infinite
            return float('inf' if value.endswith('INF0') else value)

