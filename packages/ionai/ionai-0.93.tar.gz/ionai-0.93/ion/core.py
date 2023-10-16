#
# [name] ion.core.py
# [test] python -m ion.core
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

# nkjlib

from nkj.str import *
import nkj.time as nt

# ionlib

from .const import *

#-- global variance

__NAMESPACE = DEFAULT_NAMESPACE

#-- global functions

def namespace(s=None):
	global __NAMESPACE
	if (s is None):
		return __NAMESPACE
	elif (isinstance(s, str)):
		NAMESPACE = s
		return True
	else:
		return False

def _namespace(s=None):
	return namespace(s)

def is_anystr(s:str):
	return True if (s == STR_ANY) else False

def anystr(s:str):
	return is_anystr(s)

def is_nullstr(s:str):
	return True if (s == STR_NULL) else False

def nullstr(s:str):
	return is_nullstr(s)

def is_nullslot(slot):
	return True if (slot is None) else is_nullstr(slot)

def isnot_nullslot(slot):
	return not is_nullstr(slot)

def nullslot(slot):
	return is_nullslot(slot)

def not_nullslot(slot):
	return isnot_nullslot(slot)

def dictslot_equalsto(dictslot1, dictslot2):
	if (nullslot(dictslot1)):
		return True
	if (nullslot(dictslot2)):
		return True
	return (dictslot1 == dictslot2)

def dictslot_included(dictslot1, dictslot2):
	if (nullslot(dictslot1)):
		return True
	if (nullslot(dictslot2)):
		return True
	return (dictslot1 <= dictslot2)

def dictslot_includes(dictslot1, dictslot2):
	if (nullslot(dictslot1)):
		return True
	if (nullslot(dictslot2)):
		return True
	return (dictslot1 >= dictslot2)

def semantics_equalsto(sem1, sem2):
	if (sem1 is None):
		return False
	if (sem2 is None):
		return False

def semantics_included(sem1, sem2):
	if (sem1 is None):
		return False
	if (sem2 is None):
		return False
	return (sem1 <= sem2)

def semantics_includes(sem1, sem2):
	if (sem1 is None):
		return False
	if (sem2 is None):
		return False
	return (sem1 >= sem2)

#-- classes

class core:
	_classname = 'ion.core'

	def __init__(self):
		ldprint2('core.__init__()')

	@classmethod
	def getClassName(cls):
		return core._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

class strslot(str, core):
	_classname = 'ion.strslot'
	_classkey = KEY_UNKNOWN

	def __new__(cls, val:str=DEFAULT_STRSLOT):
		ldprint2('__new__()')
		val = NULL_SLOT if (val is None) else val
		self = str.__new__(cls, val)
		"""
		self = super().__new__(cls, val)  # 上の行の方が明示的
		"""
		return self

	def __init__(self, val=DEFAULT_STRSLOT):
		ldprint2('__init__()')
		core.__init__(self)

	def __eq__(self, second):
		ldprint('--> strslot.__eq__()')
		ldprint2(second)
		if (isinstance(second, str)):
			ldprint2('str: \'{}\''.format(second))
			ldprint('<-- strslot.__eq__()')
			return True if (is_anystr(self.str) or is_anystr(second)) else (self.str == second)
		else:
			ldprint2('str: \'{0}\' ({1})'.format(second, type(second)))
			ldprint('<-- strslot.__eq__()')
			return True if (is_anystr(self.str) or is_anystr(second.str)) else (self.str == second.str)

	# __ne__() は実装しなくても、__eq__() から自動で実装されるので定義しない．

	def __lt__(self, second):
		if (is_anystr(self.str)):  # 自身が any なら True を返す．
			return True
		t = type(second)

		if (t == tuple or t == list):  # second がリストなら、要素に含まれるか判定
			ldprint2('this: \'{}\''.format(self.str))
			ldprint2('list: {}'.format(second))
			if (isinstance(second[0], str)):
				return self.str in second
			else:
				flag = False
				for slot in second:
					if (self.str == slot.str):
						flag = True
						break
				return flag
		elif (t == str):  # second が文字列なら、文字列の一部に含まれるか判定
			if (is_anystr(second)):  # 相手が any なら True を返す
				return True
			else:
				return (self.str in second) and self.__ne__(second)
		else:
			if (is_anystr(second.str)):  # 相手が any なら True を返す
				return True
			else:
				return (self.str in second.str) and self.__ne__(second)

	def __le__(self, second):
		return (self.__lt__(second) or self.__eq__(second))

	def __gt__(self, second):
		if (is_anystr(self.str)):  # 自身が any なら True を返す．
			return True
		if (isinstance(second, str)):
			return (second in self.str) and self.__ne__(second)
		else:
			return (second.str in self.str) and self.__ne__(second)

	def __ge__(self, second):
		return (self.__gt__(second) or self.__eq__(second))

	@classmethod
	def getClassName(cls):
		return cls._classname

	"""
	___NOT_IMPLEMENTED
	def set(self, val):
		ldprint('--> set(\'{}\')'.format(val))
		self = strslot(val)
		ldprint('<-- set()')
	"""

	def get(self):  # null 文字のとき、None へ変換．
		if (is_nullstr(self)):
			return None
		else:
			return self

	@property
	def str(self) -> str:  # string クラスへ強制変換
		return str(self)

	def equalsto(self, second):
		return self.__eq__(second)

	def not_equalto(self, second):
		return self.equalsto(second)

	def included(self, second):
		return self.__le__(second)

	def not_included(self, second):
		return not self.included(second)

	def includes(self, second):
		return self.__ge__(second)

	def not_includes(self, second):
		return not self.includes(second)

	def startswith(self, second):
		if (is_anystr(self.str)):
			return True
		if (isinstance(second, str)):
			if (is_anystr(second)):
				return True
			return self.str.startswith(second)
		else:
			if (is_anystr(second.str)):
				return True
			return self.str.startswith(second.str)

	def endswith(self, second):
		if (is_anystr(self.str)):
			return True
		if (isinstance(second, str)):
			if (is_anystr(second)):
				return True
			return self.str.endswith(second)
		else:
			if (is_anystr(second.str)):
				return True
			return self.str.endswith(second.str)

	def startsfor(self, second):
		if (is_anystr(self.str)):
			return True
		if (isinstance(second, str)):
			if (is_anystr(second)):
				return True
			return second.startswith(self.str)
		else:
			if (is_anystr(second.str)):
				return True
			return second.str.startswith(self.str)

	def starts(self, second):
		return self.startsfor(second)

	def ends(self, second):
		if (is_anystr(self.str)):
			return True
		if (isinstance(second, str)):
			if (is_anystr(second)):
				return True
			return second.endswith(self.str)
		else:
			if (is_anystr(second.str)):
				return True
			return second.str.endswith(self.str)

	def endsfor(self, second):
		return self.ends(second)

	def getClassKey(self):
		return self._classkey

	@property
	def classkey(self):
		return self.getClassKey()

	def getClassValue(self):
		return self.str

	@property
	def classvalue(self):
		return self.getClassValue()

	@property
	def classval(self):
		return self.classvalue

	def getDict(self):
		return {self.classkey: self.classvalue}

	@property
	def dict(self):
		return self.getDict()

	def getPrintString(self, title=None):
		s = '' if (title is None) else '-- {} --\n'.format(title)
		s += str(self.dict)
		if (title is not None):
			s += '\n--'
		return s

	@property
	def printstr(self):
		return self.getPrintString()

	@property
	def pstr(self):
		return self.getPrintString()

	def print(self, title=None):
		print(self.getPrintString(title), flush=True)

class slot(strslot):
	_classname = 'ion.slot'

	def __new__(cls, val=DEFAULT_SLOT):
		return super().__new__(cls, val)

	def __init__(self, val=DEFAULT_SLOT):
		super().__init__(val)

	@classmethod
	def getClassName(cls):
		return cls._classname

	def get(self):  # null 文字のとき、None へ変換．int および float のとき、それぞれ int、float へ変換．
		s = self
		if (s == ''):
			return None
		elif (is_intstr(s)):
			return int(s)
		elif (is_floatstr(s)):
			return float(s)
		else:
			return self

class role_slot(slot):
	_classname = 'ion.role_slot'
	_classkey = KEY_ROLE

	def __new__(cls, val=None):
		return super().__new__(cls, val)

	@classmethod
	def getClassName(cls):
		return cls._classname

	def getClassKey(self):
		return self._classkey

class entity_slot(slot):
	_classname = 'ion.entity_slot'
	_classkey = KEY_ENTITY

	def __new__(cls, val=None):
		return super().__new__(cls, val)

	@classmethod
	def getClassName(cls):
		return cls._classname

	def getClassKey(self):
		return self._classkey

class baseentity_slot(slot):
	_classname = 'ion.baseentity_slot'
	_classkey = KEY_BASEENTITY

	def __new__(cls, val=None):
		return super().__new__(cls, val)

	@classmethod
	def getClassName(cls):
		return cls._classname

	def getClassKey(self):
		return self._classkey

