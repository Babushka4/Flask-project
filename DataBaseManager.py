class BDManager():
	def __init__(self, current_app):
		self.app = current_app
	
	def connect_db(self):
		conn = sqlite3.connect(self.app.config["DATABASE"])
		conn.row_factory = sqlite3.Row
		return conn
		
	def create_db(self):
		db = connect_db()
		with self.app.open_resource('sql_db.sql', mode='r') as f:
			db.cursor().executescript(f.read())
			db.commit()
			db.close()
			
	def get_db(self):
		if not hasattr(g, "link_db"):
			g.link_db = connect_db()
		return g.link_db
		
		

class FDataBase:
	def __init__(self,db):
		self.__db = db
		self.__cur = db.cursor()
		
		
		
	def getUsers(self, filter = None):
		# говно говна
		
		sql = "SELECT * FROM User"
		
		if filter:
			# if filter fields was given, make more complex request 
			
			filter_fields = list(filter.keys())
			
			sql += " WHERE {0} == '{1}'".format(filter_fields[0], filter[filter_fields[0]])
			
			for field in filter_fields[1:]:
				sql += " AND {0} == '{1}' ".format(field, filter[field])
			print(sql)
			
		# request execution
		self.__cur.execute(sql)
		res = self.__cur.fetchall(),
		return res if res else False
	
	
	
	def searchUserBy(self, field, value):
		for [user] in self.getUsers():
			if user[field] == value:
				return True
		return False
	
	
	
	def createObject(self, values):
		sql = "INSERT INTO User(login, password, email, name) VALUES(?,?,?,?)"
		self.__cur.execute(sql, values)
		self.__db.commit()
		
		
		
	def getData(self, table, filter = None):
		sql = "SELECT * FROM " + table
		
		if filter:
			# if filter fields was given, make more complex request 
			filter_fields = list(filter.keys())
			sql += " WHERE {0} == '{1}' ".format(filter_fields[0], filter[filter_fields[0]])
			
			for field in filter_fields[1:]:
				sql += "AND {0} == '{1}' ".format(field, filter[field])
			
		# request execution
		self.__cur.execute(sql)
		res = self.__cur.fetchall()
		# return res[0] if res else False
		return res if res else False
		
		
		
	def getById(self, table, id):
		sql = "SELECT * FROM " + table
		sql += " WHERE id == {0}".format(id)
		
		# request execution
		self.__cur.execute(sql)
		res = self.__cur.fetchall()
		# return res[0] if res else False
		return res if res else False