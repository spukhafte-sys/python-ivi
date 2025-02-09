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

import time
import struct

from .. import ivi
from .. import scpi
'''
MeasurementRangeMapping = {
        'dc_volts': 'volt:dc:range',
        'dc_current': 'curr:dc:range',
        }

MeasurementAutoRangeMapping = {
        'dc_volts': 'volt:dc:range:auto',
        'dc_current': 'curr:dc:range:auto',
        }
'''
class bk8542B(scpi.load.Base):
    "B&K Precision 8542BA single-channel electronic load driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'B&K Precision, 8542B')

        super(bk8542B, self).__init__(*args, **kwargs)
        
        self._identity_description = "B&K Precision 8542B electronic load driver"
        self._identity_instrument_manufacturer = "B&K Precision"
        self._identity_supported_instrument_models = ['8542B']

    def _initialize(self, resource=None, id_query=False, reset=False, **kwargs):

        super(bk8542B, self)._initialize(resource, id_query, reset, **kwargs)

        if reset:  # Only way to clear the input buffer?
            timeout = self._interface.timeout
            self._interface.timeout = 1
            try:
                while True:
                    self._interface.read()
            except:
                pass
            self._interface.timeout = timeout

    # This load only has one channel 
    def _get_channel(self):
        pass

    def _set_channel(self, index):
        pass

