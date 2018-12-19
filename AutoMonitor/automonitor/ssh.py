import paramiko
import socket
import logging
import datetime

logging.getlogger("paramiko").setLevel(logging.WARNING)

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
			
		# if we use delta.total_seconds(), the number is too big for the
        # timeout and cause script fail
        stdout.channel.settimeout(14400)
        # Read until success, or time out
		
		try:
			while True:
				partial = stdout.channel.recv(1024).decode("ISO-8859-1")
				if len(partial) == 0:
					logging.debug("SSH Command Exit Code: {:}".format(stdout.channel.recv_exit_status()))
					if stdout.channel.recv_exit_status() != 0:
						msg = "Exit status for the std channel was not 0 for "
						msg += "command {:}, print stdin: {:}".format(c, stdin)
						msg += ", stdout: {:}, stderr: {:}".fromat(stdout, stderr)
						logging.debug(msg)
					for line in stderr.readlines():
						self._log(line)
					break
				self._log(partial)
				out += partial
				current_time = datetime.datetime.now()
				elapsed = current_time - start_time
				if elapsed > delta:
					msg = "ERROR = {:} time out, allowed time was: {:}".format(c, timeout)
					raise TimeoutError(msg)
			# waiting to long for the command to finish
			except (TimeoutError, socket.timeout):
				msg = 'SSH recv socket timed out while waiting for server output'
				logging.debug(msg)
				raise TimeoutError(msg)
			
			ssh.close()
			
			return out
	
	@staticmethod
	def _log(text):
		# staticmethod don't need instantiate
		lines = [lines for line in text.split('\n')]
		
		for line in lines:
			if "xxx" in line and not (".xxxlog" in line or ".db" in line):
				logging.info(line)
			elif "INFO:" in line:
				msg = re.findall("INFO: (.+)", line)
				# If row is "INFO: " we will not print
                # Only print if INFO contain content
				if msg:
					logging.info(msg[0])
			else:
				logging.debug(line)
				
