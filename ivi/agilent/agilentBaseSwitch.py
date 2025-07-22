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

#import time
#import struct

from .. import ivi
from .. import swtch
from .. import scpi

SwitchCommandMapping = {
        'dc_volts': 'volt',
        'ac_volts': 'volt:ac',
        'dc_current': 'curr',
        'ac_current': 'curr:ac',
        'continuity': 'cont',
        'diode': 'diod'}

class dio:
    def init(self, rack, slot):
        DIOS = ((90,4),
                (91,1), (92,1), (93,1), (94,1)) 

        for i,j in DIOS:
            vars(rack).setdefault('_dio_name', []).append(f'DIN{slot:d}{i}')
            vars(rack).setdefault('_dio_size', []).append(j)

class agilent44470:
    def init(self, rack, slot):
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
                    ('_channel_slot', slot),
                   )

        for i in range(CHANNEL_COUNT):
            channel_address = slot * 100 + i
            vars(rack).setdefault('_channel_name', []).append(f'CH{channel_address}')
            vars(rack).setdefault('_channel_address', []).append(channel_address)

            for j, k in SPECS:
                vars(rack).setdefault(j, []).append(k)

        for i in range(COMMON_COUNT):
            pass

    def path_connect(self):
        pass

class agilent44471:
    @classmethod
    def init(cls, rack, slot):
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
                    ('_channel_slot', slot),
                   )

        for i in range(CHANNEL_COUNT):
            channel_address = slot * 100 + i
            vars(rack).setdefault('_channel_name', []).append(f'CH{channel_address}')
            vars(rack).setdefault('_channel_address', []).append(channel_address)

        for j, k in SPECS:
            vars(rack).setdefault(j, []).append(k)

    @classmethod
    def path_connect(cls, channel1, channel2):
        pass


OptionCardMapping = {
        'BUILD-IN DIO 3499': dio,
        'GP RELAY 44471': agilent44471,
        }


class agilentBaseSwitch(scpi.swtch.Base):
    """Agilent IVI Switch Driver
    
       Parent class for all Agilent SCPI switches
    """

    BUILT_IN_DIO_COUNT = 1
    
    def __init__(self, *args, cache=False, **kwargs):
        if cache:
            raise InvalidOptionValueException('Cache not supported by driver (use cache=False)')

        if not hasattr(self, '_instrument_id'):
            self._instrument_id = '3499'
        
        super().__init__(*args, **kwargs)
        
        self._channel_count = 101
        self._memory_size = 5

        self._identity_description = "Agilent 3499 IVI Switch Driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent Technologies, Inc."
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 4
        self._identity_specification_minor_version = 1
        self._identity_supported_instrument_models = ['3499A', '3499B', '3499C']

    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."
        
        # The initialize() method is added and called at the end of ivi.py/Driver/__init__()
        # and points to (this) _initialize()
        super()._initialize(resource, id_query, reset, **keywargs)
        
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

        self._init_cards()

    def _init_cards(self):
        # Scan option cards

        self._slot = list()

        for slot in range(0, self.BUILT_IN_DIO_COUNT + self.SLOT_COUNT):
            card_info = self._ask(f'syst:ctyp? {slot:d}').split(',')
            card_type = ' '.join(card_info[0].split())  # Remove redundant whitespace
            if card_type in OptionCardMapping:
                card = OptionCardMapping[card_type]()  # Instantiate card
                card.init(self, slot)
                self._slot.append(card)

        self.dios._set_list(self._dio_name)
        self.channels._set_list(self._channel_name)

    def _path_can_connect(self, channel1, channel2):
        return False

    def _path_connect(self, channel1, channel2):
        channel1 = ivi.get_index(self._channel_name, channel1)
        channel2 = ivi.get_index(self._channel_name, channel2)

        slot = self._channel_slot(channel1)
        if slot != self._channel_slot(channel2):
            raise swtch.PathNotFoundException
        else:
            return self._slot[self.slot].path_connect(self, slot)

    def _path_disconnect(self, channel1, channel2):
        raise swtch.PathNotFoundException

    def _path_disconnect_all(self, channel1, channel2):
        raise swtch.PathNotFoundException

    def _get_display_title(self):
        return (self._display_title)

    def _set_display_title(self, value):
        self._display_title = str(value).upper()
        if not self._driver_operation_simulate:
            self._write(f'diag:disp:info "{self._display_title}"')

    def relay(self, action, *args):
        clist = ''
        for i in args:
            if isinstance(i, str) or isinstance(i, int):
                clist += str(self._channel_address[ivi.get_index(self._channel_name, i)]) + ','
            else:
                raise SelectorNameException

        self._write('rout:' + ('clos' if action else 'open') + f' (@{clist});')
