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
#from couchbase.bucket import Bucket
import tornado.platform.twisted
tornado.platform.twisted.install()
from twisted.internet import reactor

from txcouchbase.bucket import Bucket

from couchbase.n1ql import N1QLQuery, N1QLError
from pprint import pprint

server = "52.27.232.218"
bucketname = "zips"

Connection = "couchbase://" + server + "/" + bucketname

print Connection
p0 = time.time()

i=0

bkt = Bucket(Connection)

p1 = time.time()
print p1-p0


class IndexHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous	
	def get(self):
		print "entered"
		query = "SELECT * FROM `zips` where pincode= '632014'"
		q = N1QLQuery(query)
		#self.bkt = bkt
		t0 = time.time()
		#res = bkt.n1qlQueryAll(q)
		res = bkt.n1qlQueryAll(q)
		res.addCallback(self.on_ok)
		#reactor.run()
		t1 = time.time()
		print t1-t0
		self.write("Hello World")
		
	def on_ok(self,response):
		for each in response._BatchedRowMixin__rows:
			print each

		self.finish()

handlers = [
    (r'/',IndexHandler),
]

if __name__ == "__main__":
    parse_command_line()
    # template path should be given here only unlike handlers
    app = tornado.web.Application(handlers, template_path=os.path.join(os.path.dirname(__file__), "templates"),
                                  static_path=os.path.join(os.path.dirname(__file__), "static"), cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=", debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8889, address='0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()

