#
# [name] ion.net.py
# [test] python -m ion.net
#
# Written by Yoshikazu NAKAJIMA
#

import sys
import json
import pprint  # リストや辞書を整形して出力
import datetime
import copy
from typing import Union
import socket
import pickle
import time

# nkjlib

from nkj.str import *
import nkj.time as nt

# ionlib

from .core import *

# classes

#-- network agents

__BROADCAST = ''

_DEFAULT_SERVERPORT = 8060
_DEFAULT_BUFFERSIZE = 4096
_DEFAULT_BACKLOG = 1
_DEFAULT_TIMEOUT = 5.0 # sec
_DEFAULT_SLEEPTIME = 0  # sec
_DEFAULT_CODING = 'json'  # {'utf-8', 'shift_jis', 'json', 'pickle', 'binary'}

"""
[encoding methods]
'文字列'.encode()/b'バイト列'decode():  文字列 <-> バイト列の変換．
json.dumps()/json.loads():              辞書形式 <-> 文字列の直列化．これと encode()/decode() の組合せが安全．
pickle.dumps()/pickle.loads(): データのシリアライズ(Serialize)．安全でない．非シリアライズの過程で任意のコードを実行するような悪意のある pickle オブジェクトを生成可能．
json に比べ、pickle はバイナリを処理できるが、(1) python 特有、かつ (2) 安全でない
"""

__PACKET_PREPOSITION = 'iON.PACKET: '

__DEFAULT_PACKET_ENCRYPTION_FLAG = True

__COMMAND_SHUTDOWN = 'ion.shutdown'
__RESPONSE_SHUTDOWN = 'ion.bye'
__COMMAND_RESPONSEREQUEST = 'ion.response_request'
__RESPONSE_RESPONSEREQUEST = 'ion.alive'
__COMMAND_DATAREQUEST = 'ion.data_request'
__RESPONSE_SUCCEEDED = 'ion.succeeded'
__RESPONSE_ERROR = 'ion.error'
__RESPONSE_FAILED = __RESPONSE_ERROR
__RESPONSE_OK = 'ion.ok'
__RESPONSE_CANCEL = 'ion.cancel'
__RESPONSE_YES = __RESPONSE_OK
__RESPONSE_NO = __RESPONSE_CANCEL

__SERVERPORT = _DEFAULT_SERVERPORT
__BUFFERSIZE = _DEFAULT_BUFFERSIZE
__BACKLOG = _DEFAULT_BACKLOG
__TIMEOUT = _DEFAULT_TIMEOUT
__SLEEPTIME = _DEFAULT_SLEEPTIME
__CODING = _DEFAULT_CODING

# global access

_PACKET_PREPOSITION = __PACKET_PREPOSITION
_PACKET_ENCRYPTION_FLAG = __DEFAULT_PACKET_ENCRYPTION_FLAG

_COMMAND_SHUTDOWN = __COMMAND_SHUTDOWN
_RESPONSE_SHUTDOWN = __RESPONSE_SHUTDOWN
_COMMAND_RESPONSEREQUEST = __COMMAND_RESPONSEREQUEST
_RESPONSE_RESPONSEREQUEST = __RESPONSE_RESPONSEREQUEST
_COMMAND_DATAREQUEST = __COMMAND_DATAREQUEST
_RESPONSE_ERROR = __RESPONSE_ERROR
_RESPONSE_SUCCEEDED = __RESPONSE_SUCCEEDED
_RESPONSE_FAILED = __RESPONSE_FAILED
_RESPONSE_OK = __RESPONSE_OK
_RESPONSE_CANCEL = __RESPONSE_CANCEL
_RESPONSE_YES = __RESPONSE_YES
_RESPONSE_NO = __RESPONSE_NO

COMMAND_SHUTDOWN = __COMMAND_SHUTDOWN
RESPONSE_SHUTDOWN = __RESPONSE_SHUTDOWN
COMMAND_RESPONSEREQUEST = __COMMAND_RESPONSEREQUEST
RESPONSE_RESPONSEREQUEST = __RESPONSE_RESPONSEREQUEST
COMMAND_DATAREQUEST = __COMMAND_DATAREQUEST
RESPONSE_SUCCEEDED = __RESPONSE_SUCCEEDED
RESPONSE_ERROR = __RESPONSE_ERROR
RESPONSE_FAILED = __RESPONSE_FAILED
RESPONSE_OK = __RESPONSE_OK
RESPONSE_CANCEL = __RESPONSE_CANCEL
RESPONSE_YES = __RESPONSE_YES
RESPONSE_NO = __RESPONSE_NO