class dictslot(dict, core):
	_classname = 'ion.dictslot'
	_classkey = KEY_UNKNOWN

	def __init__(self, val:Union[dict, tuple, list, str, None]=None):
		ldprint('--> dictslot.__init__()')
		ldprint2('val: \'{0}\' ({1})'.format(val, type(val)))
		dict.__init__(self)
		if (isinstance(val, dictslot) or isinstance(val, spatial_slot) or isinstance(val, ti_slot) or isinstance(val, optional_slot)):
			val = dict(val)
		d = todict(val)  # dict, tuple, list, str, None -> dict
		for key, value in d.items():
			self.__setitem__(key, value)
		ldprint('<-- dictslot.__init__()')

	# 一致性は、両方の辞書に共通する keys に対して、それらの values が全一致したとき（ただし、any 一致は認める）に一致とみなす
	# 片方のリストにある key がもう一方のリストにない時には、ない方のリスト要素を any とみなす = すなわち、「指定なし」＝any として、その key については一致とみなす

	def __eq__(self, second:Union[dict, str, None]):
		if (second is None):  # second が None なら True
			return True
		if (type(second) == str):
			second = json.loads(second)  # str -> dict
		if (is_nulldict(self) or is_nulldict(second)):  # どちらかの辞書に要素がなければ True
			return True
		"""
		anditems = [(key, value) for key, value in self.items() if (slot(value) == slot(second.get(key)))]  # value を slot として一致性比較 = any 一致を認める
		print(anditems)
		"""
		mismatchitems = [(key, value, second.get(key)) for key, value in self.items() if (slot(value) != slot(second.get(key)))]  # value を slot として一致性比較 = any 一致を認める
		if (is_nulllist(mismatchitems)):
			return True
		else:
			return False

	def __lt__(self, second:Union[dict, str, None]):
		if (second is None):
			return False
		if (type(second) == str):
			second = json.loads(second)  # str -> dict
		if (is_nulldict(self) or is_nulldict(second)):  # どちらかの辞書に要素がなければ False
			return False
		mismatchitems = [(key, value, second.get(key)) for key, value in self.items() if (slot(value) < slot(second.get(key)))]  # value を slot として被包含性比較 = any 包含を認める
		if (is_nulllist(mismatchitems)):
			return False
		else:
			return True

	def __le__(self, second:Union[dict, str, None]):
		return (self.__lt__(second) or self.__eq__(second))

	def __gt__(self, second:Union[dict, str, None]):
		if (second is None):
			return False
		if (type(second) == str):
			second = json.loads(second)  # str -> dict
		if (is_nulldict(self) or is_nulldict(second)):  # どちらかの辞書に要素がなければ False
			return False
		mismatchitems = [(key, value, second.get(key)) for key, value in self.items() if (slot(value) > slot(second.get(key)))]  # value を slot として被包含性比較 = any 包含を認める
		if (is_nulllist(mismatchitems)):
			return False
		else:
			return True

	def __ge__(self, second:Union[dict, str, None]):
		return (self.__gt__(second) or self.__eq__(second))

	@classmethod
	def getClassName(cls):
		return dictslot._classname

	def getClassKey(self):
		return self._classkey

	@property
	def classkey(self):
		return self.getClassKey()

	def equalsto(self, second):
		return self.__eq__(second)

	def not_equalto(self, second):
		return self.equalsto(second)

	def included(self, second):
		return self.__le__(second)

	def not_included(self, second):
		return not self.included(second)

	def includes(self, second):
		return self.__ge__(second)

	def not_includes(self, second):
		return not self.includes(second)

	def getPrintString(self, title=None):
		s = ''
		if (title is not None):
			s += '--- {} ---\n'.format(title)
		s += json.dumps(self)  # dict -> str
		if (title is not None):
			s += '\n---'
		return s

	@property
	def printstr(self):
		return self.getPrintString()

	@property
	def pstr(self):
		return self.getPrintString()

	def print(self, title=None):
		if (title is not None):
			print('--- {} ---'.format(title))
		pprint.pprint(self.printstr)
		if (title is not None):
			print('---', flush=True)
		else:
			sys.stdout.flush()

	def getClassValue(self):
		return copy.deepcopy(dict(self))

	@property
	def classvalue(self):
		return self.getClassValue()

	def getDict(self):
		return {self.classkey: self.classvalue}

	def addDict(self, d):
		for key, value in d.items():
			self[key] = value

	def setDict(self, d):
		self.clear()
		self.addDict(d)

	@property
	def dict(self):
		return self.getDict()

	@dict.setter
	def dict(self, d):
		self.setDict(d)

	# json.{loads(), dumps()}: dict データと string データの変換
	# json.{load(), dump()}:   JSON ファイルの読み書き

	def getJSONStr(self):
		try:
			s = json.dumps(self)  # dict -> str
			return s
		except TypeError:
			return None

	def setJSONStr(self, s:str):
		try:
			json.loads(s)
		except TypeError:
			return False
		else:
			return True

	@property
	def jsonstr(self):
		return self.getJSON()

	@jsonstr.setter
	def jsonstr(self, s:str):
		self.setJSON(s)

	def add(self, c):  # add a component
		if (isinstance(c, list) or isinstance(c, tuple)):
			if (len(c) % 2 == 0):
				for i in range(len(c) / 2):
					key = c[2 * i]
					val = c[2 * i + 1]
					ldprint2('key: {0}, val: {1}'.format(key, val))
					self[key] = val
			else:
				__ERROR__
		else:
			__ERROR__

	def remove(self, k):  # remove a component
		del self[k]

	def delete(self, k):  # remove a component
		self.remove(k)

	def load(self, filename=None):
		filename = self.getFilename() if (filename is None) else filename
		if (filename is None):
			return False
		with open(filename) as f:
			self = json.load(f)

	def save(self, filename=None):
		filename = self.getFilename() if (filename is None) else filename
		if (filename is None):
			return False
		with open(filename, 'wt') as f:  # テキストモードで書き出し
			json.dump(self, f)

class spatial_slot(dictslot):  # spatial identifier
	_classname = 'ion.spatial_slot'
	_classkey = KEY_SPATIAL

	def __init__(self, val:Union[dict, tuple, list, str, None]=None):
		ldprint('--> ion.spatial_slot.__init__({0} ({1})'.format(val, type(val)))
		super().__init__()
		if (False): # Default value setting
			self[KEY_DIMENSION] = DEFAULT_DIMENSION
		if (val is None):
			pass
		elif (isinstance(val, dict)):
			super().__init__(copy.deepcopy(val))
		elif (isinstance(val, str)):
			self[KEY_INDEX] = val
		elif (isinstance(val, set)):
			key, val = val
			ldprint2('key: \'{0}\', val: \'{1}\''.format(key, val))
			self[key] = val
		elif (isinstance(val, list) or isinstance(val, tuple)):
			if (len(val) % 2 == 0):
				for i in range(len(val) / 2):
					key = val[2 * i]
					val = val[2 * i + 1]
					ldprint2('key: {0}, val: {1}'.format(key, val))
					self[key] = val
			else:
				__ERROR__
		else:
			__ERROR__
	ldprint('<-- ion.spatial_slot.__init__()')

	@classmethod
	def getClassName(cls):
		return dictslot._classname

	def getClassKey(self):
		return self._classkey

class si_slot(spatial_slot):
	pass

class temporal_slot(dictslot):  # temporal identifier
	_classname = 'ion.temporal_slot'
	_classkey = KEY_TEMPORAL

	def __init__(self, t=STR_TIME_PRESENT):
		ldprint('--> ion.temporal_slot.__init__({0} ({1}))'.format(t, type(t)))
		super().__init__()
		if (t is None):
			ldprint2('None: {}'.format(t))
			self.time = None
		elif (isinstance(t, dict)):
			ldprint2('dict: {}'.format(t))
			super().__init__(t)
		elif (isinstance(t, set)):
			ldprint2('set: {}'.format(t))
			key, val = t
			ldprint2('key: \'{0}\', val: \'{1}\''.format(key, val))
			self[key] = val
		elif (isinstance(t, temporal_slot)):
			ldprint2('temporal_slot: {}'.format(t))
			self.time = t.time
		elif (isinstance(t, str)):
			ldprint2('str: {}'.format(t))
			if (t == STR_TIME_PRESENT):
				self.update_time()
			elif (t == STR_ANY):
				self.time = None
			else:
				self.time = t
		elif (isinstance(t, list) or isinstance(t, tuple)):
			ldprint2('list: {}'.format(t))
			if (len(t) % 2 == 0):
				for i in range(len(t) / 2):
					key = t[2 * i]
					val = t[2 * i + 1]
					ldprint2('key: {0}, val: {1}'.format(key, val))
					if (key == KEY_TIME):
						if (val == STR_TIME_PRESENT):
							self.update_time()
						else:
							self[key] = val
					else:
						self[key] = val
			else:
				__ERROR__
		else:
			__ERROR__
		ldprint('<-- ion.temporal_slot.__init__()')

	"""
	def __lt__(self, second:si_slot):  # 記号の意味としては、本来は等価を含まないが、実装の都合上、ここでは含むものとする
		return self.__le__(second)
	"""

	def __le__(self, second:si_slot):
		return self.included(second)

	"""
	def __gt__(self, second:si_slot):  # 記号の意味としては、本来は等価を含まないが、実装の都合上、ここでは含むものとする
		return self.__ge__(second)
	"""

	def __ge__(self, second:si_slot):
		return self.includes(second)

	@classmethod
	def getClassName(cls):
		return dictslot._classname

	def getClassKey(self):
		return self._classkey

	@property
	def time(self):
		return self.get(KEY_TIME)

	@time.setter
	def time(self, t):
		if (t is None):
			if (self.get(KEY_TIME) is not None):
				del self[KEY_TIME]
		else:
			if (t == STR_TIME_PRESENT):
				self.update_time()
			else:
				self[KEY_TIME] = t

	@property
	def timeperiod(self):
		return self.get(KEY_TIMEPERIOD)

	@timeperiod.setter
	def timeperiod(self, tp):
		ldprint('--> timeperiod.setter(\'{0}\' ({1}))'.format(tp, type(tp)))
		if (tp is None):
			del self[KEY_TIMEPERIOD]
		else:
			self[KEY_TIMEPERIOD] = tp

	def update_time(self):
		self.time = datetime.datetime.now().strftime(TIMEDESCRIPTION)  # python datetime のデフォルト書式で記述

	def clear_timeperiod(self):
		self.timeperiod = SLOT_ANY

	def included(self, second:si_slot):
		if (self.time is None or second.time is None):  # 記述がないときは any とみなして True
			return True
		if (is_anystr(self.time) or is_anystr(second.time)):  # どちらかが any のときは True. any は基本的には記述なしで対応するのでできるだけ使用しないこと．
			return True
		return (self == second) or (nt.time(self.time, self.timeperiod) <= nt.time(second.time, second.timeperiod))

	def includes(self, second:si_slot):
		if (self.time is None or second.time is None):  # 記述がないときは any とみなして True
			return True
		if (is_anystr(self.time) or is_anystr(second.time)):  # どちらかが any のときは True. any は基本的には記述なしで対応するのでできるだけ使用しないこと．
			return True
		return (self == second) or (nt.time(self.time, self.timeperiod) >= nt.time(second.time, second.timeperiod))

