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
        self._channel_input_enabled = []
        self._channel_input_shorted = []
        self._channel_voltage = []
        self._channel_voltage_range = []
        self._channel_voltage_on = []
        self._channel_voltage_off = []
        self._channel_current = []
        self._channel_current_range = []
        self._channel_current_slew = []
        self._channel_current_slew_rise = []
        self._channel_current_slew_fall = []
        self._channel_current_protection = []
        self._channel_power = []
        self._channel_power_protection = []
        self._channel_resistance = []

        # Properties
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
        self._add_property('current.setpoint',
            self._get_current,
            self._set_current,
            None,
            ivi.Doc("""
            Set range given a maximum current.
            """))
        self._add_property('current.range',
            self._get_current_range,
            self._set_current_range,
            None,
            ivi.Doc("""
            Set range given a maximum current.
            """))
        self._add_property('current.slew',
            self._get_voltage_off,
            self._set_voltage_off,
            None,
            ivi.Doc("""
            Disable load at or below this voltage.
            """))
        self._add_property('current.slew_rise',
            self._get_current_slew,
            self._set_current_slew,
            None,
            ivi.Doc("""
            Disable load at or below this voltage.
            """))
        self._add_property('current.slew_fall',
            self._get_current_slew_fall,
            self._set_current_slew_fall,
            None,
            ivi.Doc("""
            Disable load at or below this current.
            """))
        self._add_property('current.protection',
            self._get_current_protection,
            self._set_current_protection,
            None,
            ivi.Doc("""
            Disable load at or below this current.
            """))
        self._add_property('power.setpoint',
            self._get_power,
            self._set_power,
            None,
            ivi.Doc("""
            Disable load at or below this voltage.
            """))
        self._add_property('power.protection',
            self._get_power_protection,
            self._set_power_protection,
            None,
            ivi.Doc("""
            Disable load at or below this voltage.
            """))
        self._add_property('resistance',
            self._get_resistance,
            self._set_resistance,
            None,
            ivi.Doc("""
            Disable load at or below this voltage.
            """))

        # Methods
        self.voltage._add_method('measure',
            self._measure_voltage,
            ivi.Doc("""
            Measure and return voltage across load.
            """))
        self._add_method('measure.min.voltage',
            self._measure_min_voltage,
            ivi.Doc("""
            Measure and return minimum voltage across load.
            """))
        self._add_method('measure.max.voltage',
            self._measure_max_voltage,
            ivi.Doc("""
            Measure and return maximum voltage across load.
            """))
        self._add_method('measure.ptp.voltage',
            self._measure_ptp_voltage,
            ivi.Doc("""
            Measure and return peak-to-peak ripple voltage across load.
            """))
        self._add_method('measure.current',
            self._measure_current,
            ivi.Doc("""
            Measure and return current across load.
            """))
        self._add_method('measure.min.current',
            self._measure_min_current,
            ivi.Doc("""
            Measure and return minimum current across load.
            """))
        self._add_method('measure.max.current',
            self._measure_max_current,
            ivi.Doc("""
            Measure and return maximum current across load.
            """))
        self._add_method('measure.ptp.current',
            self._measure_ptp_current,
            ivi.Doc("""
            Measure and return peak-to-peak ripple current across load.
            """))
        self._add_method('measure.power',
            self._measure_power,
            ivi.Doc("""
            Measure and return peak-to-peak ripple current across load.
            """))
        self._add_method('measure.resistance',
            self._measure_resistance,
            ivi.Doc("""
            Measure and return peak-to-peak ripple current across load.
            """))

        self._init_channels()

    def _init_channels(self):
        try:
            super(Base, self)._init_channels()
        except AttributeError:
            pass

        for i in range(self._channel_count):
            self._channel_name.append(f'CH{i+1:d}')
            self._channel_mode.append('constant_current')
            self._channel_input_enabled.append(False)
            self._channel_input_shorted.append(False)
            self._channel_voltage.append(0)
            self._channel_voltage_range.append(0)
            self._channel_voltage_on.append(0.1)
            self._channel_voltage_off.append(0)
            self._channel_current.append(0)
            self._channel_current_range.append(0)
            self._channel_current_slew.append(0)
            self._channel_current_slew_rise.append(0)
            self._channel_current_slew_fall.append(0)
            self._channel_current_protection.append(0)
            self._channel_power.append(0)
            self._channel_power_protection.append(0)
            self._channel_resistance.append(None)

        self.channels._set_list(self._channel_name)

    # Property functions
    def _get_channel(self):
        return self._channel

    def _set_channel(self, index):
        # Set channel using either channel name or index
        self._channel = ivi.get_index(self._channel_name, index)

    def _get_name(self):
        return self._channel_name[self._channel]

    def _set_name(self, value):
        # Set name of current channel
        self._channel_name[self._channel] = str(value)

    def _get_channel_name(self, index):
        return self._channel_name[self._channel]

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

    def _get_voltage(self):
        return self._channel_voltage[self._channel]

    def _set_voltage_range(self, value):
        self._channel_voltage[self._channel] = float(value)

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

    def _get_current(self):
        return self._channel_current[self._channel]

    def _set_current(self, value):
        self._channel_current[self._channel] = float(value)

    def _get_current_range(self):
        return self._channel_current_range[self._channel]

    def _set_current_range(self, value):
        self._channel_current_range[self._channel] = float(value)

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
        self._channel_power_protection[self._channel] = float(value)

    def _get_power_protection(self):
        return self._channel_power_protection[self._channel]

    def _set_power_protection(self, value):
        self._channel_power_protection[self._channel] = float(value)

    def _get_resistance(self):
        return self._channel_resistance[self._channel]

    def _set_resistance(self, value):
        self._channel_resistance[self._channel] = float(value)

    # Measurement functions
    def _measure_voltage(self):
        return None

    def _measure_min_voltage(self):
        return None

    def _measure_max_voltage(self):
        return None

    def _measure_ptp_voltage(self):
        return None

    def _measure_current(self):
        return None

    def _measure_min_current(self):
        return None

    def _measure_max_current(self):
        return None

    def _measure_ptp_current(self):
        return None

    def _measure_power(self):
        return None

    def _measure_resistance(self):
        return None