_ID_ERROR = -1

ID_ERROR = _ID_ERROR

def encryption_flag(flag=None):
	global _PACKET_ENCRYPTION_FLAG
	if (flag is None):
		return _PACKET_ENCRYPTION_FLAG
	else:
		_PACKET_ENCRYPTION_FLAG = flag
		return True

def broadcast():
	global __BROADCAST
	return __BROADCAST

def serverport(port=None):
	global __SERVERPORT
	if (port is None):
		return __SERVERPORT
	else:
		__SERVERPORT = port
		return True

def server_port(port=None):
	return serverport(port)

def buffersize(size=None):
	global __BUFFERSIZE
	if (size is None):
		return __BUFFERSIZE
	else:
		__BUFFERSIZE = size
		return True

def buffer_size(size=None):
	return buffersize(size)

def backlog(num=None):
	global __BACKLOG
	if (num is None):
		return __BACKLOG
	else:
		__BACKLOG = num
		return True

def listen_num(num=None):
	return backlog(num)

def timeout(time=None):
	global __TIMEOUT
	if (time is None):
		return __TIMEOUT
	else:
		__TIMEOUT = time
		return True

def timeout_(time=None):
	return timeout(time)

def sleeptime(time=None):
	global __SLEEPTIME
	if (time is None):
		return __SLEEPTIME
	else:
		__SLEEPTIME = time
		return True

def sleep_time(time=None):
	return sleeptime(time)

def coding(code=None):
	global __CODING
	if (code is None):
		return __CODING
	else:
		__CODING = code
		return True

def coding_(code=None):
	return coding(code)

# encoding/decoding functions

def _add_preposition(message):
	global _PACKET_PREPOSITION
	return _PACKET_PREPOSITION + message

def _remove_preposition(message):
	global _PACKET_PREPOSITION
	lenpp = len(_PACKET_PREPOSITION)
	prestr = message[0:lenpp]
	if (prestr == _PACKET_PREPOSITION):
		message = message[lenpp:]
	else:
		raise ValueError("ERROR: Non-iON packet.")  # iON packet でない場合は、例外を発生
	return message

def _encrypt(message):
	if (encryption_flag()):
		ldprint2('encrypt...')
		return message
	else:
		return message  # Noting done

def _decrypt(message):
	if (encryption_flag()):
		ldprint2('decrypt...')
		return message
	else:
		return message  # Noting done

def _package(message):
	return _add_preposition(_encrypt(message))

def _unpackage(message):
	return _decrypt(_remove_preposition(message))

def _encode(message, coding=None):
	ldprint('--> _encode(\'{0}\', {1})'.format(message, coding))
	coding = coding_() if (coding is None) else coding
	ldprint2('message: \'{}\''.format(message))
	ldprint2('coding:  \'{}\''.format(coding))
	if (coding == 'utf-8' or coding == 'shift_jis'):
		encoded_message = _package(message).encode(coding)
	elif (coding == 'json'):
		encoded_message = _package(json.dumps(message)).encode('utf-8')
	elif (coding == 'pickle' or coding == 'binary'):
		encoded_message = _package(pickle.dumps(message))
	else:
		__ERROR__
	ldprint('<-- _encode(): {}'.format(encoded_message))
	return encoded_message

def _decode(packet_message, coding=None):
	ldprint('--> _decode({0}, {1})'.format(packet_message, coding))
	coding = coding_() if (coding is None) else coding
	ldprint2('packet: \'{}\''.format(packet_message))
	ldprint2('coding: \'{}\''.format(coding))
	"""
	if (packet_message == b''):
		ldprint('<-- _decode(): \'{}\''.format(''))
		return ''
	"""
	if (coding == 'utf-8' or coding == 'shift_jis'):
		message = _unpackage(packet_message.decode())
	elif (coding == 'json'):
		message = json.loads(_unpackage(packet_message.decode()))
	elif (coding == 'pickle' or coding == 'binary'):
		message = pickle.loads(_unpackage(packet_message))
	else:
		__ERROR__
	ldprint('<-- _decode(): \'{}\''.format(message))
	return message

def _binary_encode(message):
	return _encode(message, 'binary')

def _binary_deode(packet_message):
	return _deode(packet_message, 'binary')

def encode(message, coding=None):
	return _encode(message, coding)

def decode(packet_message, coding=None):
	return _decode(packet_message, coding)

def binary_encode(message):
	return _binary_encode(message)

