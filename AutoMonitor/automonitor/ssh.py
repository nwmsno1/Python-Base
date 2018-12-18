import paramiko
import socket

class SSH(object):

	def __init__(self, user, passwd, ip, port=22):
		self.user = user
		self.passwd = passwd
		self.ip = ip
		self.port = port
		self.last_msg = ''
	
	def is_alive(self, timeout=None):
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
			ssh.connect(hostname=self.ip,
					   port=self.port,
					   username=self.user,
					   password=self.passwd,
					   timeout=timeout,
					   banner_timeout=timeout)
			ssh.close()
			return True
		except ConnectionRefusedError:
			msg = 'No SSH daemon active at ' + self.ip
		except (TimeoutError, socket.timeout):
			mag = 'No connection could be established ' + self.ip
			
