
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

from .  import agilentBaseSwitch
from .. import ivi
from .. import swtch
from .. import extra

class agilent3488A(agilentBaseSwitch,
                   ivi.Driver,
                   swtch.Base,
                   extra.common.Title, extra.common.SerialNumber):
    "Agilent 3488A IVI Switch Driver"

    CMD_CTYPE = 'CTYPE %s'
    CMD_DISP_INFO = 'DISP %s'
    CMD_ROUT = '%s %s'

    BUILT_IN_DIO = False
    SLOT_COUNT = 2  # TODO change to 5 after testing with 3499B

    def _utility_reset(self):
        self._write('RESET')
