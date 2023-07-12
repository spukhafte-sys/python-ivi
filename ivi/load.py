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

from . import ivi

# Parameter Values
ApertureTimeUnits = set(['seconds', 'powerline_cycles'])
Auto = set(['off', 'on', 'once'])
Auto2 = set(['off', 'on'])
LoadMode = set(['constant_current', 'constant_voltage', 'constant_resistance', 'constant_power',])
Slope = set(['positive', 'negative'])

class Base(ivi.IviContainer):
    "Base IVI methods for electronic loads"
    
    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        
        cls = 'Load'
        grp = 'Base'
        ivi.add_group_capability(self, cls+grp)
        
        self._load_mode = 'constant_current'
        self._range = 0
        self._auto_range = 'off'
        self._resolution = 1
        
        self._trigger_delay = 0
        self._trigger_delay_auto = False
        self._trigger_source = ''
        
        self._add_property('mode',
            self._get_load_mode,
            self._set_load_mode)
        self._add_property('range',
            self._get_range,
            self._set_range)
        self._add_property('auto_range',
            self._get_auto_range,
            self._set_auto_range)
        self._add_property('resolution',
            self._get_resolution,
            self._set_resolution)
        self._add_property('trigger.delay',
            self._get_trigger_delay,
            self._set_trigger_delay)
        self._add_property('trigger.delay_auto',
            self._get_trigger_delay_auto,
            self._set_trigger_delay_auto)
        self._add_property('trigger.source',
            self._get_trigger_source,
            self._set_trigger_source)
        self._add_method('configure',
            self._configure)
        self._add_method('trigger.configure',
            self._trigger_configure)
        self._add_method('measurement.abort',
            self._measurement_abort)
        self._add_method('measurement.fetch',
            self._measurement_fetch)
        self._add_method('measurement.initiate',
            self._measurement_initiate)
        self._add_method('measurement.is_out_of_range',
            self._measurement_is_out_of_range)
        self._add_method('measurement.is_over_range',
            self._measurement_is_over_range)
        self._add_method('measurement.is_under_range',
            self._measurement_is_under_range)
        self._add_method('measurement.read',
            self._measurement_read)
    
    def _get_load_mode(self):
        return self._load_mode
    
    def _set_load_mode(self, value):
        if value not in LoadMode:
            raise ivi.ValueNotSupportedException()
        self._load_mode = value
    
    def _get_range(self):
        return self._range
    
    def _set_range(self, value):
        value = float(value)
        self._range = value
    
    def _get_auto_range(self):
        return self._auto_range
    
    def _set_auto_range(self, value):
        if value not in Auto:
            raise ivi.ValueNotSupportedException()
        self._auto_range = value
    
    def _get_resolution(self):
        return self._resolution
    
    def _set_resolution(self, value):
        value = float(value)
        self._resolution = value
    
    def _get_trigger_delay(self):
        return self._trigger_delay
    
    def _set_trigger_delay(self, value):
        value = float(value)
        self._trigger_delay = value
    
    def _get_trigger_delay_auto(self):
        return self._trigger_delay_auto
    
    def _set_trigger_delay_auto(self, value):
        value = bool(value)
        self._trigger_delay_auto = value
    
    def _get_trigger_source(self):
        return self._trigger_source
    
    def _set_trigger_source(self, value):
        value = str(value)
        self._trigger_source = value
    
    def _measurement_abort(self):
        pass
    
    def _configure(self, function, range):
        self._set_load_mode(function)
        if range in Auto:
            self._set_auto_range(range)
        else:
            self._set_range(range)
    
    def _trigger_configure(self, source, delay):
        self._set_trigger_source(source)
        if isinstance(delay, bool):
            self._set_trigger_auto_delay(delay)
        else:
            self._set_trigger_delay(delay)
    
    def _measurement_fetch(self, max_time):
        return 0.0
    
    def _measurement_initiate(self):
        pass
    
    def _measurement_is_out_of_range(self, value):
        return self._measurement_is_over_range(value) or self._measurement_is_under_range(value)
    
    def _measurement_is_over_range(self, value):
        return False
    
    def _measurement_is_under_range(self, value):
        return False
    
    def _measurement_read(self, max_time):
        return 0.0
    
    
class ACMeasurement(ivi.IviContainer):
    "Extension IVI methods for electronic loads that can take AC voltage or AC current measurements"
    
    def __init__(self, *args, **kwargs):
        super(ACMeasurement, self).__init__(*args, **kwargs)
        
        cls = 'Load'
        grp = 'ACMeasurement'
        ivi.add_group_capability(self, cls+grp)
        
        self._ac_frequency_max = 100
        self._ac_frequency_min = 10
        
        self._add_property('ac.frequency_max',
                        self._get_ac_frequency_max,
                        self._set_ac_frequency_max)
        self._add_property('ac.frequency_min',
                        self._get_ac_frequency_min,
                        self._set_ac_frequency_min)
        self._add_method('ac.configure_bandwidth',
                        self._ac_configure_bandwidth)
    
    def _get_ac_frequency_max(self):
        return self._ac_frequency_max
    
    def _set_ac_frequency_max(self, value):
        value = float(value)
        self._ac_frequency_max = value
    
    def _get_ac_frequency_min(self):
        return self._ac_frequency_min
    
    def _set_ac_frequency_min(self, value):
        value = float(value)
        self._ac_frequency_min = value
    
    def _ac_configure_bandwidth(self, min_f, max_f):
        self._set_ac_frequency_min(min_f)
        self._set_ac_frequency_max(max_f)
    
