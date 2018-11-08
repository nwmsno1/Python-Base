import sys
import time
from datetime import datetime, timedelta
from os.path import join
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft, ifft
from automonitor import conn_visa


class OSMonitor(conn_visa.visainst):
    def __init__(self, inst_id):
        super(OSMonitor, self).__init__(inst_id)
        self.write("*CLS")
        self.write(':WAVeform:POINts:MODE ASCii')
        self.write(':WAVeform:FORMat ASCii')
        self.offset = np.array([])
        self.preamble = None

    def _check_data_string(self, data_str):
        pound = data_str[0:1]
        if pound != "#":
            print("PROBLEM: Invalid binary block format, pound char is '%s'." % pound)
            print("Exited because of problem.")
            sys.exit(1)
        data = np.fromstring(data_str[10:], dtype=float, sep=', ')
        return data

    def _get_preamble(self):
        # x_reference is always 0
        x_increment = float(self.query(":WAVeform:XINCrement?"))
        x_origin = float(self.query(":WAVeform:XORigin?"))
        y_increment = float(self.query(":WAVeform:YINCrement?"))
        y_origin = float(self.query(":WAVeform:YORigin?"))
        y_reference = float(self.query(":WAVeform:YREFerence?"))
        preamble = dict()
        preamble['x_increment'] = x_increment
        preamble['x_origin'] = x_origin
        preamble['y_increment'] = y_increment
        preamble['y_origin'] = y_origin
        preamble['y_reference'] = y_reference
        return preamble

    def _cal_axis(self, data, preamble):
        self.npts = data.shape[0]
        time_axis = np.zeros(self.npts)
        # voltage = np.zeros(npts)
        for i in range(self.npts):
            time_axis[i] = (preamble['x_origin'] + i * preamble['x_increment']) * 1000
            # voltage[i] = ((data[i] - preamble['y_reference']) * preamble['y_increment']) + preamble['y_origin']
        return time_axis

    def _read_data(self):
        data = []
        time_axis = []
        self.write(':SINGle')
        preamble = self._get_preamble()
        for i in range(4):
            self.write(':WAV:SOURce CHANnel%d' % (i+1))
            datastr = self.query(':WAVeform:DATA?')
            data.append(self._check_data_string(datastr))
            time_axis.append(self._cal_axis(data[i], preamble))
        delay = float(self.query(':MEASure:DELay? CHANnel1,CHANnel3'))
        self.write(':RUN')
        return data, preamble, time_axis, delay

    def single(self):
        self.write(':SINGle')

    def run(self):
        self.write(':RUN')

    def delay(self, scale=5e-8):
        self.write('TIMebase:SCALe %s' % str(scale))
        return float(self.query(':MEASure:DELay? CHANnel1,CHANnel3'))

    def delay24(self, scale=5e-4):
        self.write('TIMebase:SCALe %s' % str(scale))
        return float(self.query(':MEASure:DELay? CHANnel2,CHANnel4'))

    def get_ch_data(self, scale=5e-5):
        self.write('TIMebase:SCALe %s' % str(scale))

        # read data from channel1
        data, self.preamble, time_axis, delay = self._read_data()
        self.data_ch1 = data[0]
        self.time_axis_ch1 = time_axis[0]

        self.data_ch2 = data[1]
        self.time_axis_ch2 = time_axis[1]

        self.data_ch3 = data[2]
        self.time_axis_ch3 = time_axis[2]

        self.data_ch4 = data[3]
        self.time_axis_ch4 = time_axis[3]

        return delay

    def cc_freq(self):
        dat1 = self.data_ch2.copy()
        dat2 = self.data_ch4.copy()

        cc_func = ifft(fft(dat1)*fft(dat2))
        cc_coef = np.sum(cc_func)/(np.sqrt(np.sum(dat1**2)) * np.sqrt(np.sum(dat2**2)))
        return cc_coef

    def cc(self, delay=0):
        dat1 = self.data_ch2.copy()
        dat2 = self.data_ch4.copy()
        dt = self.preamble['x_increment']
        nt_delay = int(np.abs(delay)/dt)
        if delay < 0:
            dat1_new = dat1[nt_delay:]
            if nt_delay == 0:
                dat2_new = dat2
            else:
                dat2_new = dat2[:-nt_delay]
        else:
            dat2_new = dat2[nt_delay:]
            if nt_delay == 0:
                dat1_new = dat1
            else:
                dat1_new = dat1[:-nt_delay]
        return np.corrcoef(dat1_new, dat2_new)[0][1]

    def get_cc(self):
        self.ccc = np.append(self.ccc, self.cc())

    def plot(self, path='.\\'):
        time_now = datetime.now()
        fig = plt.figure(figsize=(20, 15))
        ax1 = fig.add_subplot(411)
        ax1.plot(self.time_axis_ch1, self.data_ch1)
        ax1.set_xlim(np.min(self.time_axis_ch1), np.max(self.time_axis_ch1))
        ax1.set_title("Channel 1")

        ax2 = fig.add_subplot(412)
        ax2.plot(self.time_axis_ch2, self.data_ch2)
        ax2.set_xlim(np.min(self.time_axis_ch2), np.max(self.time_axis_ch2))
        ax2.set_title("Channel 2")

        ax3 = fig.add_subplot(413)
        ax3.plot(self.time_axis_ch3, self.data_ch3)
        ax3.set_xlim(np.min(self.time_axis_ch3), np.max(self.time_axis_ch3))
        ax3.set_title("Channel 3")

        ax4 = fig.add_subplot(414)
        ax4.plot(self.time_axis_ch4, self.data_ch4)
        ax4.set_xlim(np.min(self.time_axis_ch3), np.max(self.time_axis_ch4))
        ax4.set_xlabel("Time (ms)")
        ax4.set_title("Channel 4")

        fig.savefig(join(path, 'wave_%s.png' % time_now.strftime('%Y%m%d%H%M%S')))


def monitor_delay(os, len, output):
    delay = np.array([])
    b_time = datetime.now()
    e_time = b_time + timedelta(seconds=len)
    while 1:
        delay = np.append(delay, os.delay(scale=5e-5))
        time.sleep(0.5)
        now_time = datetime.now()
        if now_time >= e_time:
            break
    output.put((delay, b_time, e_time))


def monitor_delay_all(os, len, output):
    delay13 = np.array([])
    delay24 = np.array([])
    b_time = datetime.now()
    e_time = b_time + timedelta(seconds=len)
    while 1:
        os.single()
        delay13 = np.append(delay13, os.delay(scale=5e-5))
        delay24 = np.append(delay24, os.delay24(scale=5e-5))
        os.run()
        time.sleep(0.5)
        now_time = datetime.now()
        if now_time >= e_time:
            break
    output.put((delay13, delay24, b_time, e_time))


if __name__ == '__main__':
    OS = OSMonitor('USB0::0x2A8D::0x1772::MYxxxxxxxx::INSTR')
    delay = OS.get_ch_data(scale=100e-6)
