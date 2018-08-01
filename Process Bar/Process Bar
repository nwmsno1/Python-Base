import sys
import time


class ShowProcess(object):
    def __init__(self, max_steps, max_arrows=100, i=0):
        self.max_steps = max_steps
        self.max_arrows = max_arrows
        self.i = i

    def show_process(self, i=None):
        if i is not None:
            self.i = i
        else:
            self.i += 1
        num_arrow = int(self.i * self.max_arrows / self.max_steps)
        num_line = self.max_arrows - num_arrow
        percent = self.i * 100 / self.max_steps
        process_bar = '\r' + '[' + '>' * num_arrow + '-' * num_line + ']' + '%.2f' % percent + '%'
        sys.stdout.write(process_bar)
        sys.stdout.flush() # refresh the stdout
        # self.i += 1

    def close(self, word='done'):
        print('')
        print(word)
        self.i = i


if __name__ == '__main__':
    max_steps = 100
    process_bar = ShowProcess(max_steps)
    for i in range(max_steps + 1):
        process_bar.show_process()
        time.sleep(0.05)
    process_bar.close()