class ti_slot(temporal_slot):
	pass

class optional_slot(dictslot):  # optional identifier
	_classname = 'ion.optional_slot'
	_classkey = KEY_OPTIONAL

	@classmethod
	def getClassName(cls):
		return dictslot._classname

	def getClassKey(self):
		return self._classkey

class role(role_slot):
	pass

class entity(entity_slot):
	pass

class baseentity(baseentity_slot):
	pass

class spatial(spatial_slot):
	pass

class si(si_slot):
	pass

class temporal(temporal_slot):
	pass

class ti(ti_slot):
	pass

class optional(optional_slot):
	pass

class oi(optional_slot):
	pass

class semantics_cls():
	_classname = 'ion.semantics'
	_classkey = KEY_SEMANTICS

	def __init__(self, semantics=None, namespace=None):
		ldprint('--> semantics.__init__(\'{0}\' ({1}), \'{2}\' ({3}))'.format(semantics, type(semantics), namespace, type(namespace)))
		namespace = _namespace() if (namespace is None) else namespace
		self.setNameSpace(namespace)
		self.setSemantics(semantics)
		ldprint('namespace:   \'{}\''.format(self.namespace))
		ldprint('role:        \'{}\''.format(self.role))
		ldprint('entity:      \'{}\''.format(self.entity))
		ldprint('base entity: \'{}\''.format(self.baseentity))
		ldprint('spatial:     \'{}\''.format(self.spatial))
		ldprint('temporal:    \'{}\''.format(self.temporal))
		ldprint('options:     \'{}\''.format(self.optional))
		ldprint('<-- semantics.__init__()')

	def __str__(self):
		return self.getPrintString()

	def __eq__(self, second):
		r = True
		r &= (self.entity == second.entity)
		r &= (self.baseentity == second.baseentity)
		r &= (self.role == second.role)
		if (not any(self.si)):
			r &= (self.si == second.si)
		if (not any(self.ti)):
			r &= (self.ti == second.ti)
		if (not any(self.optional)):
			r &= (self.optional == second.optional)
		return r

	def __lt__(self, second):
		return (self.__lt__(second) and not self.__eq__(second))

	def __le__(self, second):
		r = True
		r &= (self.entity <= second.entity)
		r &= (self.baseentity <= second.baseentity)
		r &= (self.role <= second.role)
		if (any(self.si)):
			r &= (self.si <= second.si)
		if (any(self.ti)):
			r &= (self.ti <= second.ti)
		if (any(self.optional)):
			r &= (self.optional <= second.optional)
		return r

	def __gt__(self, second):
		return (self.__gt__(second) and not self.__eq__(second))

	def __ge__(self, second):
		r = True
		r &= (self.entity >= second.entity)
		r &= (self.baseentity >= second.baseentity)
		r &= (self.role >= second.role)
		if (any(self.si)):
			r &= (self.si >= second.si)
		if (any(self.ti)):
			r &= (self.ti >= second.ti)
		if (any(self.optional)):
			r &= (self.optional >= second.optional)
		return r

	@classmethod
	def getClassName(cls):
		return semantics._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def getClassKey(self):
		return self._classkey

	@property
	def classkey(self):
		return self.getClassKey()

	def getNameSpace(self):
		if (self._namespace is not None):
			return self._namespace
		else:
			return namespace()  # call global function

	def setNameSpace(self, ns):
		self._namespace = ns

	@property
	def namespace(self):
		return self.getNameSpace()

	@namespace.setter
	def namespace(self, ns):
		self.setNameSpace(ns)

	@property
	def ns(self):
		return self.namespace

	@ns.setter
	def ns(self, ns_):
		self.namespace = ns_

	def getSemantics(self):
		return copy.deepcopy(self)

	def setSemantics(self, val):
		if (val is None):
			self._role = role_slot(None)           # role
			self._entity = entity_slot(None)       # entity
			self._bentity = baseentity_slot(None)  # base entity (optional)
			self._spatial = spatial_slot(None)     # spatial identifier
			self._temporal = temporal_slot(None)   # temporal identifier
			self._optional = optional_slot(None)   # optional properties
		elif (isinstance(val, dict)):
			d = copy.deepcopy(val)
			self._role = role_slot(d.get(KEY_ROLE))                # role
			self._entity = entity_slot(d.get(KEY_ENTITY))          # entity
			self._bentity = baseentity_slot(d.get(KEY_BASEENTITY)) # base entity (optional)
			self._spatial = spatial_slot(d.get(KEY_SPATIAL))       # spatial identifier
			self._temporal = temporal_slot(d.get(KEY_TEMPORAL))    # temporal identifier
			self._optional = optional_slot(d.get(KEY_OPTIONAL))    # optional properties
		elif (isinstance(val, str) or isinstance(val, tuple) or isinstance(val, list)):
			d = todict(val)
			self._role = role_slot(d.get(KEY_ROLE))                # role
			self._entity = entity_slot(d.get(KEY_ENTITY))          # entity
			self._bentity = baseentity_slot(d.get(KEY_BASEENTITY)) # base entity (optional)
			self._spatial = spatial_slot(d.get(KEY_SPATIAL))       # spatial identifier
			self._temporal = temporal_slot(d.get(KEY_TEMPORAL))    # temporal identifier
			self._optional = optional_slot(d.get(KEY_OPTIONAL))    # optional properties
		elif (isinstance(val, semantics_cls)):
			self._role = val._role
			self._entity = val._entity
			self._bentity = val._bentity
			self._spatial = val._spatial
			self._temporal = val._temporal
			self._optional = val._optional
		else:
			__ERROR__

	@property
	def semantics(self):
		return self.getSemantics()

	@property
	@semantics.setter
	def semantics(self, s):
		self.setSemantics(s)

	def get(self):
		return self.getSemantics()

	def set(self, val):
		self.setSemantics(val)

	@property
	def role(self):
		return self._role

	@role.setter
	def role(self, val):
		self._role = role_slot(val)

	@property
	def r(self):
		return self.role

	@r.setter
	def r(self, val):
		self.role = val

	@property
	def entity(self):
		return self._entity

	@entity.setter
	def entity(self, val):
		self._entity = entity_slot(val)

	@property
	def e(self):
		return self.entity

	@e.setter
	def e(self, val):
		self.entity = val

	@property
	def baseentity(self):
		return self._bentity

	@baseentity.setter
	def baseentity(self, val):
		self._bentity = baseentity_slot(val)

	@property
	def bentity(self):
		return self.baseentity

	@bentity.setter
	def bentity(self, val):
		self.baseentity = val

	@property
	def be(self):
		return self.baseentity

	@be.setter
	def be(self, val):
		self.baseentity = val

	@property
	def spatialidentifier(self):
		return self.spatial

	@spatialidentifier.setter
	def spatialidentifier(self, si):
		self.spatial = si

	@property
	def spatial(self):
		return self._spatial

	@spatial.setter
	def spatial(self, si):
		self._spatial = spatial_slot(si)

	@property
	def si(self):
		return self.spatial

	@si.setter
	def si(self, si_):
		self.spatial = si_

	@property
	def s(self):
		return self.si

	@s.setter
	def s(self, si):
		self.spatial = si

	@property
	def temporalidentifier(self):
		return self.temporal

	@temporalidentifier.setter
	def temporalidentifier(self, ti):
		self.temporal = ti

	@property
	def temporal(self):
		return self._temporal

	@temporal.setter
	def temporal(self, t):
		self._temporal = temporal_slot(t)

	@property
	def ti(self):
		return self.temporal

	@ti.setter
	def ti(self, t):
		self.temporal = t

	@property
	def t(self):
		return self.temporal

	@t.setter
	def t(self, t_):
		self.temporal = t_

	@property
	def time(self):
		return self.temporal.time

	@time.setter
	def time(self, t):
		self.temporal.time = t

	@property
	def timeperiod(self):
		return self.temporal.timeperiod

	@timeperiod.setter
	def timeperiod(self, tp):
		self.temporal.timeperoid = tp

	@property
	def optionalidentifier(self):
		return self.optional

	@optionalidentifier.setter
	def optionalidentifier(self, o):
		self.optional = o

	@property
	def optional(self):
		return self._optional

	@optional.setter
	def optional(self, o):
		self._optional = optional_slot(o)

	@property
	def oi(self):
		return self.optional

	@oi.setter
	def oi(self, o):
		self.optional = o

	@property
	def o(self):
		return self.optional

	@o.setter
	def o(self, o_):
		self.optional = o_

	def equalsto(self, second):
		return self.__eq__(second)

	def not_equalto(self, second):
		return self.equalsto(second)

	def included(self, second):
		return self.__le__(second)

	def not_included(self, second):
		return not self.included(second)

	def includes(self, second):
		return self.__ge__(second)

	def not_includes(self, second):
		return not self.includes(second)

	def getClassValue(self):
		d = {**self.entity.dict, **self.baseentity.dict, **self.role.dict}
		if (self.si is not None):
			d = dict(d, **self.si.dict)
		if (self.ti is not None):
			d = dict(d, **self.ti.dict)
		if (self.optional is not None):
			d = dict(d, **self.optional.dict)
		return copy.deepcopy(d)

	@property
	def classvalue(self):
		return self.getClassValue()

	def getDict(self):
		return {self.classkey: self.classvalue}

	def setDict(self, d):
		d = copy.deepcopy(d)
		if (d.get(KEY_SEMANTICS) is not None):
			d = d.get(KEY_SEMANTICS)
		subd = d.get(KEY_ENTITY)
		if (subd is not None):
			self.entity = subd
		subd = d.get(KEY_BASEENTITY)
		if (subd is not None):
			self.baseentity = subd
		subd = d.get(KEY_ROLE)
		if (subd is not None):
			self.role = subd
		subd = d.get(KEY_SPATIAL)
		if (subd is not None):
			self.si = subd
		subd = d.get(KEY_TEMPORAL)
		if (subd is not None):
			self.ti = subd
		subd = d.get(KEY_OPTIONAL)
		if (subd is not None):
			self.optional = subd

	@property
	def dict(self):
		return self.getDict()

	@dict.setter
	def dict(self, d):
		self.setDict(d)

	def getPrintString(self, title=None):
		s = ''
		if (title is not None):
			s += '--- {} ---\n'.format(title)
		s += 'role:        \'{}\'\n'.format(self.role)
		s += 'entity:      \'{}\'\n'.format(self.entity)
		s += 'base entity: \'{}\'\n'.format(self.baseentity)
		if (any(self.si)):
			s += 'spatial:     '
			s += self.si.getPrintString()
			s += '\n'
		if (any(self.ti)):
			s += 'temporal:    '
			s += self.ti.getPrintString()
			s += '\n'
		if (any(self.optional)):
			s += 'optional:    '
			s += self.optional.getPrintString()
			s += '\n'
		if (title is not None):
			s += '---'
		return s

	@property
	def printstr(self):
		return self.getPrintString()

	@property
	def pstr(self):
		return self.getPrintString()

	def print(self, title=None):
		print(self.getPrintString(title), flush=True)

