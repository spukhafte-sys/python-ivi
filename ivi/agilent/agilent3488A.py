
"""

Python Interchangeable Virtual Instrument Library

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

from .. import extra
from .. import ivi
from .  import agilentSwitch
from .. import swtch

class agilent3488A(agilentSwitch.Base,
                   extra.common.Title, extra.common.SerialNumber,
                   swtch.Base,
                   ivi.Driver,
                   ):
    "Agilent 3488A IVI Switch Driver"

    CMD_CTYPE = 'CTYPE %s'
    CMD_DISP = 'DISP %s'
    CMD_ROUT = '%s %s'

    BUILT_IN_DIO = False
    SLOT_COUNT = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._identity_description = "Agilent 3488 IVI Switch Driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent Technologies, Inc."
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 4
        self._identity_specification_minor_version = 1
        self._identity_supported_instrument_models = ['3488A',]

    def _utility_reset(self):
        self._write('RESET')
