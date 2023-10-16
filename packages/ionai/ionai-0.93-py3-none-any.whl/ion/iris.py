#
# [name]    ion.iris.py
# [comment] library to connect to InterSystems IRIS database
#
# Written by Yoshikazu NAKAJIMA
#

import irisnative
from ion import *

_TMDUBMI_IRIS_IP = '192.168.0.47'
_TMDUBMI_IRIS_PORT = 1972
_TMDUBMI_NAMESPACE = 'FS'
_TMDUBMI_USERNAME = '_SYSTEM'
_TMDUBMI_PASSWORD = 'bmi-2718'

_DEFAULT_IRIS_IP = _TMDUBMI_IRIS_IP
_DEFAULT_IRIS_PORT = _TMDUBMI_IRIS_PORT
_DEFAULT_IRIS_NAMESPACE = _TMDUBMI_NAMESPACE
_DEFAULT_IRIS_USERNAME = _TMDUBMI_USERNAME
_DEFAULT_IRIS_PASSWORD = _TMDUBMI_PASSWORD

class iris(agent.database_agent):
	_classname = 'ion.iris'

	def __init__(self):
		self._iris_connection = None
		self._iris_ip = _DEFAULT_IRIS_IP
		self._iris_port = _DEFAULT_IRIS_PORT
		self._iris_namespace = _DEFAULT_IRIS_NAMESPACE
		self._iris_username = _DEFAULT_IRIS_USERNAME
		self._iris_password = _DEFAULT_IRIS_PASSWORD

	def __del__(self):
		self.iris_close()

	@classmethod
	@property
	def classname(cls):
		return cls._classname

	@property
	def iris_connection(self):
		return self._iris_connection

	@property
	def iris_ip(self):
		return self._iris_ip

	@ip.setter
	def iris_ip(self, ip_):
		self._iris_ip = ip_

	@property
	def iris_port(self):
		return self._iris_port

	@iris_port.setter
	def iris_port(self, p):
		self._iris_port = p

	@property
	def namespace(self):
		return self._iris_namespace

	@namespace.setter
	def namespace(self, ns):
		self._iris_namespace = ns

	@property
	def ns(self):
		return self.iris_namespace

	@ns.setter
	def ns(self, ns_):
		self.iris_namespace = ns_

	@property
	def username(self):
		return self._iris_username

	@username.setter
	def username(self, name):
		self._iris_username = name

	@property
	def userid(self):
		return self.username

	@userid.setter
	def userid(self, name):
		self.username = name

	@property
	def user(self):
		return self.username

	@user.setter
	def user(self, name):
		self.username = name

	@property
	def password(self):
		return self._iris_password

	@password.setter
	def password(self, pw):
		self._iris_password = pw

	@property
	def pw(self):
		return self.password

	@pw.setter
	def pw(self, pw_):
		self.password = pw_

	def iris_open(self):
		self.iris_connection = irisnative.createConnection(self.iris_ip, self.iris_port, self.namespace, self.username, self.password)
		iris_native = irisnative.createIris(self.iris_connection)

	def iris_close(self):
		if (self.iris_connected()):
			self._connection.close()
			self._connection = None

	def iris_connected(self):
		return (self._connection is not None)

	def iris_not_connected(self):
		return (self._connection is None)

	def update_data(self, query):
		pass

#-- main

if __name__ == '__main__':

	from nkj.str import *

	_DEBUGLEVEL = 1
	_LIB_DEBUGLEVEL = 1
	debuglevel(_DEBUGLEVEL)
	lib_debuglevel(_LIB_DEBUGLEVEL)

	iris = iris()
