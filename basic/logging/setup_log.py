import logging
import re
from os.path import basename


class setuplog(object):
    def __init__(self, filename):
        self.filename = filename
        fh = logging.FileHandler(filename)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.FClog = logging.getLogger('FCMonitor')
        self.OSlog = logging.getLogger('OSMonitor')
        self.SAlog = logging.getLogger('SAMonitor')
        self.SGlog = logging.getLogger('SGControl')
        self.Runtime = logging.getLogger('Runtime')
        self.FClog.addHandler(fh)
        self.FClog.addHandler(ch)
        self.FClog.setLevel(logging.INFO)
        self.OSlog.addHandler(fh)
        self.OSlog.addHandler(ch)
        self.OSlog.setLevel(logging.INFO)
        self.SAlog.addHandler(fh)
        self.SAlog.addHandler(ch)
        self.SAlog.setLevel(logging.INFO)
        self.SGlog.addHandler(fh)
        self.SGlog.addHandler(ch)
        self.SGlog.setLevel(logging.INFO)
        self.Runtime.addHandler(fh)
        self.Runtime.addHandler(ch)
        self.Runtime.setLevel(logging.INFO)

    def truncate(self):
        with open(self.filename, 'w') as f:
            f.truncate()

    def CaseFail(self, reason):
        self.Runtime.error('result = case_fail;')
        self.Runtime.error('description:'+reason+';')

    def CasePass(self):
        self.Runtime.info('result = case_passed;')

    def check_error(self):
        with open(self.filename) as f:
            content = f.read()
        if re.search(r'ERROR:', content):
            self.CaseFail('See %s' % basename(self.filename))
        else:
            self.CasePass()


if __name__ == '__main__':
    log = setuplog('test.log')
    log.FClog.exception('test')
