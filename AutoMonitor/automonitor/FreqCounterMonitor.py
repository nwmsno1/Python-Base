import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
from automonitor import conn_visa


def _isplot(pltdura, time_sleep, this_idx):
    if this_idx == 0:
        return False
    elif (this_idx + 1) * time_sleep // pltdura == this_idx * time_sleep // pltdura:
        return False
    else:
        return True

def freq_devi(freq_value):
    return (freq_value - 13000000 / 48) / ((13000000 / 48) / 1000000000)

def freq_2diff(value1, value2):
    return (value1 - value2) / ((13000000 / 48) / 1000000000)


# Connect to frequency counter using class visainst
# Input:    Instrument number as string
# Return:   class visainst
class FCMonitor(conn_visa.visainst):
    def __init__(self, inst_id):
        super(FCMonitor, self).__init__(inst_id)
        self.write("*CLS;MODE 3;AUTM 0;CLCK 1;CLKF 0;SRCE 1")
        self.freq1 = np.array([])
        self.freq2 = np.array([])

    @property
    def out_path(self):
        return self._out_path

    @out_path.setter
    def out_path(self, value):
        self._out_path = value

    @property
    def time_sleep(self):
        return self._time_sleep

    @time_sleep.setter
    def time_sleep(self, value):
        self._time_sleep = value

    def get_freq(self, chan=1):
        if chan not in [1, 2]:
            raise ValueError('Error channel number')
        value = float(self.query('MEASure:SCALar:VOLTage:FREQuency? (@%d)' % chan))
        if chan == 1:
            self.freq1 = np.append(self.freq1, value)
        elif chan == 2:
            self.freq2 = np.append(self.freq2, value)
        else:
            pass

    def get_freq_devi(self, chan=1):
        if chan == 1:
            return freq_devi(self.freq1)
        elif chan == 2:
            return freq_devi(self.freq2)
        else:
            raise ValueError('Error channel number')

    def get_freq_2diff(self):
        return freq_2diff(self.freq1, self.freq2)

    def plot(self, this_idx, time_now, wave):
        axis = np.arange(this_idx+1)*self._time_sleep
        plt.plot(axis, wave, color='blue', linewidth=2)
        plt.plot(axis, np.ones_like(wave)*5, color='gray', linewidth=3.5)
        plt.plot(axis, np.ones_like(wave)*-5, color='gray', linewidth=3.5)
        plt.xlim(np.min(axis), np.max(axis))
        plt.xlabel('Time (sec)')
        plt.savefig(self._out_path+'\\FC_%s.png' % time_now.strftime('%Y%m%d%H%M%S'))


def monitor_devi(fc, len, output):
    b_time = datetime.now()
    e_time = b_time + timedelta(seconds=len)
    while 1:
        fc.get_freq(chan=1)
        time.sleep(0.5)
        now_time = datetime.now()
        if now_time >= e_time:
            break
    devi = fc.get_freq_devi(chan=1)
    fc.freq1 = np.array([])
    output.put((devi, b_time, now_time))


def monitor_2chan(fc, len, output):
    b_time = datetime.now()
    e_time = b_time + timedelta(seconds=len)
    while 1:
        fc.get_freq(chan=1)
        fc.get_freq(chan=2)
        time.sleep(0.5)
        now_time = datetime.now()
        if now_time >= e_time:
            break
    devi = fc.get_freq_devi(chan=1)
    diff = fc.get_freq_2diff()
    fc.freq1 = np.array([])
    fc.freq2 = np.array([])
    output.put((devi, diff, b_time, now_time))


if __name__ == '__main__':
    inst_id = 'GPIB0::4::INSTR'
    fc = FCMonitor(inst_id)
