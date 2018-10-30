import visa
import numpy as np

def list_inst():
    rm = visa.ResourceManager()
    print(rm.list_resources())


class visainst(object):

    def __init__(self, inst_id):
        self.inst_id = inst_id
        self._rm = visa.ResourceManager()
        self.this_inst = self._rm.open_resource(self.inst_id)

    @property
    def inst_name(self):
        return self.this_inst.query('*IDN?')

    def close(self):
        self.this_inst.close()

    def query(self, cmd):
        return self.this_inst.query(cmd).strip()

    def write(self, cmd):
        self.this_inst.write(cmd)

    def read(self, cmd):
        return self.this_inst.query_ascii_values(cmd, container=np.array)

if __name__ == '__main__':
    list_inst()
    ins = visainst('USB0::0x2A8D::0x1772::MY57190679::INSTR')
    print(ins.inst_name)
    ins.write(':WAVeform:POINts:MODE ASCii')
    ins.write(':WAVeform:FORMat ASCii')
    ins.write(':MEASure:SOURce CHANnel1')
    #ins.write('FORMat:TRACe:DATA REAL,32')
    #ins.write('FORMat:BORDer SWAPped')
    try:
        print(ins.query(':WAVeform:DATA?'))
        print(ins.query(":WAVeform:XINCrement?"))
    finally:
        ins.close()