class TriggerSlope(ivi.IviContainer):
    """Extension IVI methods for electronic loads that can specify the polarity of
    the external trigger signal"""
    
    def __init__(self, *args, **kwargs):
        super(TriggerSlope, self).__init__(*args, **kwargs)
        
        cls = 'Load'
        grp = 'TriggerSlope'
        ivi.add_group_capability(self, cls+grp)
        
        self._trigger_slope = 'positive'
        
        self._add_property('trigger.slope',
                        self._get_trigger_slope,
                        self._set_trigger_slope)
    
    def _get_trigger_slope(self):
        return self._trigger_slope
    
    def _set_trigger_slope(self, value):
        if value not in Slope:
            raise ivi.ValueNotSupportedException()
        self._trigger_slope = value
    
class SoftwareTrigger(ivi.IviContainer):
    "Extension IVI methods for electronic loads that can initiate a measurement based on a software trigger signal"
    
    def __init__(self, *args, **kwargs):
        super(SoftwareTrigger, self).__init__(*args, **kwargs)
        
        cls = 'Load'
        grp = 'SoftwareTrigger'
        ivi.add_group_capability(self, cls+grp)
        
        self._add_method('send_software_trigger',
            self._send_software_trigger,
            ivi.Doc("""
            This function sends a software-generated trigger to the instrument. It is
            only applicable for instruments using interfaces or protocols which
            support an explicit trigger function. For example, with GPIB this function
            could send a group execute trigger to the instrument. Other
            implementations might send a ``*TRG`` command.
                        
            Since instruments interpret a software-generated trigger in a wide variety
            of ways, the precise response of the instrument to this trigger is not
            defined. Note that SCPI details a possible implementation.
                        
            This function should not use resources which are potentially shared by
            other devices (for example, the VXI trigger lines). Use of such shared
            resources may have undesirable effects on other devices.
                        
            This function should not check the instrument status. Typically, the
            end-user calls this function only in a sequence of calls to other
            low-level driver functions. The sequence performs one operation. The
            end-user uses the low-level functions to optimize one or more aspects of
            interaction with the instrument. To check the instrument status, call the
            appropriate error query function at the conclusion of the sequence.
                        
            The trigger source attribute must accept Software Trigger as a valid
            setting for this function to work. If the trigger source is not set to
            Software Trigger, this function does nothing and returns the error Trigger
            Not Software.
            """, cls, grp, '13.2.1', 'send_software_trigger'))
    
    def _send_software_trigger(self):
        pass
    
class DeviceInfo(ivi.IviContainer):
    "A set of read-only attributes for electronic loads that can be queried to determine how they are presently configured"
    
    def __init__(self, *args, **kwargs):
        super(DeviceInfo, self).__init__(*args, **kwargs)
        
        cls = 'Load'
        grp = 'DeviceInfo'
        ivi.add_group_capability(self, cls+grp)
        
        self._advanced_aperture_time = 1.0
        self._advanced_aperture_time_units = 'seconds'
        
        self._add_property('advanced.aperture_time',
                        self._get_advanced_aperture_time)
        self._add_property('advanced.aperture_time_units',
                        self._get_advanced_aperture_time_units)
    
    def _get_advanced_aperture_time(self):
        return self._advanced_aperture_time
    
    def _get_advanced_aperture_time_units(self):
        return self._advanced_aperture_time_units
    
class AutoRangeValue(ivi.IviContainer):
    "Extension IVI methods for electronic loads that can return the actual range value when auto ranging"
    
    def __init__(self, *args, **kwargs):
        super(AutoRangeValue, self).__init__(*args, **kwargs)
        
        cls = 'Load'
        grp = 'AutoRangeValue'
        ivi.add_group_capability(self, cls+grp)
        
        self._advanced_actual_range = 1.0
        
        self._add_property('advanced.actual_range',
                        self._get_advanced_actual_range)
    
    def _get_advanced_actual_range(self):
        return self._advanced_actual_range
    
class AutoZero(ivi.IviContainer):
    "Extension IVI methods for electronic loads that can take an auto zero reading"
    
    def __init__(self, *args, **kwargs):
        super(AutoZero, self).__init__(*args, **kwargs)
        
        cls = 'Load'
        grp = 'AutoZero'
        ivi.add_group_capability(self, cls+grp)
        
        self._advanced_auto_zero = 'off'
        
        self._add_property('advanced.auto_zero',
                        self._get_advanced_auto_zero,
                        self._set_advanced_auto_zero)
        
    def _get_advanced_auto_zero(self):
        return self._advanced_auto_zero
    
    def _set_advanced_auto_zero(self, value):
        if value not in Auto:
            return ivi.ValueNotSupportedException
        self._advanced_auto_zero = value
    
class PowerLineFrequency(ivi.IviContainer):
    "Extension IVI methods for electronic loads that can specify the power line frequency"
    
    def __init__(self, *args, **kwargs):
        super(PowerLineFrequency, self).__init__(*args, **kwargs)
        
        cls = 'Load'
        grp = 'PowerLineFrequency'
        ivi.add_group_capability(self, cls+grp)
        
        self._advanced_power_line_frequency = 60.0
        
        self._add_property('advanced.power_line_frequency',
                        self._get_advanced_power_line_frequency,
                        self._set_advanced_power_line_frequency)
        
    def _get_advanced_power_line_frequency(self):
        return self._advanced_power_line_frequency
    
    def _set_advanced_power_line_frequency(self, value):
        value = float(value)
        self._advanced_power_line_frequency = value
