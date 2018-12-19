import paramiko
import socket
import logging
import datetime

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
		except paramiko.ssh_exception.AuthenticationException:
			msg = 'SSH deamon active, but logon credential are wrong'
			self.last_msg = msg
			raise EnvironmentError(msg)
		except Exception as errorlog:
			# Added back the generic exception catcher since there might be
            # a bug in paramiko in the NoValidConnectionError class.
			msg = 'Unhandled fault - ' + str(errorlog)
		# We will only get here if we have not already raised an exception or
        # returned from the method.
		self.last_mag = msg
		logging.debug(msg)
		return False
	
	def send_command(self, c, timeout=None):
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
		ssh.connect(hostname=self.ip,
				   port=self.port,
				   username=self.user,
				   password=self.passwd)
		transport = ssh.get_transport()
		transport.set_keepalive(30)
		
		# send the command
		logging.debug("Sending command: {:}".format(c))
		stdin, stdout, stderr = ssh.exec_command(c)
		
		out = ""
		start_time = datetime.datetime.now()
		if timeout is None:
			delta = datetime.timedelta(days=datetime.timedelta.max.days)
		else:
			delta = timeout