def binary_decode(packet_message):
	return _binary_decode(packet_message)

def server_response(cli_sock, response):
	cli_sock.sendall(_encode(response))

def svr_response(cli_sock, response):
	server_response(cli_sock, response)

class server_cls():
	_classname = 'ion.server_cls'

	def __init__(self):
		self._svr_sock = None
		self._hostname = socket.gethostname()
		self._address = socket.gethostbyname(self._hostname)
		self._datafound = False
		ldprint('Server Hostname:   \'{}\''.format(self.hostname))
		ldprint('Server IP Address: {}'.format(self.address))

	def __del__(self):
		self.close()

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	@property
	def hostname(self):
		return self._hostname

	@hostname.setter
	def hostname(self, n):
		self._hostname = n

	@property
	def address(self):
		return self._address

	@address.setter
	def address(self, a):
		self._address = a

	@property
	def svr_address(self):
		return self.address

	@svr_address.setter
	def svr_address(self, a):
		self.address = a

	@property
	def port(self):
		return serverport()

	@port.setter
	def port(self, p):
		serverport(p)

	@property
	def svr_port(self):
		return self.port

	@svr_port.setter
	def svr_port(self, p):
		self.port = p

	@property
	def buffersize(self):
		return buffer_size()

	@buffersize.setter
	def buffersize(self, size):
		buffer_size(size)

	@property
	def server_socket(self):
		return self._svr_sock

	@server_socket.setter
	def server_socket(self, s):
		self._svr_sock = s

	@property
	def svr_socket(self):
		return self.server_socket

	@svr_socket.setter
	def svr_socket(self, s):
		self.server_socket = s

	@property
	def backlog(self):
		return backlog()

	@backlog.setter
	def backlog(self, n):
		backlog(n)

	@property
	def timeout(self):
		return timeout_()

	@timeout.setter
	def timeout(self, t):
		timeout_(t)

	@property
	def sleeptime(self):
		return sleep_time()

	@sleeptime.setter
	def sleeptime(self, t):
		sleep_time(t)

	@property
	def coding(self):
		return coding_()

	@coding.setter
	def coding(self, c):
		coding_(c)

	@property
	def datafound(self):
		return self._datafound

	@datafound.setter
	def datafound(self, flag):
		self._datafound = flag

	def open(self):
		if (self.hostname is None):
			return False
		if (self.address is None):
			return False

		self.svr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		try:
			ldprint('[SVR] Timeout: {} (sec)'.format(self.timeout))
			self.svr_socket.settimeout(self.timeout)
			self.svr_socket.bind((self.svr_address, self.svr_port))
			ldprint('[SVR] Binding succeeded')

		except OSError:
			print_error('iON ERROR: OS error')
			pass

		else:
			# Binding succeeded

			self.svr_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
			self.svr_socket.listen(self.backlog)
			ldprint('[SVR] Listen started')

			while True:
				try:
					cli_sock, cli_connection = self.svr_socket.accept()
					ldprint('[SVR] Accept client')
					cli_address, cli_port = cli_connection
					ldprint('[SVR] Client address (port): {0} ({1})'.format(cli_address, cli_port))

				except KeyboardInterrupt:
					ldprint('Keyboard interrupted.')
					break

				except socket.error:
					#print_error('Network connection failed.')
					if (self.sleeptime != 0):
						time.sleep(self.sleeptime)
					pass

				else:
					# Connection scceeded

					ldprint('[SVR] Connection succeeded.')

					def __ion_command(cli_message):
						ldprint('--> server.__ion_command(\'{}\')'.format(cli_message))

						if (cli_message == _COMMAND_RESPONSEREQUEST):
							ldprint('[SVR] command: response request')
							svr_message = _RESPONSE_RESPONSEREQUEST
							ldprint('[SVR] SVRMESSAGE: {}'.format(svr_message))
							cli_sock.sendall(_encode(svr_message))

						else:
							ldprint('[SVR] command: unknown')
							ldprint('<-- server.__ion_command(): {}'.format(False))
							return False

						ldprint('<-- server.__ion_command(): {}'.format(True))
						return True

					def __recv(cli_sock):
						ldprint('[SVR] Buffersize: {}'.format(self.buffersize))
						return cli_sock.recv(self.buffersize)
						"""
						# recv() の成功／失敗の判定は以下でやる
						if not cli_data:
							break
						"""

					# connection processing

					ldprint('[SVR] Start connection process...')
					cli_data = __recv(cli_sock)
					ldprint('[SVR] Data from client: {}'.format(cli_data))

					try:
						cli_message = None if (cli_data == '') else _decode(cli_data)

					except ValueError as e:  # Including non-iON-packet error
						print_error(e)
						cli_sock.close()
						continue  # client socket の accept()  を閉じ、listen を続ける

					#----- client message processing -----

					ldprint0('[SVR] Received message: \'{0}\', Client address: {1}, Client port: {2}'.format(cli_message, cli_address, cli_port))

					if (cli_message == _COMMAND_SHUTDOWN):
						ldprint('[SVR] command: shutdown')
						svr_message = _RESPONSE_SHUTDOWN
						ldprint('[SVR] SVRMESSAGE: {}'.format(svr_message))
						cli_sock.sendall(_encode(svr_message))
						print_message('iON SERVER: Shutdown...')
						cli_sock.close()
						break

					if (__ion_command(cli_message)):
						ldprint('[SVR] ion command')
						pass

					elif (self._data_provision(cli_sock, cli_message)):
						ldprint('[SVR] ion data provision')
						self.datafound = False  # データ供給を終えたので，フラグを False にする．

					elif (self.query_processing(cli_sock, cli_message)):
						ldprint('[SVR] ion query processing')
						self.datafound = True  # クエリチェックで整合したので、フラグを True にしてデータ供給に備える．

					else:
						self.error_processing(cli_sock)
						ldprint('[SVR] ion error')

					cli_sock.close()

			self.close()

		return True

	def launch(self):
		self.open()

	def close(self):
		if (self.svr_socket is None):
			return False
		self.svr_socket.close()
		self.svr_socket = None
		return True

	def is_closed(self):
		return (self.svr_socket is None)

	def closed(self):
		return self.is_closed()

	def is_opened(self):
		return (not self.is_closed())

	def opened(self):
		return self.is_opened()

	# iON data sending

	def data_sending(self, cli_sock):  # Function for Override
		ldprint('--> ion.server.data_sending()'.format())
		svr_response = 'test_data'
		cli_sock.sendall(_encode(svr_response))
		ldprint('<-- ion.server.data_sending()')

	def _data_provision(self, cli_sock, cli_query):
		ldprint('--> ion.server._data_provision(,, \'{}\')'.format(cli_query))
		if (cli_query == COMMAND_DATAREQUEST):
			if (self.datafound):
				self.data_sending(cli_sock)
			else:
				svr_message = _RESPONSE_ERROR
				cli_sock.sendall(_encode(svr_message))
				raise ValueError("ERROR: Illegal iON protocol.")  # iON 通信プロトコル違反
		else:
			ldprint('<-- ion.server._data_provision(): {}'.format(False))
			return False
		ldprint('<-- ion.server._data_provision(): {}'.format(True))
		return True

	# iON query processing

	def query_processing(self, cli_sock, cli_query):  # Function for Override
		if (cli_query == 'query #1' or cli_query == 'query #2' or cli_query == 'query #3'):
			svr_response = _RESPONSE_SUCCEEDED
			cli_sock.sendall(_encode(svr_response))
			return True
		else:
			return False

	def queryprocessing(self, cli_sock, cli_query):
		return query_processing(cli_sock, cli_query)

	# iON error processing

	def error_processing(self, cli_sock):
		print_error('Unknown iON command or query.')
		svr_message = _RESPONSE_ERROR
		cli_sock.sendall(_encode(svr_message))

	def errorprocessing(self, cli_sock):
		error_processing(cli_sock)

