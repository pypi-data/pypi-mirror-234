#
# [name] ion.agent.py
# [exec] python -m ion.agent
#
# Written by Yoshikazu NAKAJIM
#

from .const import *
from .core import *
from .net import *

class data_agent(server_agent):
	_classname = 'ion.data_agent'

	@classmethod
	def getClassName(cls):
		return ion._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def __init__(self):
		super().__init__()
		self._output_queryid = ID_ERROR

	def getOutputQueryID(self):
		return self._output_queryid

	def setOutputQueryID(self, id):
		self._output_queryid = id

	@property
	def output_queryid(self):
		return self.getOutputQueryID()

	@output_queryid.setter
	def output_queryid(self, id):
		self.setOutputQueryID(id)

	@property
	def output_qid(self):
		return self.output_queryid

	@output_qid.setter
	def output_qid(self, id):
		self.output_queryid = id

	@property
	def queryid(self):
		return self.output_queryid

	@queryid.setter
	def queryid(self, id):
		self.output_queryid = id

	def semantics(self, id=None):
		if (id is None):
			if (self.output_queryid == ID_ERROR):
				return super().semantics(0)
			else:
				return super().semantics(self.output_queryid)
		else:
			return super().semantics(id)

	def query_processing(self, cli_sock, cli_query):
		ldprint0('--> ion.data_agent.query_processing()')
		ldprint0('Client query: \'{0}\', {1}'.format(cli_query, type(cli_query)))

		self.output_queryid = self.query_check(cli_query)  # ここで，どの出力クエリと整合したかを確認
		ldprint0('Matched query ID: {}'.format(self.output_queryid))

		if (self.output_queryid == ID_ERROR):
			svr_message = RESPONSE_ERROR
			cli_sock.sendall(_encode(svr_message))
			ldprint0('<-- ion.data_agent.query_processing(): {}'.format(False))
			return False

		self.update_data(cli_query)

		data = self.semantics(self.output_queryid).databody

		if (data is not None):
			svr_message = RESPONSE_SUCCEEDED
			cli_sock.sendall(_encode(svr_message))

			if (isinstance(data, bytes)):
				ldprint0('Bytes data')
				cli_sock.sendall(_encode(data, 'json'))
			else:
				ldprint0('Non-bytes data')
				cli_sock.sendall(_encode(data))

		else:
			svr_message = RESPONSE_ERROR
			cli_sock.sendall(_encode(svr_message))

		ldprint0('<-- ion.data_agent.query_processing(): {}'.format(True))
		return True

	def update_data(self, cli_query):
		pass  # Nothing to do for genenral data agent

class data_provider(data_agent):
	pass

class database_agent(server_agent):  # query check（=事前登録したquery listとの整合確認）を行わないので、data_agent でなく server_agent を継承
	_classname = 'ion.database_agent'

	def __init__(self):
		super().__init__()

	@classmethod
	def getClassName(cls):
		return ion._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def query_check(cli_query):
		__ERROR__ # disabled

"""
	def query_processing(self, cli_sock, cli_query):
		#
		# (1) cli_query をデータベースで検索
		# (2) response を返す
		# (2-1) Found -> RESPONSE_SUCCEEDED を返す
		# (2-2) Failed -> RESPONSE_ERROR を返す
		#
		return False

	def data_sending(self, cli_query):
		#
		# (3) データを見つけた（= RESPONSE_SUCCEEDED である）ならば、ion.data_request を受けてデータを返す
		#
		if (cli_query == COMMAND_DATAREQUEST):
			svr_response = 'test_data'
			cli_sock.sendall(_encode(svr_response))
			ldprint('<-- ion.server.data_sending(): {}'.format(True))
			return True
		else:
			ldprint('<-- ion.server.data_sending(): {}'.format(False))
			return False
"""

class DB_agent(database_agent):
	pass

class database(database_agent):
	pass

class DB(database_agent):
	pass

class sensor_agent(data_agent):  # Realtime data provider
	_classname = 'ion.sensor_agent'

	@classmethod
	def getClassName(cls):
		return ion._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def update_data(self, query):
		# Update data here.
		pass

class sen_agent(sensor_agent):
	pass

class sensor(sensor_agent):
	pass

class algorithm_agent(server_agent):
	_classname = 'ion.algorithm_agent'

	@classmethod
	def getClassName(cls):
		return ion._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

class algorithmagent(algorithm_agent):
	pass

class alg_agent(algorithm_agent):
	pass

class data_processor(algorithm_agent):
	pass

class processor(data_processor):
	pass

#-- main

if __name__ == '__main__':
	import argparse
	import nkj
	import ion

	_DEBUGLEVEL = 1 
	_LIB_DEBUGLEVEL = 0 
	nkj.str.debuglevel(_DEBUGLEVEL)
	nkj.str.lib_debuglevel(_LIB_DEBUGLEVEL)

	dpv = ion.data_provider()
	dpc = ion.data_processor()
