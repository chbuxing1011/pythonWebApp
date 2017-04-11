#!/usr/bin/python
# -*- coding: utf-8 -*-

class Model(dict):
	__metaclass__ = ModelMetaclass

	def __init__(self, **kw):
		super(Model, self).__init__(**kw)

	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

	def __setattr__(self, key, value):
		self[key] = value
	
	@classmethod
    def get(cls, pk):
	d = db.select_one('select * from %s where %s=?' % (cls.__table__, cls.__primary_key__.name), pk)
	return cls(**d) if d else None
	
	def insert(self):
		params = {}
		for k, v in self.__mappings__.iteritems():
		    params[v.name] = getattr(self, k)
		db.insert(self.__table__, **params)
		return self
	
	def find_first(self):
		pass
	def find_all(self):
		pass
	def find_by(self):
		pass
	def count_all(self):
		pass
	def count_by(self):
		pass
	def update(self):
		pass
	def delete(self):
		pass
	
	
		
class ModelMetaclass(type):
	    def __new__(cls, name, bases, attrs):
		mapping = ... # 读取cls的Field字段
		primary_key = ... # 查找primary_key字段
		__table__ = cls.__talbe__ # 读取cls的__table__字段
		# 给cls增加一些字段：
		attrs['__mapping__'] = mapping
		attrs['__primary_key__'] = __primary_key__
		attrs['__table__'] = __table__
		return type.__new__(cls, name, bases, attrs)