class server(server_cls):  # alias
	pass

class client_cls():
	_classname = 'ion.client_cls'

	def __init__(self):
		self._cli_sock = None

	def __del__(self):
		self.close()

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	@property
	def client_socket(self):
		return self._cli_sock

	@client_socket.setter
	def client_socket(self, s):
		self._cli_sock = s

	@property
	def cli_socket(self):
		return self.client_socket

	@cli_socket.setter
	def cli_socket(self, s):
		self.client_socket = s

	@property
	def socket(self):
		return self.client_socket

	@socket.setter
	def socket(self, s):
		self.client_socket = s

	@property
	def server_port(self):
		return serverport()

	@server_port.setter
	def server_port(self, p):
		serverport(p)

	@property
	def serverport(self):
		return self.server_port

	@serverport.setter
	def serverport(self, p):
		self.server_port = p

	@property
	def svr_port(self):
		return self.server_port

	@svr_port.setter
	def svr_port(self, p):
		self.server_port = p

	@property
	def buffersize(self):
		return buffer_size()

	@buffersize.setter
	def buffersize(self, size):
		buffer_size(size)

	def connect(self):
		ldprint('--> ion.client.connect()')

		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		try:
			ldprint2('[CLI] Client socket: {}'.format(self.client_socket))
			ldprint2('[CLI] Try connection')
			address = broadcast()
			port = serverport()
			ldprint2('[CLI] Address: \'{0}\', Port: {1}'.format(address, port))
			self.client_socket.connect((address, port))

		except ConnectionRefusedError:
			ldprint2('[CLI] ERROR: Connection failed.')
			ldprint('<-- connect(): {}'.format(False))
			self.client_socket = None
			return False

		else:
			# Connection succeeded.
			pass

		ldprint2('[CLI] Connection succeeded.')
		ldprint('<-- ion.client.connect(): {}'.format(True))
		return True

	def open(self):
		return self.connect()

	def launch(self):
		return self.open()

	def close(self):
		if (self.client_socket is None):
			return False
		self.client_socket.close()
		self.client_socket = None
		return True

	def is_closed(self):
		return (self.client_socket is None)

	def closed(self):
		return self.is_closed()

	def is_opened(self):
		return (not self.is_closed())

	def opened(self):
		return self.is_opened()

	def __recv(self, cli_sock):
		return cli_sock.recv(self.buffersize)            # サーバからメッセージを受け取る．
		"""
		# recv() の成功／失敗の判定は以下でやる
		if not cli_data:
			break
		"""

	def recv(self):
		ldprint('--> client.recv()')
		connectionflag = False
		if (not self.opened()):
			ldprint2('[CLI] Not opened. Trying to open socket.')
			if (self.connect()):
				ldprint2('[CLI] Connection succeeded.')
				connectionflag = True
			else:
				ldprint2('<Server connection failed>')
				ldprint('<-- client.send(): \'{}\''.format(None))
				return None

		if (self.cli_socket is None):
			__ERROR__

		svr_packet = self.__recv(self.client_socket)
		ldprint2('[CLI] Packet from server: {}'.format(svr_packet))

		try:
			svr_message = _decode(svr_packet)
		except ValueError as e:
			print_error(e)
			svr_message = e
		ldprint2('[CLI] Received:   \'{}\''.format(svr_message))

		if (connectionflag):
			self.close()
		ldprint('<-- client.recv(): \'{}\''.format(svr_message))
		return svr_message

	def send(self, cli_message):
		ldprint('--> client.send(\'{}\')'.format(cli_message))
		connectionflag = False
		if (not self.opened()):
			ldprint2('[CLI] Not opened. Trying to open socket.')
			if (self.connect()):
				ldprint2('[CLI] Connection succeeded.')
				connectionflag = True
			else:
				ldprint2('<Server connection failed>')
				ldprint('<-- client.send(): \'{}\''.format(None))
				return None

		ldprint2('[CLI] Connection operation: {}'.format(connectionflag))
		ldprint2('[CLI] Client socket: {}'.format(self.client_socket))
		ldprint2('[CLI] Send:       \'{}\''.format(cli_message))

		packet_message = _encode(cli_message)
		ldprint2('[CLI] Packet message: {}'.format(packet_message))

		if (self.cli_socket is None):
			__ERROR__

		self.client_socket.sendall(packet_message)                       # サーバへメッセージを送る．
		ldprint2('[CLI] Packet sent.')

		svr_message = self.recv()
		ldprint2('[CLI] Received:   \'{}\''.format(svr_message))

		if (connectionflag):
			self.close()
		ldprint('<-- client.send(): \'{}\''.format(svr_message))
		return svr_message

	def command(self, command):
		return self.send(command)

	def receive(self):
		return self.recv()

	def response(self):  # Receive response from the server
		return self.receive()

	def query(self, query):
		return self.send(query)

