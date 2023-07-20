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

# Exceptions
class ChannelNotEnabledException(ivi.IviException): pass

# Parameter Values
#ApertureTimeUnits = set(['seconds', 'powerline_cycles'])
Auto = set(['off', 'on', 'once'])
Auto2 = set(['off', 'on'])
LoadMode = set(['constant_current', 'constant_voltage', 'constant_resistance', 'constant_power',])
Slope = set(['positive', 'negative'])

class Base(ivi.IviContainer):
    "Base methods for electronic loads with multiple channels"
    
    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        
        cls = 'Load'
        grp = 'Base'
        ivi.add_group_capability(self, cls+grp)
        
        self._channel_count = 1
        self._channel = 0
        self._channel_name = []
        self._channel_mode = []
        self._channel_input_enabled = list()
        self._channel_input_shorted = list()
        self._channel_voltage_range = list()
        self._channel_voltage_range_auto = list()
        self._channel_voltage_on = list()
        self._channel_voltage_off = list()
        self._channel_voltage_protection = list()
        self._channel_current_range = list()
        self._channel_current_range_auto = list()
        self._channel_current_slew = list()
        self._channel_current_slew_rise = list()
        self._channel_current_slew_fall = list()
        self._channel_current_protection = list()
        self._channel_power_protection = list()
        self._channel_resistance = list()
        
        self._add_property('channel',
            self._get_channel,
            self._set_channel,
            None,
            ivi.Doc("""
            Selects channel on loads with multiple channels.
            """))
        self._add_property('name',
            self._get_name,
            self._set_name,
            None,
            ivi.Doc("""
            This attribute returns the repeated capability identifier defined by
            specific driver for the channel that corresponds to the index that the
            user specifies. If the driver defines a qualified channel name, this
            property returns the qualified name.

            If the value that the user passes for the Index parameter is less than
            zero or greater than the value of the channel count, the attribute raises
            a SelectorRangeException.
            """, cls, grp, 'N/A'))
        self._add_property('channels[].name',  # Demo multiple addressable channels
            self._get_channel_name,
            self._set_channel_name,
            None,
            ivi.Doc("""
            This attribute returns the repeated capability identifier defined by
            specific driver for the channel that corresponds to the index that the
            user specifies. If the driver defines a qualified channel name, this
            property returns the qualified name.

            If the value that the user passes for the Index parameter is less than
            zero or greater than the value of the channel count, the attribute raises
            a SelectorRangeException.
            """, cls, grp, 'N/A'))
        self._add_property('mode',
            self._get_mode,
            self._set_mode,
            None,
            ivi.Doc("""
            Input mode of the load.
            """))
        self._add_property('input.enabled',
            self._get_input_enabled,
            self._set_input_enabled,
            None,
            ivi.Doc("""
            Input state.
            """))
        self._add_property('input.shorted',
            self._get_input_shorted,
            self._set_input_shorted,
            None,
            ivi.Doc("""
            Input is shorted.
            """))
        self._add_property('voltage.range',
            self._get_voltage_range,
            self._set_voltage_range,
            None,
            ivi.Doc("""
            Set range given a maximum voltage.
            """))
        self._add_property('voltage.range_auto',
            self._get_voltage_range_auto,
            self._set_voltage_range_auto,
            None,
            ivi.Doc("""
            Set range given a maximum voltage.
            """))
        self._add_property('voltage.on',
            self._get_voltage_on,
            self._set_voltage_on,
            None,
            ivi.Doc("""
            Enable load at or above this voltage.
            """))
        self._add_property('voltage.off',
            self._get_voltage_off,
            self._set_voltage_off,
            None,
            ivi.Doc("""
            Disable load at or below this voltage.
            """))
        self._add_property('voltage.protection',
            self._get_voltage_protection,
            self._set_voltage_protection,
            None,
            ivi.Doc("""
            Disable load at or above this voltage.
            """))
        self._add_method('voltage.read',
            self._get_voltage,
            ivi.Doc("""
            Measure and return voltage across load.
            """))
        self._add_method('voltage.min.fetch',
            self._get_voltage,
            ivi.Doc("""
            Measure and return minimum voltage across load.
            """))
        self._add_method('voltage.max.fetch',
            self._get_voltage,
            ivi.Doc("""
            Measure and return maximum voltage across load.
            """))
        self._add_method('voltage.ptp.fetch',
            self._get_voltage,
            ivi.Doc("""
            Measure and return peak-to-peak ripple voltage across load.
            """))
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

        self._init_channels()

    def _init_channels(self):
        try:
            super(Base, self)._init_channels()
        except AttributeError:
            pass

        for i in range(self._channel_count):
            self._channel_mode.append('constant_current')
            self._channel_name.append(f'CH{i+1:d}')
            self._channel_input_enabled.append(False)
            self._channel_input_shorted.append(False)
            self._channel_voltage_range.append(0)
            self._channel_voltage_range_auto.append(True)
            self._channel_voltage_on.append(0.1)
            self._channel_voltage_off.append(0)
            self._channel_voltage_protection.append(0)
            self._channel_current_range.append(0)
            self._channel_current_range_auto.append(True)
            self._channel_current_slew.append(0)
            self._channel_current_slew_rise.append(0)
            self._channel_current_slew_fall.append(0)
            self._channel_current_protection.append(0)
            self._channel_power_protection.append(0)
            self._channel_resistance.append(None)

        self.channels._set_list(self._channel_name)

    def _get_channel(self):
        return self._channel

    def _set_channel(self, index):
        # Set channel using either channel name or index
        self._channel = ivi.get_index(self._channel_name, index)

    def _get_name(self):
        return self._channel_name[self.channel]

    def _set_name(self, value):
        # Set name of current channel
        self._channel_name[self._channel] = str(value)

    def _get_channel_name(self, index):
        return self._channel_name[self.channel]

    def _set_channel_name(self, index, value):
        # Set name of current channel
        index = ivi.get_index(self._channel_name, index)
        self._channel_name[index] = str(value)

    def _get_mode(self):
        return self._channel_mode[self._channel]
    
    def _set_mode(self, value):
        if value in LoadMode:
            self._channel_mode[self._channel] = value
        else:
            raise ivi.ValueNotSupportedException()

    def _get_input_enabled(self):
        return self._channel_input_enabled[self._channel]

    def _set_input_enabled(self, value):
        self._channel_input_enabled[self._channel] = bool(value)
    
    def _get_input_shorted(self):
        return self._channel_input_shorted[self._channel]

    def _set_input_shorted(self, value):
        self._channel_input_shorted[self._channel] = bool(value)

    def _get_voltage_range(self):
        return self._channel_voltage_range[self._channel]
    
    def _set_voltage_range(self, value):
        self._channel_voltage_range[self._channel] = float(value)

    def _get_voltage_range_auto(self):
        return self._channel_voltage_auto[self._channel]

    def _set_voltage_range_auto(self, value):
        self._channel_voltage_auto[self._channel] = bool(value)

    def _get_voltage_on(self):
        return self._channel_voltage_on[self._channel]
    
    def _set_voltage_on(self, value):
        self._channel_voltage_on[self._channel] = float(value)

    def _get_voltage_off(self):
        return self._channel_voltage_off[self._channel]
    
    def _set_voltage_off(self, value):
        self._channel_voltage_off[self._channel] = float(value)

    def _get_voltage_protection(self):
        return self._channel_voltage_off[self._channel]
    
    def _set_voltage_protection(self, value):
        self._channel_voltage_protection[self._channel] = float(value)

    def _get_current_range(self):
        return self._channel_current_range[self._channel]
    
    def _set_current_range(self, value):
        self._channel_current_range[self._channel] = float(value)

    def _get_current_range_auto(self):
        return self._channel_current_auto[self._channel]

    def _set_current_range_auto(self, value):
        self._channel_current_auto[self._channel] = bool(value)

    def _get_current_slew(self):
        return self._channel_current_slew[self._channel]

    def _set_current_slew(self, value):
        self._channel_current_slew[self._channel] = float(value)

    def _get_current_slew_rise(self):
        return self._channel_current_slew_rise[self._channel]

    def _set_current_slew_rise(self, value):
        self._channel_current_slew_rise[self._channel] = float(value)

    def _get_current_slew_fall(self):
        return self._channel_current_slew_fall[self._channel]

    def _set_current_slew_fall(self, value):
        self._channel_current_slew_fall[self._channel] = float(value)

    def _get_current_protection(self):
        return self._channel_current_protection[self._channel]

    def _set_current_protection(self, value):
        self._channel_current_protection[self._channel] = float(value)

    def _get_resistance(self):
        return self._channel_resistance[self._channel]

    def _set_resistance(self, value):
        self._channel_resistance[self._channel] = float(value)

    def _get_voltage(self):
        return 0
    

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
"""   
class ACMeasurement(ivi.IviContainer):
    "Extension methods for electronic loads that can take AC voltage or AC current measurements"
    
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
"""   
class TriggerSlope(ivi.IviContainer):
    """Extension methods for electronic loads that can specify the polarity of
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
    "Extension methods for electronic loads that can initiate a measurement based on a software trigger signal"
    
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
"""   
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
    "Extension methods for electronic loads that can return the actual range value when auto ranging"
    
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
    "Extension methods for electronic loads that can take an auto zero reading"
    
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
    "Extension methods for electronic loads that can specify the power line frequency"
    
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
"""
