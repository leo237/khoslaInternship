import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
import tornado.websocket
import tornado.httpclient
from tornado import gen
import os.path
from tornado.options import define, options, parse_command_line
import time
from gcouchbase.bucket import Bucket
from couchbase.n1ql import N1QLQuery, N1QLError
from pprint import pprint
from gevent import monkey; monkey.patch_all()
import gevent
import Queue

#-------------------------Database Configuration-------------
server = "52.27.232.218"
bucketname = "zips"


#-----------------------Connection Object--------------------
class DatabaseConnection:
	def __init__(self, conn):
		self.connection = conn
		self.time = time.time()



Connection = "couchbase://" + server + "/" + bucketname
print Connection

p0 = time.time()

#-------------------------Creating Connection Pool-----------
bkt = set()

i=0
while(i<10):
	bucket = DatabaseConnection(Bucket(Connection))
	bkt.add(bucket)
	i+=1

p1 = time.time()

#------------------------------------------------------------
print p1-p0

inUse = list()


class IndexHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		def async_task():
			print "entered"
			query = "SELECT * FROM `zips` where pincode= '632014'"
			q = N1QLQuery(query)
			#self.bkt = bkt


#-------------SELECT DATABASE BUCKET-----------------------------------
			print "Bucket size ", len(bkt)
			print "InUse size", len(inUse)
			print bkt
			print inUse
			t0 = time.time()
			while(1):
				try:
					myBucket = bkt.pop()
					myBucket.time = time.time()
					inUse.append(myBucket)
					break
				except:
					try:
						tempBucket = inUse.pop(0)
						if (time.time()-tempBucket.time) > 3:
							bkt.add(tempBucket)
						else:
							inUse.append(tempBucket)
					except:
						pass

			res = myBucket.connection.n1ql_query(q)

			for each in res:
				print each
			t1 = time.time()
			print t1-t0

			self.write("Hello World")
			bkt.add(myBucket)
			inUse.remove(myBucket)
			print "Currently ", len(bkt), " buckets!"
			self.finish()
		gevent.spawn(async_task)
		#async_task()
handlers = [
    (r'/',IndexHandler),
]

if __name__ == "__main__":
    parse_command_line()
    # template path should be given here only unlike handlers
    app = tornado.web.Application(handlers, template_path=os.path.join(os.path.dirname(__file__), "templates"),
                                  static_path=os.path.join(os.path.dirname(__file__), "static"), cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=", debug=True)
    http_server = tornado.httpserver.HTTPServer(app,xheaders=True)
    http_server.listen(8891, address='0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()


