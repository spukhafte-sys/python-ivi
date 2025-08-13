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

from .. import ivi
from .. import swtch
from .. import extra
from .  import agilentCardSwitch


BIT, BYTE, WORD, LWORD = (1,2,4,8)

class Dio:
    def init(self, rack, slot_id):
        DIOS = ((90, 1, BYTE),
                (91, 4, BIT),) 

        SPECS = ( # Static specifications
            ('_dio_characteristics_output_dc_voltage_high', 2.4),
            ('_dio_characteristics_output_dc_voltage_low', 0.8),
            ('_dio_characteristics_output_dc_current_high', 0.001),
            ('_dio_characteristics_output_dc_current_low', -0.100),
            ('_dio_characteristics_input_dc_voltage_high', 2.0),
            ('_dio_characteristics_input_dc_voltage_low', 0.8),
            ('_dio_slot_id', slot_id),
            ('_dio_group_id', 0),
            )

        for start, count, mask in DIOS:
            for i in range(start, start+count):
                getattr(rack, '_dio_name').append(f'D{i:03d}')
                getattr(rack, '_dio_address').append(i)
                getattr(rack, '_dio_mask').append(mask)


OptionCardMapping = {
        'BUILD-IN DIO 3499': Dio,
        'RELAY MUX 44470': agilentCardSwitch.agilent44470A,
        'GP RELAY 44471': agilentCardSwitch.agilent44471A,
        'VHF SW 44472': agilentCardSwitch.agilent44472A,
        'DIGITAL IO 44474': agilentCardSwitch.agilent44474A,
        }


class Base(swtch.Base):
    """Agilent IVI Switch Driver
    
       Parent class for Agilent switches
    """

    # SCPI command mapping
    CMD_CTYPE = 'syst:ctype? %s'
    CMD_DISP = 'diag:disp:info "%s"'
    CMD_ROUT = 'rout:%s (@%s);'
    CMD_DIO_READ = 'sens:dig:data:%s? %s'
    CMD_DIO_WRITE = 'sour:dig:data:%s %s,%s'

    BUILT_IN_DIO = True  # For 3499
    
    def __init__(self, *args, cache=False, **kwargs):
        if cache:
            raise InvalidOptionValueException('Cache not supported by driver (use cache=False)')

        if not hasattr(self, '_instrument_id'):
            self._instrument_id = '3499'
        
        super().__init__(*args, **kwargs)
        
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

        self._cards = list()

        offset = 0 if self.BUILT_IN_DIO else 1
        for slot in range(offset, self.SLOT_COUNT + 1):
            card_info = self._ask(self.CMD_CTYPE % f'{slot:d}').split(',')
            card_type = ' '.join(card_info[0].split())  # Remove redundant whitespace
            if card_type in OptionCardMapping:
                card = OptionCardMapping[card_type]()  # Instantiate card
                card.init(self, slot)
                self._cards.append(card)

        self.channels._set_list(self._channel_name)
        if len(self._relay_name):
            self.relays._set_list(self._relay_name)
        if len(self._dio_name):
            self.dios._set_list(self._dio_name)

    def _path_can_connect(self, channel1, channel2):
        return False

    def _path_connect(self, channel1, channel2):
        channel1 = ivi.get_index(self._channel_name, channel1)
        channel2 = ivi.get_index(self._channel_name, channel2)

        slot = self._channel_slot_id[channel1]
        if slot != self._channel_slot_id[channel2]:
            raise swtch.PathNotFoundException
        else:
            return self._cards[slot].path_connect(self, channel1, channel2)

    def _path_disconnect(self, channel1, channel2):
        channel1 = ivi.get_index(self._channel_name, channel1)
        channel2 = ivi.get_index(self._channel_name, channel2)

        slot = self._channel_slot_id[channel1]
        if slot != self._channel_slot_id[channel2]:
            raise swtch.PathNotFoundException
        else:
            return self._cards[slot].path_disconnect(self, channel1, channel2)

    def _path_disconnect_all(self, channel1, channel2):
        raise swtch.PathNotFoundException

    def _get_display_title(self):
        return (self._display_title)

    def _set_display_title(self, value):
        self._display_title = str(value).upper()
        if not self._driver_operation_simulate:
            self._write(self.CMD_DISP % self._display_title)

    def _relay_open(self, *args):
        return self._relay_action(False, *args)

    def _relay_close(self, *args):
        return self._relay_action(True, *args)

    def _relay_action(self, action, *args):
        clist = []
        for i in args:
            if isinstance(i, str) or isinstance(i, int):
                clist.append(self._relay_address[ivi.get_index(self._relay_name, i)])
            else:
                raise SelectorNameException

        self._write(self.CMD_ROUT % (('close' if action else 'open'), ','.join(map(str,clist))))

    def _get_dio(self, address, size):
        return int(self._ask(self.CMD_DIO_READ % (size, address)))

    def _set_dio(self, address, size, value):
        self._write(self.CMD_DIO_WRITE % (size, address, value))

    def _get_dio_bit(self, index):
        return self._get_dio(self._dio_address[index], 'bit')

    def _get_dio_byte(self, index):
        return self._get_dio(self._dio_address[index], 'byte')

    def _get_dio_word(self, index):
        return self._get_dio(self._dio_address[index], 'word')

    def _set_dio_bit(self, index, value):
        self._set_dio(self._dio_address[index], 'bit', int(value)) 

    def _set_dio_byte(self, index, value):
        self._set_dio(self._dio_address[index], 'byte', int(value)) 

    def _set_dio_word(self, index, value):
        self._set_dio(self._dio_address[index], 'word', int(value)) 

