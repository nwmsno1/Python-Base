from automonitor import conn_visa


class SGControl(conn_visa.visainst):
    def __init__(self, inst_id):
        super(SGControl, self).__init__(inst_id)
        self.write("*CLS")

    @property
    def frequency(self):
        return float(self.query('FREQuency?'))

    @frequency.setter
    def frequency(self, value):
        self.write(":APPLy:SIN %f" % value)

    @property
    def output(self):
        return int(self.query("OUTPut:STATe?"))

    @output.setter
    def output(self, onoff):
        if onoff not in [0, 1]:
            raise ValueError("Output need to be 0(OFF) or 1(ON)")
        self.write("OUTPut:STATe %d" % onoff)


if __name__ == '__main__':
    sg = SGControl('GPIB0::xx::INSTR')
    sg.frequency = 10000000
    sg.output = 1
    print(sg.frequency, sg.output)
