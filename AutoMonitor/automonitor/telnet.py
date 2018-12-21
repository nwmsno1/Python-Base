# -*- coding: utf-8 -*-

import re
import telnetlib
import socket


# General Telnet class for communicating with tools
class Telnet(object):
    # Default port 4051 for Abisco Command Handler
    # Port used for MSSIM LSU is 8050
    def __init__(self, address, username, port=23, finish='$ '):
        self.address = address
        self.username = username + '\n'
        self.port = port
        self.finish = finish
        self.conn = None

    def connect(self):
        try:
            self.conn = telnetlib.Telnet(host=self.address,
                                         port=self.port,
                                         timeout=10)
        except socket.timeout:
            raise TimeoutError

        self.conn.read_until('username: '.encode())
        self.conn.write(self.username.encode())
        self.conn.read_until('password: '.encode())
        self.conn.write('\n'.encode())

    def close(self):
        # logging.debug('Closing telnet connection')
        self.conn.close()

    def command(self, cmd_unicode):

        # Open the telnet connection
        # logging.debug('Sending command to host: ' + cmd_unicode)
        self.connect()
        cmd_unicode += '\n'
        cmd = cmd_unicode.encode()

        self.conn.read_until(self.finish.encode())
        try:
            self.conn.write(cmd)
        except socket.error as e:
            raise EnvironmentError(e)

        resp = self.conn.read_until(self.finish.encode()).decode()
        self.close()

        return resp[:-len(self.finish)]

    def command_set(self, cmd_set):
        if not isinstance(cmd_set, list):
            raise ValueError('input value must be \'list\'')

        self.connect()
        resp = []

        self.conn.read_until(self.finish.encode())
        for cmd in cmd_set:

            cmd += '\n'
            try:
                self.conn.write(cmd.encode())
            except socket.error as e:
                raise EnvironmentError(e)
            resp.append(self.conn.read_until(self.finish.encode()).decode())

        self.close()
        return resp


if __name__ == '__main__':
    tn = Telnet('10.186.172.237', 'cpric_0')
    # tn.connect()
    set = ['config_sniffer 2 1 1', 'enable_emulator','set_cable_length_emulator -m 0 2', 'set_los_laser_emulator 1 1', 'set_los_laser_emulator 0 1']
    print(tn.command_set(set))