class semantics(semantics_cls):
	pass

class databody_slot(core):
	_classname = 'ion.databody_slot'
	_classkey = KEY_DATABODY

	def __init__(self, val=None):
		self._data = None
		self.setData(val)

	@classmethod
	def getClassName(cls):
		return databody._classname

	def getClassKey(self):
		return self._classkey

	@property
	def classkey(self):
		return self.getClassKey()

	def __binary_encode(self, d):
		ldprint3('--> ion.databody_slot._binary_encode()')
		ldprint3('<-- ion.databody_slot._binary_encode()')
		return pickle.dumps(d)

	def __binary_decode(self, d):
		ldprint3('--> ion.databody_slot._binary_decode()')
		ldprint3('<-- ion.databody_slot._binary_decode()')
		return pickle.loads(d)

	def __encode(self, d):
		ldprint3('--> ion.databody_slot._encode()')
		ldprint3('<-- ion.databody_slot._encode()')
		return json.dumps(d)

	def __decode(self, d):
		ldprint3('--> ion.databody_slot._decode()')
		ldprint3('<-- ion.databody_slot._decode()')
		return json.loads(d)

	def getStoreData(self):
		return self._data

	def setStoreData(self, d):
		self._data = d

	@property
	def storedata(self):
		return self.getStoreData()

	@storedata.setter
	def storedata(self, d):
		self.setStoreData(d)

	@property
	def store(self):
		return self.getStoreData()

	@store.setter
	def store(self, d):
		self.setStoreData(d)

	def isNullData(self):
		return (self.getStoreData() is None)

	def isNull(self):
		return self.isNullData()

	def nulldata(self):
		return self.isNullData()

	def null(self):
		return self.nulldata()

	def getData(self):
		if (self.isNullData()):
			return None
		else:
			if (isinstance(self.getStoreData(), bytes)):
				return self.__binary_decode(self.getStoreData())
			else:
				return self.__decode(self.getStoreData())

	def setData(self, d):
		ldprint2('--> ion.databody_slot.setData({0} ({1}))'.format(d, type(d)))

		if (d is None):
			pass

		else:
			# Data conversion

			ldprint3('Is bytes:  {}'.format(isinstance(d, bytes)))

			if (isinstance(d, bytes)):
				d = self.__binary_encode(d)
			else:
				d = self.__encode(d)

		self.setStoreData(d)

		ldprint2('<-- ion.databody_slot.setData()')

	def get(self):
		return self.getData()

	def set(self, d):
		self.setData(d)

	def getDataBody(self):
		return self.getData()

	def setDataBody(self, d):
		self.setData(d)

	def getBody(self):
		return self.getDataBody()

	def setBody(self, d):
		self.setDataBody(d)

	@property
	def data(self):
		return self.getData()

	@data.setter
	def data(self, d):
		self.setData(d)

	@property
	def databody(self):
		return self.getDataBody()

	@data.setter
	def databody(self, d):
		self.setDataBody(d)

	@property
	def body(self):
		return self.getDataBody()

	@body.setter
	def body(self, d):
		self.setDataBody(d)

	def getDataType(self):
		return type(self.getData())

	@property
	def datatype(self):
		return self.getDataType()

	def getType(self):
		return self.getDataType()

	@property
	def type(self):
		return self.getType()
	
	def isBytes(self):
		return isinstance(self.getData(), bytes)

	def is_bytes(self):
		return self.isBytes()

	def isBinary(self):
		return self.isBytes()

	def is_binary(self):
		return self.isBinary()

class dataproperty_slot(dictslot):  # data properties
	_classname = 'ion.dataproperty_slot'
	_classkey = KEY_DATAPROPERTY

	def __init__(self, val:Union[dict, str, None]=None):
		super().__init__(val)

	@classmethod
	def getClassName(cls):
		return dictslot._classname

	def getClassKey(self):
		return self._classkey

	@property
	def format(self):
		return self.get(KEY_DATAFORMAT)

	@format.setter
	def format(self, f):
		if (f is None):
			del self[KEY_DATAFORMAT]
		self[KEY_DATAFORMAT] = f

	@property
	def unit(self):
		return self.get(KEY_DATAUNIT)

	@unit.setter
	def unit(self, u):
		if (u is None):
			del self[KEY_DATAUNIT]
		self[KEY_DATAUNIT] = u

	def setDict(self, d):
		if (d.get(KEY_DATAPROPERTY) is not None):
			d = d.get(KEY_DATAPROPERTY)
		super().setDict(d)

class data_body(databody_slot):
	pass

class databody(data_body):
	pass

class dbody(data_body):
	pass

class data_property(dataproperty_slot):
	pass

class dataproperty(data_property):
	pass

class dproperty(data_property):
	pass

