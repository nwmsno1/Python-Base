import sys
import time
from datetime import datetime, timedelta
from os.path import join
import matplotlib.pyplot as plt
import numpy as np
from automonitor import conn_visa


def arfcn2freq(arfcn, uplink=False, band='900'):
    if band == '900':
        if not 1 <= arfcn <= 124:
            raise ValueError('ARFCN must be in the range of 1~124 on band of %s' % band)
        if uplink:
            freq = 890 + 0.2 * arfcn
        else:
            freq = 890 + 0.2 * arfcn + 45
    elif band == '1900':
        if not 512 <= arfcn <= 810:
            raise ValueError('ARFCN must be in the range of 512~810 on band of %s' % band)
        if uplink:
            freq = 1850.2 + 0.2 * (arfcn-512)
        else:
            freq = 1850.2 + 0.2 * (arfcn-512) + 80
    else:
        raise ValueError('band must be in \'900\' or \'1900\'')
    return freq * 1e6


class SAMonitor(conn_visa.visainst):
    def __init__(self, inst_id):
        super(SAMonitor, self).__init__(inst_id)
        self.write("*CLS")
        self.write("INSTrument:NSELect EDGEGSM")

    def pferror(self):
        for i in range(10):
            try:
                result = self.query(':FETCh:PFERror?')
                return np.fromstring(result, dtype=float, sep=',')
            except:
                if i >= 9:
                    raise TimeoutError('SA requests time out')
                else:
                    pass

    @property
    def center_freq(self):
        return float(self.query('SENSe:FREQuency:RF:CENTer?'))

    @center_freq.setter
    def center_freq(self, value):
        self.write('SENSe:FREQuency:RF:CENTer %f' % value)

    @property
    def band(self):
        return self.query('SENSe:RAD:STAN:BAND?')

    @band.setter
    def band(self, band_name):
        self.write('SENSe:RAD:STAN:BAND %s' % band_name)

    @property
    def trig_source(self):
        return self.query(':PFERror:TRIGger:SOURce?')

    @trig_source.setter
    def trig_source(self, source):
        self.write(':PFERror:TRIGger:SOURce %s' % source)

    @property
    def burst(self):
        return self.query('SENSe:CHAN:BURST?')

    @burst.setter
    def burst(self, mod='NORM'):
        self.write('SENSe:CHAN:BURST %s' % mod)

    @property
    def slot(self):
        return self.query('SENSe:CHAN:SLOT?')

    @slot.setter
    def slot(self, num):
        try:
            if num.lower() == 'off':
                self.write('SENSe:CHAN:SLOT:AUTO 0')
        except:
            self.write('SENSe:CHAN:SLOT:AUTO 1')
            self.write('SENSe:CHAN:SLOT %d' % num)

    @property
    def arfcn(self):
        return self.query('CHANnel:ARFCn?')

    @arfcn.setter
    def arfcn(self, num):
        self.write('CHANnel:ARFCn %d' % num)

    def t0_offset(self):
        return self.pferror()[9]


if __name__ == '__main__':
    sa = SAMonitor('GPIB0::xx::INSTR')
    sa.band = 'PCS1900'
    sa.trig_source = 'EXT1'
    sa.arfcn = 521
    sa.slot = 0
    print(sa.t0_offset())
