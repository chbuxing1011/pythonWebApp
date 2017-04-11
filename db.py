#!/usr/bin/python
# -*- coding: utf-8 -*-

# 导入MySQL驱动:
import MySQLdb

# 数据库引擎对象:
class _Engine(object):
	def __init__(self, connect):
		self._connect = connect
	def connect(self):
		return self._connect()

engine = None

# 持有数据库连接的上下文对象:
class _DbCtx(threading.local):
	def __init__(self):
		self.connection = None
		self.transactions = 0

	def is_init(self):
		return not self.connection is None

	def init(self):
		self.connection = _LasyConnection()
		self.transactions = 0

	def cleanup(self):
		self.connection.cleanup()
		self.connection = None

	def cursor(self):
		return self.connection.cursor()

_db_ctx = _DbCtx()
	
class _ConnectionCtx(object):
	def __enter__(self):
		global _db_ctx
		self.should_cleanup = False
		if not _db_ctx.is_init():
			_db_ctx.init()
			self.should_cleanup = True
		return self

	def __exit__(self, exctype, excvalue, traceback):
		global _db_ctx
		if self.should_cleanup:
			_db_ctx.cleanup()

def connection():
	return _ConnectionCtx()
	
	
@with_connection
def select(sql, *args):
	pass

@with_connection
def update(sql, *args):
	pass
	
class _TransactionCtx(object):
	def __enter__(self):
		global _db_ctx
		self.should_close_conn = False
		if not _db_ctx.is_init():
			_db_ctx.init()
			self.should_close_conn = True
		_db_ctx.transactions = _db_ctx.transactions + 1
		return self

	def __exit__(self, exctype, excvalue, traceback):
		global _db_ctx
		_db_ctx.transactions = _db_ctx.transactions - 1
		try:
			if _db_ctx.transactions==0:
				if exctype is None:
					self.commit()
				else:
					self.rollback()
		finally:
			if self.should_close_conn:
				_db_ctx.cleanup()

	def commit(self):
		global _db_ctx
		try:
			_db_ctx.connection.commit()
		except:
			_db_ctx.connection.rollback()
			raise

	def rollback(self):
		global _db_ctx
		_db_ctx.connection.rollback()
		
@with_transaction
def do_in_transaction():
	pass
	

def baseMethod():
	#建立和数据库系统的连接
	conn= MySQLdb.connect(
		host='localhost',
		port = 3306,
		user='root',
		passwd='123456',
		db ='test',
		)
	cur = conn.cursor()
	#执行SQL,创建一个数据库.
	#cursor.execute("""create database if not exists python""")

	#创建数据表
	#cur.execute("create table student(id int ,name varchar(20),class varchar(30),age varchar(10))")

	#插入一条数据
	#cur.execute("insert into student values('2','Tom','3 year 2 class','9')")


	#修改查询条件的数据
	#cur.execute("update student set class='3 year 1 class' where name = 'Tom'")

	#删除查询条件的数据
	#cur.execute("delete from student where age='9'")

	cur.close()
	conn.commit()
	conn.close()
#插入单条数据
def insertOne():
	conn= MySQLdb.connect(
	host='localhost',
	port = 3306,
	user='root',
	passwd='123456',
	db ='test',
	)
	cur = conn.cursor()

	#插入一条数据
	sqli="insert into student values(%s,%s,%s,%s)"
	cur.execute(sqli,('3','Huhu','2 year 1 class','7'))

	cur.close()
	conn.commit()
	conn.close()
	
#插入多条数据
def insertManay():
	conn= MySQLdb.connect(
		host='localhost',
		port = 3306,
		user='root',
		passwd='123456',
		db ='test',
		)
	cur = conn.cursor()

	#一次插入多条记录
	sqli="insert into student values(%s,%s,%s,%s)"
	cur.executemany(sqli,[
		('3','Tom','1 year 1 class','6'),
		('3','Jack','2 year 1 class','7'),
		('3','Yaheng','2 year 2 class','7'),
		])

	cur.close()
	conn.commit()
	conn.close()
	
#insertOne()
#insertManay()

def queryAllData():
	conn= MySQLdb.connect(
	host='localhost',
	port = 3306,
	user='root',
	passwd='123456',
	db ='test',
	)
	cur = conn.cursor()

	#获得表中有多少条数据
	aa=cur.execute("select * from student")
	print aa

	#打印表中的多少数据
	info = cur.fetchmany(aa)
	for ii in info:
	    print ii
	cur.close()
	conn.commit()
	conn.close()
	
#查询所有
def queryAll():
	conn= MySQLdb.connect(
	host='localhost',
	port = 3306,
	user='root',
	passwd='123456',
	db ='test',
	)
	cur = conn.cursor()

	cur.execute("select * from student")
	res=cur.fetchall()
	for row in res:
		print('userid=%s,userna=%s,desc=%s,age=%s' %row)
	cur.close()
	conn.commit()
	conn.close()
#条件查询
def queryDataByOptions(name,desc,age):
	conn= MySQLdb.connect(
	host='localhost',
	port = 3306,
	user='root',
	passwd='123456',
	db ='test',
	)
	cur = conn.cursor()

	#获得表中有多少条数据
	sqli="select * from student where name=%s" %name
	aa=cur.execute(sqli)
	print aa

	#打印表中的多少数据
	info = cur.fetchmany(aa)
	for ii in info:
	    print ii
	cur.close()
	conn.commit()
	conn.close()
#条件更新
def updateDataByOptions(name,age):
	conn= MySQLdb.connect(
	host='localhost',
	port = 3306,
	user='root',
	passwd='123456',
	db ='test',
	)
	cur = conn.cursor()

	#获得表中有多少条数据
	sqli="""update student set age=%d where name='%s'""" %(age,name)
	print sqli
	aa=cur.execute(sqli)
	cur.close()
	conn.commit()
	conn.close()

#queryDataByOptions('Tom','','9')
#updateDataByOptions('Tom',9)
#queryAll()
#queryData()