class data_storage(core):  # The class name of 'data' is prohibited and might be used in python system.
	_classname = 'ion.data'

	def __init__(self, body=None, property=None, namespace=None):
		ldprint('--> data.__init__(, \'{0}\', \'{1}\')'.format(property, namespace))
		self.setNameSpace(namespace)
		ldprint('namespace:   \'{}\''.format(self.namespace))
		super().__init__()
		self._body = databody_slot(body)
		self._property = dataproperty_slot(property)
		ldprint('<-- data.__init__()')

	@classmethod
	def getClassName(cls):
		return data_storage._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def getNameSpace(self):
		if (self._namespace is not None):
			return self._namespace
		else:
			return namespace()  # call global function

	def setNameSpace(self, ns):
		self._namespace = ns

	@property
	def namespace(self):
		return self.getNameSpace()

	@namespace.setter
	def namespace(self, ns):
		self.setNameSpace(ns)

	@property
	def ns(self):
		return self.namespace

	@ns.setter
	def ns(self, ns_):
		self.namespace = ns_

	@property
	def databody(self):
		return self._body.get()

	@databody.setter
	def databody(self, d):
		self._body.set(d)

	@property
	def dbody(self):
		return self.databody

	@dbody.setter
	def dbody(self, d):
		self.databody = d

	@property
	def db(self):
		return self.databody

	@db.setter
	def db(self, d):
		self.databody = d

	@property
	def body(self):
		return self.databody

	@body.setter
	def body(self, d):
		self.databody = d

	@property
	def b(self):
		return self.databody

	@b.setter
	def b(self, d):
		self.databody = d

	@property
	def dataproperty(self):
		return self._property

	@dataproperty.setter
	def dataproperty(self, p):
		self._property = dataproperty_slot(p)

	@property
	def dproperty(self):
		return self.dataproperty

	@dproperty.setter
	def dproperty(self, p):
		self.dataproperty = p

	@property
	def dp(self):
		return self._property

	@dp.setter
	def dp(self, p):
		self.dataproperty = p

	# 'property' is not available for the name of 'class property' in python

	@property
	def p(self):
		return self._property

	@p.setter
	def p(self, p_):
		self.dataproperty = p_

	@property
	def dataformat(self):
		return self.dataproperty.format

	@dataformat.setter
	def dataformat(self, f):
		self.dataproperty.format = f

	@property
	def format(self):
		return self.dataformat

	@format.setter
	def format(self, f):
		self.dataformat = f

	@property
	def f(self):
		return self.dataformat

	@f.setter
	def f(self, f):
		self.dataformat = f

	@property
	def df(self):
		return self.dataformat

	@df.setter
	def df(self, f):
		self.dataformat = f

	@property
	def dataunit(self):
		return self.dataproperty.unit

	@dataunit.setter
	def dataunit(self, u):
		self.dataproperty.unit = u

	@property
	def unit(self):
		return self.dataunit

	@unit.setter
	def unit(self, u):
		self.dataunit = u

	@property
	def u(self):
		return self.dataunit

	@u.setter
	def u(self, u):
		self.dataunit = u

	@property
	def du(self):
		return self.dataunit

	@du.setter
	def du(self, u):
		self.dataunit = u

	def getPrintString(self, title=None):
		s = ''
		if (title is not None):
			s += '--- {} ---\n'.format(title)
		s += 'data body:     '
		if (self.databody is None):
			s += 'None\n'
		else:
			s += '{} bytes'.format(self.databody.__sizeof__())
			if (type(self.databody) == str):
				s += ' (\'{0}\', {1} characters)'.format(self.databody, len(self.databody))
			s += '\n'
		s += 'data property: '
		s += self.dataproperty.getPrintString()
		if (title is not None):
			s += '\n---'
		return s

	@property
	def printstr(self):
		return self.getPrintString()

	@property
	def pstr(self):
		return self.getPrintString()

	def print(self, title=None):
		print(self.getPrintString(title), flush=True)

class datastorage(data_storage):  # alias
	pass

class query():
	_classname = 'ion.query'

	def __init__(self, val=None):
		ldprint('--> query.__init__({0} ({1}))'.format(val, type(val)))
		if (val is None):
			self._semantics = semantics_cls()
			self._semantics.temporal.clear()  # query では基本的に時間をクリアしておく．
			self._dataproperty = dataproperty_slot()
			self.setQuery((semantics, dataproperty))
		elif (isinstance(val, query)):
			self.setQuery(val)
		elif (isinstance(val, str)):
			self.setQuery(val)
		elif (isinstance(val, list) or isinstance(val, tuple)):
			self.setQuery(val)
		else:
			__ERROR__
		ldprint('<-- query.__init__()')

	@classmethod
	def getClassName(cls):
		return data_storage._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def getQuery(self):
		return self.getDict()  # dict

	def setQuery(self, q):
		ldprint('--> ion.query.setQuery({0} ({1}))'.format(q, type(q)))
		if (isinstance(q, query)):
			ldprint2('class: query')
			self.setSemantics(q.getSemantics())
			self.setDataProperty(q.getDataProperty())
		elif (isinstance(q, str)):
			ldprint2('class: str')
			dic = json.loads(q)
			sem = dic.get(KEY_SEMANTICS)
			if (sem is None):
				__ERROR__
			self.setSemantics(sem)
			dp = dic.get(KEY_DATAPROPERTY)
			if (dp is None):
				__ERROR__
			self.setDataProperty(dp)
		elif (isinstance(q, tuple) or isinstance(q, list)):
			ldprint2('class: list')
			self.setSemantics(q[0])
			self.setDataProperty(q[1])
		else:
			__ERROR__
		if (lib_debuglevel() > 0):
			print('-- semantics')
			self.getSemantics().print('semantics')
			print('-- data property')
			pprint.pprint(self.getDataProperty())
			print('--')
		ldprint('<-- ion.query.setQuery()')

	def __eq__(self, second):
		r = True
		r &= (self.semantics == second.semantics)
		r &= (self.dataproperty == second.dataproperty)
		return r

	def __lt__(self, second):
		return (self.__lt__(second) and not self.__eq__(second))

	def __le__(self, second):
		r = True
		r &= (self.semantics <= second.semantics)
		r &= (self.dataproperty <= second.dataproperty)
		return r

	def __gt__(self, second):
		return (self.__gt__(second) and not self.__eq__(second))

	def __ge__(self, second):
		r = True
		r &= (self.semantics >= second.semantics)
		r &= (self.dataproperty >= second.dataproperty)
		return r

	@property
	def query(self):
		return self.getQuery()

	@query.setter
	def query(self, q):
		self.setQuery(q)

	@property
	def q(self):
		return self.guery

	@q.setter
	def q(self, q):
		self.query = q

	def getSemantics(self):
		return self._semantics

	def setSemantics(self, sem):
		ldprint('--> ion.query.setSemantics()')
		if (sem is None):
			self._semantics = semantics_cls()
		else:
			if (isinstance(sem, str)):
				sem = json.loads(sem)
			if (isinstance(sem, dict)):
				self._semantics = semantics_cls(copy.deepcopy(sem))
		ldprint('<-- ion.query.setSemantics()')

	@property
	def semantics(self):
		return self.getSemantics()

	@semantics.setter
	def semantics(self, sem):
		self.setSemantics(sem)

	@property
	def sem(self):
		return self.semantics

	@sem.setter
	def sem(self, sem_):
		self.semantics = sem_

	@property
	def s(self):
		return self.semantics

	@s.setter
	def s(self, sem_):
		self.semantics = sem_

	def getDataProperty(self):
		return self._dataproperty

	def setDataProperty(self, dp):
		ldprint('--> ion.query.setDataProperty()')
		if (dp is None):
			self._dataproperty = dataproperty_slot()
		else:
			if (isinstance(dp, str)):
				dp = json.loads(dp)
			if (isinstance(dp, dict)):
				self._dataproperty = dataproperty_slot(copy.deepcopy(dp))
		ldprint('<-- ion.query.setDataProperty()')

	@property
	def dataproperty(self):
		return self.getDataProperty()

	@dataproperty.setter
	def dataproperty(self, dp):
		self.setDataProperty(dp)

	@property
	def data_property(self):
		return self.dataproperty

	@data_property.setter
	def data_property(self, dp):
		self.dataproperty = dp

	@property
	def dp(self):
		return self.dataproperty

	@dp.setter
	def dp(self, dp):
		self.dataproperty = dp

	def equalsto(self, second):
		return self.__eq__(second)

	def not_equalto(self, second):
		return self.equalsto(second)

	def included(self, second):
		return self.__le__(second)

	def not_included(self, second):
		return not self.included(second)

	def includes(self, second):
		return self.__ge__(second)

	def not_includes(self, second):
		return not self.includes(second)

	@property
	def role(self):
		return self.semantics.role

	@role.setter
	def role(self, r):
		self.semantics.role = r

	@property
	def r(self):
		return self.role

	@r.setter
	def r(self, r_):
		self.role = r_

	@property
	def entity(self):
		return self.semantics.entity

	@entity.setter
	def entity(self, e):
		self.semantics.entity = e

	@property
	def e(self):
		return self.entity

	@e.setter
	def e(self, e_):
		self.entity = e_

	@property
	def baseentity(self):
		return self.semantics.baseentity

	@baseentity.setter
	def baseentity(self, be):
		self.semantics.baseentity = be

	@property
	def be(self):
		return self.baseentity

	@be.setter
	def be(self, be_):
		self.baseentity = be_

	@property
	def spatial(self):
		return self.semantics.spatial

	@spatial.setter
	def spatial(self, s):
		self.semantics.spatial = s

	@property
	def si(self):
		return self.semantics.spatial

	@si.setter
	def si(self, s):
		self.semantics.spatial = s

	@property
	def s(self):
		return self.semantics.spatial

	@s.setter
	def s(self, s_):
		self.semantics.spatial = s_

	@property
	def temporal(self):
		return self.semantics.temporal

	@temporal.setter
	def temporal(self, t):
		self.semantics.temporal = t

	@property
	def ti(self):
		return self.semantics.temporal

	@ti.setter
	def ti(self, t):
		self.semantics.temporal = t

	@property
	def t(self):
		return self.semantics.temporal

	@t.setter
	def t(self, t_):
		self.semantics.temporal = t_

	@property
	def optional(self):
		return self.semantics.optional

	@optional.setter
	def optional(self, o):
		self.semantics.optional = o

	@property
	def oi(self):
		return self.optional

	@oi.setter
	def oi(self, o):
		self.optional = o

	@property
	def o(self):
		return self.optional

	@o.setter
	def o(self, o_):
		self.optional = o_

	@property
	def dataformat(self):
		return self.dataproperty.format

	@dataformat.setter
	def dataformat(self, f):
		self.dataproperty.format = f

	@property
	def format(self):
		return self.dataformat

	@format.setter
	def format(self, f):
		self.dataformat = f

	@property
	def f(self):
		return self.dataformat

	@f.setter
	def f(self, f_):
		self.dataformat = f_

	@property
	def dataunit(self):
		return self.dataproperty.unit

	@dataunit.setter
	def dataunit(self, u):
		self.dataproperty.unit = u

	@property
	def unit(self):
		return self.dataunit

	@unit.setter
	def unit(self, u):
		self.dataunit = u

	@property
	def u(self):
		return self.dataunit

	@u.setter
	def u(self, u_):
		self.dataunit = u_

	def getDict(self):
		d = {}
		if (self.semantics is not None):
			d = {**d, **self.semantics.dict}
		if (self.dataproperty is not None):
			d = {**d, **self.dataproperty.dict}
		return copy.deepcopy(d)

	def setDict(self, d):
		semd = d.get(KEY_SEMANTICS)
		if (semd is not None):
			if (False):
				self.semantics.dict = {KEY_SEMANTICS: semd}  # version #1
			else:
				self.semantics.dict = semd                    # version #2
		propd = d.get(KEY_DATAPROPERTY)
		if (propd is not None):
			if (False):
				self.dataproperty.dict = {KEY_DATAPROPERTY: propd}  # version #1
			else:
				self.dataproperty.dict = propd                       # version #2

	@property
	def dict(self):
		return self.getDict()

	@dict.setter
	def dict(self, d):
		self.setDict(d)

	def getTuple(self):
		return (self.getSemantics(), self.getDataProperty())

	def setTuple(self, t):
		self.setSemantics(t[0])
		self.setDataProperty(t[1])

	@property
	def tuple(self):
		return self.getTuple()

	@tuple.setter
	def tuple(self, t):
		self.setTuple(t)

	def getList(self):
		return [self.getSemantics(), self.getDataProperty()]

	def setList(self, l):
		self.setSemantics(l[0])
		self.setDataProperty(l[1])

	@property
	def list(self):
		return self.getList()

	@list.setter
	def list(self, l):
		self.setList(l)

	def getJSONStr(self):
		try:
			s = json.dumps(self.dict)  # dict -> str
			return s
		except TypeError:
			return None

	def setJSONStr(self, s:str):
		try:
			self.dict = json.loads(s)
		except TypeError:
			return False
		else:
			return True

	@property
	def jsonstr(self):
		return self.getJSONStr()

	@jsonstr.setter
	def jsonstr(self, s:str):
		self.setJSONStr(s)

	def getQueryStr(self):
		return self.getJSONStr()

	def setQueryStr(self, s:str):
		self.setJSONStr(s)

	@property
	def querystr(self):
		return self.getQueryStr()

	@querystr.setter
	def querystr(self, s:str):
		self.setQueryStr(s)

	def getPrintString(self, title=None):
		s = ''
		if (title is not None):
			s += '--- {} ---\n'.format(title)
		s += '- semantics\n'
		s += self.semantics.getPrintString()
		s += '- data property\n'
		s += self.dataproperty.getPrintString()
		if (title is not None):
			s += '\n---'
		return s

	@property
	def printstr(self):
		return self.getPrintString()

	@property
	def pstr(self):
		return self.getPrintString()

	def print(self, title=None):
		print(self.getPrintString(title), flush=True)

