import time

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
from tornado import gen

define('port', default=8000, help='run on the given port', type=int)


class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		greeting = self.get_argument('greeting', 'Hello')
		self.write(greeting + ', friendly user!')

	def write_error(self, status_code, **kwargs):
		self.write('Gosh darnit, user! You caused a %d error.' % status_code)


class SleepHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	@gen.coroutine
	def get(self, *args, **kwargs):
		yield tornado.gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time() + 5)
		self.write('over')
		self.finish()


if __name__ == '__main__':
	tornado.options.parse_command_line()
	app = tornado.web.Application(
		handlers=[
			(r'/', IndexHandler),
			(r'/sleep', SleepHandler),
		]
	)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()