class client(client_cls):  # alias
	pass

# Network agents

class server_agent(server_cls):  # Add query operations to server_cls()
	_classname = 'ion.server_agent'

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def __init__(self, sl=None):
		super().__init__()
		self.setSemanticsList(sl)

	def getSemanticsList(self):
		return self._semlist

	def setSemanticsList(self, sl):
		if (sl is None):
			self._semlist = [ion_agent()]
		elif (isinstance(sl, ion.ion_agent)):
			self._semlist = [sl]
		elif (isinstance(sl, dict)):
			self._semlist = [ion_agent(dict)]
		elif (isinstance(sl, list) or isinstance(sl, tuple)):
			self._semlist = list(sl)
		else:
			__ERROR__  # Illegal type of semantics list

		self._updateQueryList()  # Synchronize the semantics list to the query list

	@property
	def semanticslist(self):
		return self.getSemanticsList()

	@semanticslist.setter
	def semanticslist(self, sl):
		self.setSemanticsList(sl)

	def getSemList(self):
		return self.getSemanticsList()

	def setSemList(self, sl):
		self.setSemanticsList(sl)

	@property
	def semlist(self):
		return self.getSemList()

	@semlist.setter
	def semlist(self, sl):
		self.setSemList(sl)

	def getSemantics(self, id=0):
		if (id >= 0 and id < len(self.semanticslist)):
			return self.semanticslist[id]
		else:
			return None  # ERROR

	def setSemantics(self, s, id=None):
		sllen = len(self.semanticslist)
		if (id is None):
			self.semanticslist.append(s)
		elif (id < 0):
			return False
		elif (id == sllen):
			self.semanticslist.append(s)
		elif (id > sllen):
			for i in range(sllen, id):
				self.semanticslist.append(ion_agent())
			self.semanticslist.append(s)
		else:
			self.semanticslist[id] = s
		self._updateQueryList()
		return True

	def semantics(self, id=0, s=None):
		if (s is None):
			if (id < 0 or id > len(self.semanticslist) - 1):
				return None
			else:
				return self.getSemantics(id)
		else:
			return self.setSemantics(id, s)

	def sem(self, id=0, s=None):
		return semantics(id, s)

	def s(self, id=0, s=None):
		return semantics(id, s)

	def _updateQueryList(self):
		if (self.semantics is None):
			self._querylist = None
		else:
			self._querylist = [sem.query for sem in self.semanticslist]

	def getQueryList(self):
		return self._querylist

	@property
	def querylist(self):
		return self.getQueryList()

	def getQuery(self, id=0):
		if (id >= 0 and id < len(self.querylist)):
			return self.querylist[id]
		else:
			return None  # ERROR

	def query(self, id=0):
		return self.getQuery(id)

	def q(self, id=0):
		return self.query(id)

	def query_check(self, cli_query):
		ldprint('--> ion.server_agent()')
		ldprint('Query: \'{0}\' ({1})'.format(cli_query, type(cli_query)))
		if (type(cli_query) == 'dict'):
			ldprint('Dict type')
			cli_query = query(dict)
			ldprint('Query: \'{0}\' ({1})'.format(cli_query, type(cli_query)))
		else:
			__ERROR__
		if (not isinstance(cli_query, ion.query)):
			ldprint0('ERROR: Non-query inputed.')
			ldprint('<-- ion.server_agent()')
			return ID_ERROR
		for id in range(len(self.querylist)):
			if (self.query(id) <= cli_query):
				return id
		ldprint('<-- ion.server_agent()')
		return ID_ERROR

	def query_processing(self, cli_sock, cli_query):
		ldprint0('Client query: \'{0}\', {1}'.format(cli_query, type(cli_query)))
		qid = self.query_check(cli_query)
		ldprint0('Matched query ID: {}'.format(qid))
		if (qid == ID_ERROR):
			svr_message = RESPONSE_ERROR
			cli_sock.sendall(_encode(svr_message))
			return False
		else:
			svr_message = RESPONSE_SUCCEEDED
			cli_sock.sendall(_encode(svr_message))
			return True

class serveragent(server_agent):  # alias
	pass

class client_agent(client):
	_classname = 'ion.client_agent'

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

class clientagent(client_agent):  # alias
	pass

#-- main

if __name__ == '__main__':
	import argparse
	import ion

	_DEBUGLEVEL = 1
	_LIB_DEBUGLEVEL = 0

	debuglevel(_DEBUGLEVEL)
	lib_debuglevel(_LIB_DEBUGLEVEL)

	parser = argparse.ArgumentParser()

	parser.add_argument('--mode', '-mode', choices=['server', 'client'], default='client')
	args = parser.parse_args()
	mode = args.mode

	if (mode == 'server'):
		svr = ion.server_agent()
		svr.launch()

	elif (mode == 'client'):
		for command in [ion.COMMAND_RESPONSEREQUEST, ion.COMMAND_SHUTDOWN]:
			dprint('[MAIN] command: \'{}\''.format(command))
			message = ion.client_agent().send(command)
			if (message is None):
				print_error('[MAIN] command sending error.')
				break
			else:
				dprint('[MAIN] server response: \'{}\''.format(message))
	else:
		__ERROR__
