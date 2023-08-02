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
LoadMode = set(['constant_current', 'constant_voltage', 'constant_resistance', 'constant_power',])

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
        self._channel_voltage_constant = []
        self._channel_voltage_range = []
        self._channel_voltage_on = []
        self._channel_voltage_off = []
        self._channel_current_constant = []
        self._channel_current_range = []
        self._channel_current_slew = []
        self._channel_current_slew_rise = []
        self._channel_current_slew_fall = []
        self._channel_current_protection = []
        self._channel_power_constant = []
        self._channel_power_protection = []
        self._channel_resistance_constant = []

        # Properties
        self._add_property('channel',
            self._get_channel,
            self._set_channel,
            None,
            ivi.Doc("""
            Selects the current channel on instruments with multiple channels.
            """))
        self._add_property('name',
            self._get_name,
            self._set_name,
            None,
            ivi.Doc("""
            This attribute is the name of the currently selected channel.
            The index can be the channel's numeric index or name.

            If the value that the user passes for the Index parameter is less than
            zero or greater than the value of the channel count, the attribute raises
            a SelectorRangeException.
            """, cls, grp, 'N/A'))
        self._add_property('channels[].name',  # Demo multiple addressable channels
            # Use this as a template to add support for multi-channel instruments
            self._get_channel_name,
            self._set_channel_name,
            None,
            ivi.Doc("""
            This attribute is the name associated with the channel at the specified index.
            The index can be the channel's numeric index or name.

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
            If True, the input is enabled.
            """))
        self._add_property('input.shorted',
            self._get_input_shorted,
            self._set_input_shorted,
            None,
            ivi.Doc("""
            If True, the input is shorted.
            """))
        self._add_property('voltage.constant',
            self._get_voltage_constant,
            self._set_voltage_constant,
            None,
            ivi.Doc("""
            Load voltage in constant voltage mode. (V)
            """))
        self._add_property('voltage.range',
            self._get_voltage_range,
            self._set_voltage_range,
            None,
            ivi.Doc("""
            Maximum voltage for voltage range. (V)
            """))
        self._add_property('voltage.on',
            self._get_voltage_on,
            self._set_voltage_on,
            None,
            ivi.Doc("""
            Enable load at or above this voltage. (V)
            """))
        self._add_property('voltage.off',
            self._get_voltage_off,
            self._set_voltage_off,
            None,
            ivi.Doc("""
            Disable load at or below this voltage. (V)
            """))
        self._add_property('current.constant',
            self._get_current_constant,
            self._set_current_constant,
            None,
            ivi.Doc("""
            Load current in constant current mode. (A)
            """))
        self._add_property('current.range',
            self._get_current_range,
            self._set_current_range,
            None,
            ivi.Doc("""
            Maximum current for current range. (A)
            """))
        self._add_property('current.slew',
            self._get_current_slew,
            self._set_current_slew,
            None,
            ivi.Doc("""
            Rate at which current changes in response programmed current changes. (A/us)

            Sets rise and fall slew rate in instrument.
            """))
        self._add_property('current.slew_rise',
            self._get_current_slew_rise,
            self._set_current_slew_rise,
            None,
            ivi.Doc("""
            Rate at which current decreases in response programmed current changes. (A/µs)
            """))
        self._add_property('current.slew_fall',
            self._get_current_slew_fall,
            self._set_current_slew_fall,
            None,
            ivi.Doc("""
            Rate at which current increases in response programmed current changes. (A/µs)
            """))
        self._add_property('current.protection',
            self._get_current_protection,
            self._set_current_protection,
            None,
            ivi.Doc("""
            Disable load at or below this current. (A)
            """))
        self._add_property('power.constant',
            self._get_power_constant,
            self._set_power_constant,
            None,
            ivi.Doc("""
            Load power for constant power mode. (W)
            """))
        self._add_property('power.protection',
            self._get_power_protection,
            self._set_power_protection,
            None,
            ivi.Doc("""
            Disable load at or below this power. (W)
            """))
        self._add_property('resistance.constant',
            self._get_resistance_constant,
            self._set_resistance_constant,
            None,
            ivi.Doc("""
            Load resistance in constant resistance mode. (Ω)
            """))

        # Methods
        self._add_method('voltage.measure',
            self._measure_voltage,
            ivi.Doc("""
            Measure and return voltage across load.
            """))
        self._add_method('voltage.min.measure',
            self._measure_min_voltage,
            ivi.Doc("""
            Measure and return minimum voltage across load.
            """))
        self._add_method('voltage.max.measure',
            self._measure_max_voltage,
            ivi.Doc("""
            Measure and return maximum voltage across load.
            """))
        self._add_method('voltage.ptp.measure',
            self._measure_ptp_voltage,
            ivi.Doc("""
            Measure and return peak-to-peak ripple voltage across load.
            """))
        self._add_method('current.measure',
            self._measure_current,
            ivi.Doc("""
            Measure and return current through load.
            """))
        self._add_method('current.min.measure',
            self._measure_min_current,
            ivi.Doc("""
            Measure and return minimum current through load.
            """))
        self._add_method('current.max.measure',
            self._measure_max_current,
            ivi.Doc("""
            Measure and return maximum current through load.
            """))
        self._add_method('current.ptp.measure',
            self._measure_ptp_current,
            ivi.Doc("""
            Measure and return peak-to-peak ripple current through load.
            """))
        self._add_method('power.measure',
            self._measure_power,
            ivi.Doc("""
            Measure and return power dissipated by load.
            """))
        self._add_method('resistance.measure',
            self._measure_resistance,
            ivi.Doc("""
            Compute and return load resistance.

            Can return infinity.
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
            self._channel_voltage_constant.append(0)
            self._channel_voltage_range.append(0)
            self._channel_voltage_on.append(0.1)
            self._channel_voltage_off.append(0)
            self._channel_current_constant.append(0)
            self._channel_current_range.append(0)
            self._channel_current_slew.append(0)
            self._channel_current_slew_rise.append(0)
            self._channel_current_slew_fall.append(0)
            self._channel_current_protection.append(0)
            self._channel_power_constant.append(0)
            self._channel_power_protection.append(0)
            self._channel_resistance_constant.append(None)

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

    def _get_voltage_constant(self):
        return self._channel_voltage_constant[self._channel]

    def _set_voltage_constant(self, value):
        self._channel_voltage_constant[self._channel] = float(value)

    def _get_voltage_range(self):
        return self._channel_voltage_range[self._channel]

    def _set_voltage_range(self, value):
        self._channel_voltage_range[self._channel] = float(value)

    def _get_voltage_on(self):
        return self._channel_voltage_on[self._channel]

    def _set_voltage_on(self, value):
        self._channel_voltage_on[self._channel] = float(value)

    def _get_voltage_off(self):
        return self._channel_voltage_off[self._channel]

    def _set_voltage_off(self, value):
        self._channel_voltage_off[self._channel] = float(value)

    def _get_current_constant(self):
        return self._channel_current_constant[self._channel]

    def _set_current_constant(self, value):
        self._channel_current_constant[self._channel] = float(value)

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

    def _get_resistance_constant(self):
        return self._channel_resistance[self._channel]

    def _set_resistance_constant(self, value):
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