#-- ion agent

class ion_agent(core):
	_classname = 'ion.ion_agent'

	def __init__(self, sa=None):
		if (sa is None):
			self._semantics = semantics()
			self._datastorage = data_storage()
		elif (isinstance(sa, ion.ion_agent)):
			self._semantics = sa._semantics
			self._datastorage = sa._datastorage
		else:
			__ERROR__

	@classmethod
	def getClassName(cls):
		return ion_agent._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	@property
	def namespace(self):
		return namespace()  # call global function

	@namespace.setter
	def namespace(self, ns):
		namespace(ns)  # call global function

	@property
	def ns(self):
		return self.namespace

	@ns.setter
	def ns(self, ns_):
		self.namespace = ns_

	@property
	def semantics(self):
		return self._semantics

	@semantics.setter
	def semantics(self, s):
		self._semantics = s

	@property
	def sem(self):
		return self.semantics

	@sem.setter
	def sem(self, s_):
		self.semantics = s_

	@property
	def s(self):
		return self.semantics

	@s.setter
	def s(self, s_):
		self.semantics = s_

	@property
	def entity(self):
		return self.s.entity

	@entity.setter
	def entity(self, e):
		self.s.entity = e

	@property
	def ent(self):
		return self.entity

	@ent.setter
	def ent(self, e_):
		self.entity = e_

	@property
	def e(self):
		return self.entity

	@e.setter
	def e(self, e_):
		self.entity = e_

	@property
	def baseentity(self):
		return self.s.baseentity

	@baseentity.setter
	def baseentity(self, be):
		self.s.baseentity = be

	@property
	def bentity(self):
		return self.baseentity

	@bentity.setter
	def bentity(self, be):
		self.baseentity = be

	@property
	def bent(self):
		return self.baseentity

	@bent.setter
	def bent(self, be_):
		self.baseentity = be_

	@property
	def be(self):
		return self.baseentity

	@be.setter
	def be(self, be_):
		self.baseentity = be_

	@property
	def role(self):
		return self.s.role

	@role.setter
	def role(self, r):
		self.s.role = r

	@property
	def r(self):
		return self.role

	@r.setter
	def r(self, r_):
		self.role = r_

	@property
	def spatialidentifier(self):
		return self.s.spatialidentifier

	@spatialidentifier.setter
	def spatialidentifier(self, si):
		self.s.spatialidentifier = si

	@property
	def spatial(self):
		return self.spatialidentifier

	@spatial.setter
	def spatial(self, si_):
		self.spatialidentifier = si_

	@property
	def si(self):
		return self.spatialidentifier

	@si.setter
	def si(self, si_):
		self.spatialidentifier = si_

	@property
	def temporalidentifier(self):
		return self.s.temporalidentifier

	@temporalidentifier.setter
	def temporalidentifier(self, ti):
		self.s.temporalidentifier = ti

	@property
	def temporal(self):
		return self.temporalidentifier

	@temporal.setter
	def temporal(self, ti_):
		self.temporalidentifier = ti_

	@property
	def ti(self):
		return self.temporalidentifier

	@ti.setter
	def ti(self, ti_):
		self.temporalidentifier = ti_

	@property
	def time(self):
		return self.ti.time

	@time.setter
	def time(self, t):
		self.ti.time = t

	@property
	def timeperiod(self):
		return self.ti.timeperiod

	@timeperiod.setter
	def timeperiod(self, tp):
		self.ti.timeperiod = tp

	@property
	def optional(self):
		return self.s.optional

	@optional.setter
	def optional(self, o):
		self.s.optional = o

	@property
	def opt(self):
		return self.optional

	@opt.setter
	def opt(self, o):
		self.optional = o

	@property
	def o(self):
		return self.optional

	@o.setter
	def o(self, o_):
		self.optional = o_

	@property
	def datastorage(self):
		return self._datastorage

	@datastorage.setter
	def datastorage(self, ds):
		self._datastorage= ds

	@property
	def dstorage(self):
		return self.datastorage

	@dstorage.setter
	def dstorage(self, ds_):
		self.datastorage = ds_

	@property
	def ds(self):
		return self.datastorage

	@ds.setter
	def ds(self, ds_):
		self.datastorage = ds_

	@property
	def databody(self):
		return self.datastorage.databody

	@databody.setter
	def databody(self, db):
		self.datastorage.databody = db

	@property
	def dbody(self):
		return self.databody

	@dbody.setter
	def dbody(self, db):
		self.databody = db

	@property
	def db(self):
		return self.databody

	@db.setter
	def db(self, db):
		self.databody = db

	@property
	def data(self):
		return self.databody

	@data.setter
	def data(self, db):
		self.databody = db

	@property
	def d(self):
		return self.data

	@d.setter
	def d(self, ds_):
		self.data = ds_

	@property
	def dataproperty(self):
		return self.datastorage.dataproperty

	@dataproperty.setter
	def dataproperty(self, dp):
		self.datastorage.dataproperty = dp

	@property
	def dproperty(self):
		return self.dataproperty

	@dproperty.setter
	def dproperty(self, dp):
		self.dataproperty = dp

	@property
	def dp(self):
		return self.dataproperty

	@dp.setter
	def dp(self, dp_):
		self.dataproperty = dp_

	@property
	def unit(self):
		return self.dp.unit

	@unit.setter
	def unit(self, u):
		self.dp.unit = u

	@property
	def dataformat(self):
		return self.dataproperty.format

	@dataformat.setter
	def dataformat(self, f):
		self.dataproperty.format = f

	@property
	def format(self):
		return self.dataformat

	@format.setter
	def format(self, f):
		self.dataformat = f

	@property
	def f(self):
		return self.dataformat

	@f.setter
	def f(self, f):
		self.dataformat = f

	@property
	def df(self):
		return self.dataformat

	@df.setter
	def df(self, f):
		self.dataformat = f

	@property
	def dataunit(self):
		return self.dataproperty.unit

	@dataunit.setter
	def dataunit(self, u):
		self.dataproperty.unit = u

	@property
	def unit(self):
		return self.dataunit

	@unit.setter
	def unit(self, u):
		self.dataunit = u

	@property
	def u(self):
		return self.dataunit

	@u.setter
	def u(self, u):
		self.dataunit = u

	@property
	def du(self):
		return self.dataunit

	@du.setter
	def du(self, u):
		self.dataunit = u

	def getQuery(self):
		return query((self.semantics, self.dataproperty))

	def setQuery(self, q):
		self.semantics = q.semantics
		self.dataproperty = q.dataproperty

	@property
	def query(self):
		return self.getQuery()

	@query.setter
	def query(self, q):
		self.setQuery(q)

	@property
	def q(self):
		return self.query

	@q.setter
	def q(self, q_):
		self.query = q_

	def getPrintString(self, title=None):
		str = ''
		if (title is not None):
			str += '--- {} ---\n'.format(title)
		str += '-- semantics\n'
		str += self.semantics.printstr
		str += '-- data property\n'
		str += self.dataproperty.printstr
		str += '\n'
		if (title is not None):
			str += '---\n'
		return str

	@property
	def printstr(self):
		return self.getPrintString()

	def print(self, title=None):
		print(self.getPrintString(title), flush=True)

