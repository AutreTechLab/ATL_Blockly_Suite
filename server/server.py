#!/usr/bin/env python3

try:
	import tornado.ioloop
	import tornado.web
	import tornado.websocket
	import tornado.template
	from tornado import locks, gen
	from tornado.platform.asyncio import AsyncIOMainLoop
	from tornado import gen
	from tornado.options import options, define
	from tornado.queues import Queue
except ImportError:
	sys.exit("Cannot import Tornado: Do `pip3 install --user tornado` to install")

import asyncio

import signal
import argparse
import os
import json
import re
from CodeExecutor import CodeExecutor
from cozmobot import CozmoBot
from subprocess import Popen

cozmoBlockly = None
nodejs = None

def signal_handler(signal, frame):
	global cozmoBlockly, nodejs

	print('Got ' + str(signal) + ' signal. Shutting down...')
	cozmoBlockly.stop()
	if nodejs != None:
		nodejs.terminate()
		nodejs.wait()
	exit(0)

class CozmoBlockly(tornado.web.Application):

	class WSBlocksSubHandler(tornado.websocket.WebSocketHandler):
		def open(self):
			print('[Server] WSBlocksSub client connected')
			self.application._blocks = self

		def on_close(self):
			print('[Server] WSBlocksSub client disconnected')

		def on_message(self, message):
			print('[Server] WSBlocksSub client message: ' + message)
			# echo message back to client
			self.write_message(message)

	class WSBlocksPubHandler(tornado.websocket.WebSocketHandler):
		def open(self):
			print('[Server]  WSBlocksSPub Handler client connected')

		def on_message(self, message):
			try:
				if self.application._blocks:
					self.application._blocks.write_message(message)
			except Exception:
				pass

		def on_close(self):
			print('[Server]  WSConsolePub client disconnected')

	class WSConsoleSubHandler(tornado.websocket.WebSocketHandler):
		def open(self):
			print('[Server] WSConsoleSub client connected')
			self.application._console = self

		def on_close(self):
			print('[Server] WSConsoleSub client disconnected')

		def on_message(self, message):
			print('[Server] WSConsoleSub client message: ' + message)
			# echo message back to client
			self.write_message(message)

	class WSConsolePubHandler(tornado.websocket.WebSocketHandler):
		def open(self):
			print('[Server]  WSConsolePub client connected')

		def on_message(self, message):
			try:
				if self.application._console:
					self.application._console.write_message(message)
			except Exception:
				pass

		def on_close(self):
			print('[Server]  WSConsolePub client disconnected')

	class WS3dSubHandler(tornado.websocket.WebSocketHandler):
		def open(self):
			print('[Server] 3dSub client connected')
			self.application._ws3d = self

		def on_close(self):
			print('[Server] 3dSub client disconnected')

		def on_message(self, message):
			print('[Server] 3dSub client message: ' + message)
			# echo message back to client
			self.write_message(message)

	class WS3dPubHandler(tornado.websocket.WebSocketHandler):
		def open(self):
			print('[Server] 3dPub client connected')

		def on_message(self, message):
			try:
				if self.application._ws3d:
					self.application._ws3d.write_message(message)
			except Exception:
				pass

		def on_close(self):
			print('[Server] 3dPub client disconnected')

	class WSCameraSubHandler(tornado.websocket.WebSocketHandler):
		def open(self):
			print('[Server] CameraSub client connected')
			self.application._wsCamera = self

		def on_close(self):
			print('[Server] CameraSub client disconnected')

	class WSCameraPubHandler(tornado.websocket.WebSocketHandler):
		def open(self):
			print('[Server] CameraPub client connected')

		def on_message(self, message):
			try:
				if self.application._wsCamera:
					self.application._wsCamera.write_message(message, binary=True)
			except Exception:
				pass

		def on_close(self):
			print('[Server] CameraPub client disconnected')

	class RobotSubmitHandler(tornado.web.RequestHandler):
		@gen.coroutine
		def post(self):
			data = self.request.body
			try:
				code = str(data, 'utf-8')
				print('Received code: ')
				print(code)
				with (yield self.application._lock.acquire()):
					self.application._executor.start(code)
				self.write('OK')
			except Exception as e:
				err = str(e)
				raise tornado.web.HTTPError(500, err, reason=err)

	class RobotTerminateHandler(tornado.web.RequestHandler):
		@gen.coroutine
		def post(self):
			print('Terminating code')
			with (yield self.application._lock.acquire()):
				self.application._executor.stop()
			self.write('OK')

	class NoCacheStaticFileHandler(tornado.web.StaticFileHandler):
		def set_extra_headers(self, path):
			# Disable cache
			self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

	class SavesHandler(tornado.web.RequestHandler):
		def get(self, folder, file):
			file = file.strip('/')
			if len(file) == 0:
				# Send folder index
				storedFiles = []
				removeXmlRegex = re.compile('\.xml$')
				for filename in os.listdir(folder):
					relativePath = os.path.join(folder, filename)
					if os.path.isfile(relativePath) and filename.endswith('.xml'):
						storedFiles.append(removeXmlRegex.sub('', filename))
				print("Returning files list: " + str(storedFiles))
				self.write(json.dumps(storedFiles).encode('utf-8'))
				self.set_header('Content-type','application/json')
			else:
				# Send only one file
				f = open(os.path.join(folder, file + '.xml'), 'r')
				data = f.read()
				f.close()
				self.write(data)

		def put(self, folder, file):
			file = file.strip('/')
			print('[Server] SavesHandler: Saving ' + file)
			data = self.request.body
			f = open(os.path.join(folder, file + '.xml'), 'wb')
			f.write(data)
			f.close()

	class ATLHomeHandler(tornado.web.RequestHandler):
		def initialize(self, args):
			self.args = args

		def get(self, path):
			path = '../atl-blockly/' + path

			self.render(path + 'index.html')

	class HomeHandler(tornado.web.RequestHandler):
		def initialize(self, args):
			self.args = args

		def get(self, path):
			cozmo_blockly_path = '../cozmo-blockly/' + path
			thymio_blockly_path = '../thymio-blockly/' + path

			loader = tornado.template.Loader(cozmo_blockly_path, whitespace='all')
			file = 'includes.template'
			if self.args.dev:
				file = 'includes_debug.template'
			t = loader.load(file)
			includes = t.generate()

			# Modularisation of the toolbox depending on the available robots
			loader = tornado.template.Loader(cozmo_blockly_path, whitespace='all')
			file = 'cozmo_blocks.xml'
			t = loader.load(file)
			cozmo_blocks = t.generate()

			loader = tornado.template.Loader(thymio_blockly_path, whitespace='all')
			file = 'thymio_blocks.xml'
			t = loader.load(file)
			thymio_blocks = t.generate()

			if self.args.nonsecure:
				nonsec = 'true'
			else:
				nonsec = 'false'

			print('[Server] HomeHandler: Loading ' + cozmo_blockly_path + ' and ' + thymio_blockly_path)

			self.render(cozmo_blockly_path + 'index.html', includes=includes, cozmo_blocks=cozmo_blocks, thymio_blocks=thymio_blocks, name=self.args.name, nonsecure=nonsec)


	def stop(self):
		# with (yield self._lock.acquire()):
		# 	self._executor.stop()
		# 	tornado.ioloop.IOLoop.instance().stop()
		self._executor.stop()
		tornado.ioloop.IOLoop.instance().stop()

	def start(args):
		global cozmoBlockly, nodejs

		app = CozmoBlockly([
			(r'/()', CozmoBlockly.ATLHomeHandler, dict(args=args)),
			(r'/EN/()', CozmoBlockly.HomeHandler , dict(args=args)),
			(r'/FR/()', CozmoBlockly.HomeHandler , dict(args=args)),
			(r'/EN/(.+)', tornado.web.StaticFileHandler if not args.dev else CozmoBlockly.NoCacheStaticFileHandler, dict(path='../cozmo-blockly')),
			(r'/FR/(.+)', tornado.web.StaticFileHandler if not args.dev else CozmoBlockly.NoCacheStaticFileHandler, dict(path='../cozmo-blockly')),
			(r'/static/(.*)', tornado.web.StaticFileHandler if not args.dev else CozmoBlockly.NoCacheStaticFileHandler,dict(path='../gallery')),
			(r'/blockly/(.*)', tornado.web.StaticFileHandler if not args.dev else CozmoBlockly.NoCacheStaticFileHandler, dict(path='../blockly')),
			(r'/thymio-blockly/(.*)', tornado.web.StaticFileHandler if not args.dev else CozmoBlockly.NoCacheStaticFileHandler,dict(path='../thymio-blockly')),
			(r'/atl-blockly/(.*)',tornado.web.StaticFileHandler if not args.dev else CozmoBlockly.NoCacheStaticFileHandler,dict(path='../atl-blockly')),
			(r'/closure-library/(.*)', tornado.web.StaticFileHandler if not args.dev else CozmoBlockly.NoCacheStaticFileHandler, dict(path='../closure-library')),
			(r'/(saves)/(.*)', CozmoBlockly.SavesHandler),
			(r'/robot/submit', CozmoBlockly.RobotSubmitHandler),
			(r'/robot/terminate', CozmoBlockly.RobotTerminateHandler),
			(r'/camSub', CozmoBlockly.WSCameraSubHandler),
			(r'/camPub', CozmoBlockly.WSCameraPubHandler),
			(r'/WsSub', CozmoBlockly.WS3dSubHandler),
			(r'/WsPub', CozmoBlockly.WS3dPubHandler),
			(r'/blocksSub', CozmoBlockly.WSBlocksSubHandler),
			(r'/blocksPub', CozmoBlockly.WSBlocksPubHandler),
			(r'/consoleSub', CozmoBlockly.WSConsoleSubHandler),
			(r'/consolePub', CozmoBlockly.WSConsolePubHandler),
		])
		cozmoBlockly = app


		if not args.nonsecure:
			try:
				nodejs = Popen(['node', '../nodejs/headless.js'])
			except FileNotFoundError as e:
				print("node.js wasn't found in your system.")
				print("Secure mode (default) requires node.js. Please install node.js and follow README instructions.")
				return

		print('[Server] Starting server...')

		tornado.platform.asyncio.AsyncIOMainLoop().install()
		if args.dev:
			print('[Server] Running in debug mode')
		app.listen(9090)

		app._executor = CodeExecutor(args.nonsecure, args.nocozmo, args.aruco)
		app._lock = locks.Lock()
		app._wsCamera = None
		app._ws3d = None

		app._ioloop = tornado.ioloop.IOLoop.current()
		print('[Server] Started, awaiting requests...')
		print('===========================================================================')
		app._ioloop.start()
		print('[Server] Server stopped')


def main():
	# listen for SIGINT
	signal.signal(signal.SIGINT, signal_handler)
	signal.signal(signal.SIGTERM, signal_handler)

	parser = argparse.ArgumentParser(description='Cozmo Blocks')
	parser.add_argument('-n', '--name', default='',
	                    help='default file name to load/save')
	parser.add_argument('-d', '--dev', action="store_true",
						help='enable development mode (disables caching)')
	parser.add_argument('--nonsecure', action="store_true",
						help="run server in non-secure mode, which doesn't require nodejs but python code is accepted from the network for execution")
	parser.add_argument('--nocozmo', action="store_true",
						help="mock Cozmo")
	parser.add_argument('--aruco', action="store_true",
						help="enable Aruco markers detection")
	args = parser.parse_args()

	print('===========================================================================')

	CozmoBlockly.start(args)

if __name__ == '__main__':
	main()
