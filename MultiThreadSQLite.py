from threading import Thread
try:
	from queue import Queue
except:
	from Queue import Queue
import apsw

class MultiThreadSQLite(Thread):
	def __init__(self, db):
		super(MultiThreadSQLite, self).__init__()

		self.db = db
		self.reqs = Queue()
		self.start()

	def run(self):
		cnx = apsw.Connection(self.db)
		cursor = cnx.cursor()
		while True:
			req, arg, res = self.reqs.get()
			if req == '--close--':
				break

			cursor.execute(req, arg)
			if res:
				for rec in cursor:
					res.put(rec)
				res.put('--no more--')
		cnx.close()

	def execute(self, req, arg=None, res=None):
		self.reqs.put((req, arg or tuple(), res))

	def select(self, req, arg=None):
		res = Queue()
		self.execute(req, arg, res)

		while True:
			rec = res.get()
			if rec == '--no more--':
				break

			yield rec

	def close(self):
		self.execute('--close--')