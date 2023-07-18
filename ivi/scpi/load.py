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

class Base(common.IdnCommand, common.ErrorQuery, common.Reset, common.SelfTest,
           load.Base,
           ivi.Driver,
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
        self._identity_instrument_manufacturer = "B&K Precision"
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
    
    def _get_load_mode(self):
        if not self._driver_operation_simulate:
            value = self._ask(":SOUR:MODE?").upper().strip('"')
            value = [k for k,v in LoadModeMapping.items() if v==value][0]
            self._load_mode = value
        return self._load_mode
    
    def _set_load_mode(self, value):
        if value in LoadModeMapping:
            if not self._driver_operation_simulate:
                self._write(":SOUR:MODE '{LoadModeMapping[value]}'") 
            self._load_mode = value
        else:
            raise ivi.ValueNotSupportedException()
    
    def _get_range(self):
        if not self._driver_operation_simulate:
            func = self._get_measurement_function()
            if func in MeasurementRangeMapping:
                cmd = MeasurementRangeMapping[func]
                value = float(self._ask("%s?" % (cmd)))
                self._range = value
        return self._range
    
    def _set_range(self, value):
        value = float(value)
        # round up to even power of 10
        value = math.pow(10, math.ceil(math.log10(value)))
        if not self._driver_operation_simulate:
            func = self._get_measurement_function()
            if func in MeasurementRangeMapping:
                cmd = MeasurementRangeMapping[func]
                self._write("%s %g" % (cmd, value))
        self._range = value
    
    def _get_auto_range(self):
        if not self._driver_operation_simulate:
            func = self._get_measurement_function()
            if func in MeasurementAutoRangeMapping:
                cmd = MeasurementAutoRangeMapping[func]
                value = int(self._ask("%s?" % (cmd)))
                if value == 0:
                    value = 'off'
                elif value == 1:
                    value = 'on'
                self._auto_range = value
        return self._auto_range

    def _get_channel_enabled(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate:
            self._channel_enabled[index] = bool(int(
                self._ask(f":{self._channel_name[index]}:inp?")))
        return self._channel_enabled[index]

    def _set_channel_enabled(self, index, value):
        value = bool(value)
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate:
            self._write("inp %d" % (int(value)))
        self._channel_enabled[index] = value
    
    def _set_auto_range(self, value):
        if value not in load.Auto2:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            func = self._get_measurement_function()
            if func in MeasurementAutoRangeMapping:
                cmd = MeasurementAutoRangeMapping[func]
                self._write("%s %d" % (cmd, int(value == 'on')))
        self._auto_range = value
    
    def _get_trigger_delay(self):
        if not self._driver_operation_simulate:
            value = float(self._ask("trigger:delay?"))
            self._trigger_delay = value
        return self._trigger_delay
    
    def _set_trigger_delay(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write('trigger:delay %g' % value)
        self._trigger_delay = value
    
    def _get_trigger_delay_auto(self):
        if not self._driver_operation_simulate:
            value = bool(int(self._ask("trigger:delay:auto?")))
            self._trigger_delay_auto = value
        return self._trigger_delay_auto
    
    def _set_trigger_delay_auto(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write('trigger:delay:auto %d' % int(value))
        self._trigger_delay_auto = value
    
    def _get_trigger_source(self):
        if not self._driver_operation_simulate:
            value = self._ask("trigger:source?").upper()
            value = [k for k,v in TriggerSourceMapping.items() if v==value][0]
            self._trigger_source = value
        return self._trigger_source
    
    def _set_trigger_source(self, value):
        if value not in TriggerSourceMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":trigger:source %s" % TriggerSourceMapping[value])
        self._trigger_source = value
    
    def _measurement_abort(self):
        if not self._driver_operation_simulate:
            self._write(":abort")
    
    def _measurement_fetch(self, max_time):
        if not self._driver_operation_simulate:
            return float(self._ask(":fetch?"))
        return 0.0
    
    def _measurement_initiate(self):
        if not self._driver_operation_simulate:
            self._write(":initiate")
    
    def _measurement_is_out_of_range(self, value):
        return self._measurement_is_over_range(value) or self._measurement_is_under_range(value)
    
    def _measurement_is_over_range(self, value):
        return value == 9.9e+37
    
    def _measurement_is_under_range(self, value):
        return value == -9.9e+37
    
    def _measurement_read(self, max_time):
        if not self._driver_operation_simulate:
            return float(self._ask(":read?"))
        return 0.0
    
class SoftwareTrigger(load.SoftwareTrigger):
    """Extension methods for electronic loads that can initiate a measurement
    based on a software trigger signal"""
    
    def _send_software_trigger(self):
        if not self._driver_operation_simulate:
            self._write("*trg")

