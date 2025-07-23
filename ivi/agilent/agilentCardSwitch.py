"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2012-2017 Alex Forencich
Copyright (c) 2025 Fred Fierling

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

from .. import swtch

class agilent44470A:
    'Agilent 10-Channel MUX Module'

    @staticmethod
    def init(rack, slot_id):
        CHANNEL_COUNT = 10
        COMMON_COUNT = 1

        SPECS = ( # Static specifications
                    ('_channel_characteristics_ac_current_carry_max', 2),
                    ('_channel_characteristics_ac_current_switching_max', 2),
                    ('_channel_characteristics_ac_power_carry_max', 500),
                    ('_channel_characteristics_ac_power_switching_max', 500),
                    ('_channel_characteristics_ac_voltage_max', 250),
                    ('_channel_characteristics_bandwidth', 10e6),
                    ('_channel_characteristics_impedance', 50),
                    ('_channel_characteristics_dc_current_carry_max', 2),
                    ('_channel_characteristics_dc_current_switching_max', 2),
                    ('_channel_characteristics_dc_power_carry_max', 60),
                    ('_channel_characteristics_dc_power_switching_max', 60),
                    ('_channel_characteristics_dc_voltage_max', 250),
                    ('_channel_is_configuration_channel', False),
                    ('_channel_is_source_channel', False),
                    ('_channel_characteristics_settling_time', 0.1),  # Guessed
                    ('_channel_characteristics_wire_mode', 0),
                    ('_channel_slot_id', slot_id),
                    ('_channel_group_id', 0),
                   )

        for i in range(CHANNEL_COUNT):
            address = slot_id * 100 + i
            vars(rack).setdefault('_channel_name', []).append(f'CH{address:03d}')
            vars(rack).setdefault('_channel_address', []).append(address)
            vars(rack).setdefault('_channel_is_common_channel', []).append(False)

            for j, k in SPECS:
                vars(rack).setdefault(j, []).append(k)

        for i in range(COMMON_COUNT):
            vars(rack).setdefault('_channel_name', []).append(f'COM{address:d}')
            vars(rack).setdefault('_channel_address', []).append(None)
            vars(rack).setdefault('_channel_is_common_channel', []).append(True)

            for j, k in SPECS:
                vars(rack).setdefault(j, []).append(k)

    @staticmethod
    def path_connect(rack, *channels):
        rack.relay(CLOSE, *[i for i in channels if not rack._channels_is_common_channel[i]])
            
    @staticmethod
    def path_disconnect(rack, *channels):
        rack.relay(OPEN, *[i for i in channels if not rack._channels_is_common_channel[i]])
            

class agilent44471A:
    'Agilent 10-Channel GP Relay Module'

    @staticmethod
    def init(rack, slot_id):
        CHANNEL_COUNT = 10

        SPECS = ( # Static specifications
                    ('_channel_characteristics_ac_current_carry_max', 2),
                    ('_channel_characteristics_ac_current_switching_max', 2),
                    ('_channel_characteristics_ac_power_carry_max', 500),
                    ('_channel_characteristics_ac_power_switching_max', 500),
                    ('_channel_characteristics_ac_voltage_max', 250),
                    ('_channel_characteristics_bandwidth', 10e6),
                    ('_channel_characteristics_impedance', 50),
                    ('_channel_characteristics_dc_current_carry_max', 2),
                    ('_channel_characteristics_dc_current_switching_max', 2),
                    ('_channel_characteristics_dc_power_carry_max', 60),
                    ('_channel_characteristics_dc_power_switching_max', 60),
                    ('_channel_characteristics_dc_voltage_max', 250),
                    ('_channel_is_configuration_channel', False),
                    ('_channel_is_source_channel', False),
                    ('_channel_characteristics_settling_time', 0.1),  # Guessed
                    ('_channel_characteristics_wire_mode', 0),
                    ('_channel_slot_id', slot_id),
                    ('_channel_group_id', 0),
                   )

        for i in range(CHANNEL_COUNT):
            address = slot_id * 100 + i
            vars(rack).setdefault('_channel_name', []).append(f'CH{address:03d}')
            vars(rack).setdefault('_channel_address', []).append(address)
            vars(rack).setdefault('_channel_is_common_channel', []).append(False)

            for j, k in SPECS:
                vars(rack).setdefault(j, []).append(k)

    @staticmethod
    def path_connect(rack, *channels):
        raise swtch.PathNotFoundException  # GP relays have no paths

    @staticmethod
    def path_disconnect(rack, *channels):
        raise swtch.PathNotFoundException  # GP relays have no paths

class agilent44472A:
    'Agilent Dual 4-Channel VHF Module'

    @staticmethod
    def init(rack, slot_id):
        CHANNEL_COUNT = 10

        SPECS = ( # Static specifications
                    ('_channel_characteristics_ac_current_carry_max', 0.3),
                    ('_channel_characteristics_ac_current_switching_max', 0.3),
                    ('_channel_characteristics_ac_power_carry_max', 9),
                    ('_channel_characteristics_ac_power_switching_max', 9),
                    ('_channel_characteristics_ac_voltage_max', 30),
                    ('_channel_characteristics_bandwidth', 300e6),
                    ('_channel_characteristics_impedance', 50),
                    ('_channel_characteristics_dc_current_carry_max', 0.03),
                    ('_channel_characteristics_dc_current_switching_max', 0.03),
                    ('_channel_characteristics_dc_power_carry_max', 7.5),
                    ('_channel_characteristics_dc_power_switching_max', 7.5),
                    ('_channel_characteristics_dc_voltage_max', 250),
                    ('_channel_is_configuration_channel', False),
                    ('_channel_is_source_channel', False),
                    ('_channel_characteristics_settling_time', 0.1),  # Guessed
                    ('_channel_characteristics_wire_mode', 0),
                    ('_channel_slot_id', slot_id),
                    ('_channel_group_id', 0),
                   )

        for i in range(CHANNEL_COUNT):
            address = slot_id * 100 + i
            vars(rack).setdefault('_channel_name', []).append(f'CH{address:03d}')
            vars(rack).setdefault('_channel_address', []).append(address)
            vars(rack).setdefault('_channel_is_common_channel', []).append(False)

            for j, k in SPECS:
                vars(rack).setdefault(j, []).append(k)

    @staticmethod
    def path_connect(rack, *channels):
        raise swtch.PathNotFoundException  # GP relays have no paths

    @staticmethod
    def path_disconnect(rack, *channels):
        raise swtch.PathNotFoundException  # GP relays have no paths


class agilent44474A:
    'Agilent 16-Bit Digital I/O Module'

    @staticmethod
    def init(rack, slot_id):
        CHANNEL_COUNT = 10