class ionagent(ion_agent):
	pass

#-- main

if (__name__ == '__main__'):
	_DEBUGLEVEL = 1
	lib_debuglevel(_DEBUGLEVEL)
	debuglevel(_DEBUGLEVEL)

	# namespace

	if (True):
		print('\n-- NAMESPACE --')
		dprint('namespace: \'{}\''.format(namespace()))
		namespace('test_namespace')
		dprint('namespace: \'{}\''.format(namespace()))

	# test for slot class

	if (False):
		print('\n-- SLOT CLASS --')
		sl = slot()
		dprint('classname: \'{}\''.format(sl.getClassName()))
		dprint('classname: \'{}\''.format(sl.classname))
		dprint('slot:      \'{0}\' ({1})'.format(sl, type(sl)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.str, type(sl.str)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.get(), type(sl.get())))

		print('\n--')
		sl = slot('test')
		dprint('classname: \'{}\''.format(sl.classname))
		dprint('slot:      \'{0}\' ({1})'.format(sl, type(sl)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.str, type(sl.str)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.get(), type(sl.get())))

		print('\n--')
		sl = slot('-30')
		dprint('classname: \'{}\''.format(sl.classname))
		dprint('slot:      \'{0}\' ({1})'.format(sl, type(sl)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.str, type(sl.str)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.get(), type(sl.get())))

		print('\n--')
		sl = slot('-3.14')
		dprint('classname: \'{}\''.format(sl.classname))
		dprint('slot:      \'{0}\' ({1})'.format(sl, type(sl)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.str, type(sl.str)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.get(), type(sl.get())))

		print('\n--')
		sl = slot('-3.14e+3')
		dprint('classname: \'{}\''.format(sl.classname))
		dprint('slot:      \'{0}\' ({1})'.format(sl, type(sl)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.str, type(sl.str)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.get(), type(sl.get())))

		if (False):  # ___NOT_IMPLEMENTED
			print('\n-- test')
			sl.set('2.71828')
			dprint('classname: \'{}\''.format(sl.classname))
			dprint('slot:      \'{0}\' ({1})'.format(sl, type(sl)))
			dprint('slot:      \'{0}\' ({1})'.format(sl.str, type(sl.str)))
			dprint('slot:      \'{0}\' ({1})'.format(sl.get(), type(sl.get())))

	# test for semantics class

	if (True):
		print('\n-- SEMANTICS CLASS --')
		sem = semantics({KEY_ENTITY: 'test_entity'})
		dprint('classname: \'{}\''.format(sem.classname))
		sem.print('semantics')

		print('\n--')
		dprint('namespace: \'{}\''.format(sem.namespace))
		sem.namespace = 'test_namespace2'
		dprint('namespace: \'{}\''.format(sem.namespace))
		sem.ns = 'test_namespace3'
		dprint('namespace: \'{}\''.format(sem.ns))

		print('\n--')
		dprint('classname: \'{}\''.format(sem.entity.classname))
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity, type(sem.entity)))
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity.str, type(sem.entity.str)))
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity.get(), type(sem.entity.get())))

		print('\n--')
		dprint('classname: \'{}\''.format(sem.entity.classname))
		sem.entity = slot('test_ent')  # 代入時は必ず slot 形式にキャストしてから代入すること．直接、string データを代入すると、sem.entity が string 型になってしまう。
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity, type(sem.entity)))
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity.str, type(sem.entity.str)))
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity.get(), type(sem.entity.get())))
		if (True):
			dprint('Is equal to \'{0}\': {1}'.format('test_entXXX', sem.entity == 'test_ent/XXX'))
			dprint('Is equal to \'{0}\': {1}'.format('test_ent', sem.entity == 'test_ent'))
			dprint('Is equal to \'{0}\': {1}'.format('test_e', sem.entity == 'test_e'))
			dprint('Is equal to \'{0}\': {1}'.format('dummy', sem.entity == 'dummy'))
			dprint('Is not equal to \'{0}\': {1}'.format('test_ent/XXX', sem.entity != 'test_ent/XXX'))
			dprint('Is not equal to \'{0}\': {1}'.format('test_ent', sem.entity != 'test_ent'))
			dprint('Is not equal to \'{0}\': {1}'.format('test_e', sem.entity != 'test_e'))
			dprint('Is not equal to \'{0}\': {1}'.format('dummy', sem.entity != 'dummy'))
			dprint('Is included in \'{0}\': {1}'.format('test_ent/XXX', sem.entity < 'test_ent/XXX'))
			dprint('Is included in \'{0}\': {1}'.format('test_ent', sem.entity < 'test_ent'))
			dprint('Is included in \'{0}\': {1}'.format('test_e', sem.entity < 'test_e'))
			dprint('Is included in \'{0}\': {1}'.format('dummy', sem.entity < 'dummy'))
			dprint('Is included in \'{0}\': {1}'.format(['dummy'], sem.entity < ['dummy']))
			dprint('Is included in \'{0}\': {1}'.format('[\'test_ent\', \'dummy\']', sem.entity < ['test_ent', 'dummy']))
			dprint('Is equal to or included in \'{0}\': {1}'.format('test_ent/XXX', sem.entity <= 'test_ent/XXX'))
			dprint('Is equal to or included in \'{0}\': {1}'.format('test_ent', sem.entity <= 'test_ent'))
			dprint('Is equal to or included in \'{0}\': {1}'.format('test_e', sem.entity <= 'test_e'))
			dprint('Is equal to or included in \'{0}\': {1}'.format('dummy', sem.entity <= 'dummy'))
			dprint('Does include \'{0}\': {1}'.format('test_ent/XXX', sem.entity > 'test_ent/XXX'))
			dprint('Does include \'{0}\': {1}'.format('test_ent', sem.entity > 'test_ent'))
			dprint('Does include \'{0}\': {1}'.format('test_e', sem.entity > 'test_e'))
			dprint('Does include \'{0}\': {1}'.format('dummy', sem.entity > 'dummy'))
			dprint('Is equal to or does include \'{0}\': {1}'.format('test_ent/XXX', sem.entity >= 'test_ent/XXX'))
			dprint('Is equal to or does include \'{0}\': {1}'.format('test_ent', sem.entity >= 'test_ent'))
			dprint('Is equal to or does include \'{0}\': {1}'.format('test_e', sem.entity >= 'test_e'))
			dprint('Is equal to or does include \'{0}\': {1}'.format('dummy', sem.entity >= 'dummy'))
			dprint('Does start with \'{0}\': {1}'.format('test_ent/XXX', sem.entity.startswith('test_ent/XXX')))
			dprint('Does start with \'{0}\': {1}'.format('test_ent', sem.entity.startswith('test_ent')))
			dprint('Does start with \'{0}\': {1}'.format('test_e', sem.entity.startswith('test_e')))
			dprint('Does start with \'{0}\': {1}'.format('dummy', sem.entity.startswith('dummy')))
			dprint('Does start for \'{0}\': {1}'.format('test_ent/XXX', sem.entity.starts('test_ent/XXX')))
			dprint('Does start for \'{0}\': {1}'.format('test_ent', sem.entity.starts('test_ent')))
			dprint('Does start for \'{0}\': {1}'.format('test_e', sem.entity.starts('test_e')))
			dprint('Does start for \'{0}\': {1}'.format('dummy', sem.entity.starts('dummy')))
			dprint('Does end with \'{0}\': {1}'.format('XXX/test_ent', sem.entity.endswith('XXX/test_ent')))
			dprint('Does end with \'{0}\': {1}'.format('test_ent', sem.entity.endswith('test_ent')))
			dprint('Does end with \'{0}\': {1}'.format('test_e', sem.entity.endswith('test_e')))
			dprint('Does end with \'{0}\': {1}'.format('dummy', sem.entity.endswith('dummy')))
			dprint('Does end \'{0}\': {1}'.format('XXX/test_ent', sem.entity.ends('XXX/test_ent')))
			dprint('Does end \'{0}\': {1}'.format('test_ent', sem.entity.ends('test_ent')))
			dprint('Does end \'{0}\': {1}'.format('test_e', sem.entity.ends('test_e')))
			dprint('Does end \'{0}\': {1}'.format('dummy', sem.entity.ends('dummy')))

		print('\n--')
		sem.entity = slot(STR_ANY)  # 代入時は必ず slot 形式にキャストしてから代入すること．直接、string データを代入すると、sem.entity が string 型になってしまう。
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity, type(sem.entity)))
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity.str, type(sem.entity.str)))
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity.get(), type(sem.entity.get())))
		if (True):
			dprint('Is equal to \'{0}\': {1}'.format('test_entXXX', sem.entity == 'test_ent/XXX'))
			dprint('Is equal to \'{0}\': {1}'.format('test_ent', sem.entity == 'test_ent'))
			dprint('Is equal to \'{0}\': {1}'.format('test_e', sem.entity == 'test_e'))
			dprint('Is equal to \'{0}\': {1}'.format('dummy', sem.entity == 'dummy'))
			dprint('Is not equal to \'{0}\': {1}'.format('test_ent/XXX', sem.entity != 'test_ent/XXX'))
			dprint('Is not equal to \'{0}\': {1}'.format('test_ent', sem.entity != 'test_ent'))
			dprint('Is not equal to \'{0}\': {1}'.format('test_e', sem.entity != 'test_e'))
			dprint('Is not equal to \'{0}\': {1}'.format('dummy', sem.entity != 'dummy'))
			dprint('Is included in \'{0}\': {1}'.format('test_ent/XXX', sem.entity < 'test_ent/XXX'))
			dprint('Is included in \'{0}\': {1}'.format('test_ent', sem.entity < 'test_ent'))
			dprint('Is included in \'{0}\': {1}'.format('test_e', sem.entity < 'test_e'))
			dprint('Is included in \'{0}\': {1}'.format('dummy', sem.entity < 'dummy'))
			dprint('Is included in \'{0}\': {1}'.format(['dummy'], sem.entity < ['dummy']))
			dprint('Is included in \'{0}\': {1}'.format('[\'test_ent\', \'dummy\']', sem.entity < ['test_ent', 'dummy']))
			dprint('Is equal to or included in \'{0}\': {1}'.format('test_ent/XXX', sem.entity <= 'test_ent/XXX'))
			dprint('Is equal to or included in \'{0}\': {1}'.format('test_ent', sem.entity <= 'test_ent'))
			dprint('Is equal to or included in \'{0}\': {1}'.format('test_e', sem.entity <= 'test_e'))
			dprint('Is equal to or included in \'{0}\': {1}'.format('dummy', sem.entity <= 'dummy'))
			dprint('Does include \'{0}\': {1}'.format('test_ent/XXX', sem.entity > 'test_ent/XXX'))
			dprint('Does include \'{0}\': {1}'.format('test_ent', sem.entity > 'test_ent'))
			dprint('Does include \'{0}\': {1}'.format('test_e', sem.entity > 'test_e'))
			dprint('Does include \'{0}\': {1}'.format('dummy', sem.entity > 'dummy'))
			dprint('Is equal to or does include \'{0}\': {1}'.format('test_ent/XXX', sem.entity >= 'test_ent/XXX'))
			dprint('Is equal to or does include \'{0}\': {1}'.format('test_ent', sem.entity >= 'test_ent'))
			dprint('Is equal to or does include \'{0}\': {1}'.format('test_e', sem.entity >= 'test_e'))
			dprint('Is equal to or does include \'{0}\': {1}'.format('dummy', sem.entity >= 'dummy'))
			dprint('Does start with \'{0}\': {1}'.format('test_ent/XXX', sem.entity.startswith('test_ent/XXX')))
			dprint('Does start with \'{0}\': {1}'.format('test_ent', sem.entity.startswith('test_ent')))
			dprint('Does start with \'{0}\': {1}'.format('test_e', sem.entity.startswith('test_e')))
			dprint('Does start with \'{0}\': {1}'.format('dummy', sem.entity.startswith('dummy')))
			dprint('Does start for \'{0}\': {1}'.format('test_ent/XXX', sem.entity.starts('test_ent/XXX')))
			dprint('Does start for \'{0}\': {1}'.format('test_ent', sem.entity.starts('test_ent')))
			dprint('Does start for \'{0}\': {1}'.format('test_e', sem.entity.starts('test_e')))
			dprint('Does start for \'{0}\': {1}'.format('dummy', sem.entity.starts('dummy')))
			dprint('Does end with \'{0}\': {1}'.format('XXX/test_ent', sem.entity.endswith('XXX/test_ent')))
			dprint('Does end with \'{0}\': {1}'.format('test_ent', sem.entity.endswith('test_ent')))
			dprint('Does end with \'{0}\': {1}'.format('test_e', sem.entity.endswith('test_e')))
			dprint('Does end with \'{0}\': {1}'.format('dummy', sem.entity.endswith('dummy')))
			dprint('Does end \'{0}\': {1}'.format('XXX/test_ent', sem.entity.ends('XXX/test_ent')))
			dprint('Does end \'{0}\': {1}'.format('test_ent', sem.entity.ends('test_ent')))
			dprint('Does end \'{0}\': {1}'.format('test_e', sem.entity.ends('test_e')))
			dprint('Does end \'{0}\': {1}'.format('dummy', sem.entity.ends('dummy')))

		print('\n--')
		dprint('classname: \'{}\''.format(sem.bentity.classname))
		dprint('bentity:   \'{0}\' ({1})'.format(sem.bentity, type(sem.bentity)))
		dprint('bentity:   \'{0}\' ({1})'.format(sem.bentity.str, type(sem.bentity.str)))
		dprint('bentity:   \'{0}\' ({1})'.format(sem.bentity.get(), type(sem.bentity.get())))

		print('\n--')
		dprint('classname: \'{}\''.format(sem.role.classname))
		dprint('role:      \'{0}\' ({1})'.format(sem.role, type(sem.role)))
		dprint('role:      \'{0}\' ({1})'.format(sem.role.str, type(sem.role.str)))
		dprint('role:      \'{0}\' ({1})'.format(sem.role.get(), type(sem.role.get())))

		print('\n--')
		dprint('classname: \'{}\''.format(sem.si.classname))
		dprint('si:      \'{0}\' ({1})'.format(sem.si, type(sem.si)))
		dprint('si:      \'{0}\' ({1})'.format(sem.si.printstr, type(sem.si.printstr)))
		dprint('si:      \'{0}\' ({1})'.format(sem.si.pstr, type(sem.si.pstr)))
		if (True):
			sem.si.print()
			sem.si.print('si')
		if (True):
			sem.si['format'] = 'tmdu/bmi/nakajima'
			sem.si['unit'] = 'radian'
			sem.si['time'] = {'time': '2023/08/22,21:12:27', 'period': '60', 'period_unit': 'seconds'}
			pprint.pprint(sem.si)
			sem.si.save('test.json')
			sem.si.load('test.json')
			sem.si.print('\'test.json\'')
			print('-- json.dumps() --')
			print(json.dumps(sem.si))
			print('--', flush=True)
			print('-- pprint.pprint() --')
			pprint.pprint(sem.si, indent=1, width=1)
			print('--', flush=True)

		print('\n--')
		dprint('classname: \'{}\''.format(sem.ti.classname))
		dprint('ti:      \'{0}\' ({1})'.format(sem.ti, type(sem.ti)))
		dprint('ti:      \'{0}\' ({1})'.format(sem.ti.printstr, type(sem.ti.printstr)))
		dprint('ti:      \'{0}\' ({1})'.format(sem.ti.pstr, type(sem.ti.pstr)))

	# test for query class

	if (True):
		print('\n-- QUERY CLASS --')
		q = query()
		dprint('classname: \'{}\''.format(q.classname))

		# CLASS <-> JSON test

		print('\n--')

	# test for ion semantics agent class

	if (True):
		print('\n-- iON SEMANTICS AGENT CLASS --')
		agent = semantics_agent()
		dprint('classname: \'{}\''.format(agent.classname))
