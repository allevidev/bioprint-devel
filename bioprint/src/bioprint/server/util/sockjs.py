# coding=utf-8
from __future__ import absolute_import

__author__ = "Gina Häußge <osd@foosel.net>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2014 The bioprint Project - Released under terms of the AGPLv3 License"

import logging
import threading
import sockjs.tornado
import time

import bioprint.timelapse
import bioprint.server
from bioprint.events import Events

import bioprint.printer

import hid
import math
import time
import threading
import requests

class PrinterStateConnection(sockjs.tornado.SockJSConnection, bioprint.printer.PrinterCallback):
	def __init__(self, printer, fileManager, analysisQueue, userManager, eventManager, pluginManager, session):
		sockjs.tornado.SockJSConnection.__init__(self, session)

		self._logger = logging.getLogger(__name__)

		self._temperatureBacklog = []
		self._temperatureBacklogMutex = threading.Lock()
		self._logBacklog = []
		self._logBacklogMutex = threading.Lock()
		self._messageBacklog = []
		self._messageBacklogMutex = threading.Lock()

		self._printer = printer
		self._fileManager = fileManager
		self._analysisQueue = analysisQueue
		self._userManager = userManager
		self._eventManager = eventManager
		self._pluginManager = pluginManager

		self._remoteAddress = None
	
	def initializeDevice(self):
		print(threading.currentThread().getName(), 'Starting')
		self.device = hid.device()
		self.bioprintBaseUrl = ''.join(['http://', '0.0.0.0', ':', '8090', '/api/']) #	This instance's url
		self.movingThread = threading.Thread(name='Moving thread', target=self.movingThread)
		self.movingThread.daemon = True
		self.isMoving = False
		self.isExtruding = False
		self.movingThread.start()
		try:
			for d in hid.enumerate():
					if(d['product_id'] == 39):
						self.device.open_path(d['path'])
						break
			print(self.device)
			self.position = {
				'X': 0,
				'Y': 0,
				'Z': 50,
			}
			while self.collectInput:
				self.read()
				time.sleep(0.05)
		except IOError as ex:
			print(ex)
		print(threading.currentThread().getName(), 'Exiting')

	def restrainPositions(self):
		def restrict(number, max_n, min_n):
			return min(max(number, min_n), max_n)
		self.position['X'] = restrict(self.position['X'], 150, 0)
		self.position['Y'] = restrict(self.position['Y'], 125, 0)

	def movingThread(self):
		while self.collectInput:
			if self.isMoving:
				self.position['X'] += self.deltaX
				self.position['Y'] += self.deltaY
				self.restrainPositions()
				command = {
					'commands': [ 'G90', 'G1 X' + str(self.position['X']) + ' Y' + str(self.position['Y']) + ' Z' + str(self.position['Z']) + ' F1000' ]
				}
				requests.post(
					self.bioprintBaseUrl + url,
					headers={
						'x-api-key': 'BIOBOTS_API_KEY',
						'x-socket-key': 'BIOBOTS_SOCKET_KEY',
						'Content-Type': 'application/json'
					},
					json=body
				)
				time.sleep(0.25)
		print(threading.currentThread().getName(), 'Exiting')


	def read(self):
		data = self.__input_translate(self.device.read(64))
		url = 'printer/command'
		body = {}

		for button in data['buttons']:
			if(button == 'A'):
				body = {
					'commands': [
						'G90',
						'G1 Z50 F1000',
						'T0',
						'M400',
						'G1 E 24 F1000.00',
						'M400',
						'G91',
						'G1 X -48.33 F2000.00',
						'G90',
						'M400',
						'G1 E 46 F1000.00',
						'G1 Z' + str(self.position['Z']) + ' F1000',
						'M400',
					]
				}
			elif(button == 'B'):
				body = {
					'commands': [
						'G90',
						'G1 Z50 F1000',
						'T0',
						'M400',
						'G1 E 24 F1000.00',
						'M400',
						'G91',
						'G1 X 48.33 F2000.00',
						'G90',
						'M400',
						'G1 E 0 F1000.00',
						'G1 Z' + str(self.position['Z']) + ' F1000',
						'M400',
					]
				}
			elif(button == 'X'):
				body = {
					'commands': [
						'G90',
						'G1 X' + str(self.position['X']) + ' Y' + str(self.position['Y']) + ' Z' + str(self.position['Z'] + 1) + ' F1000'
					]
				}
				self.position['Z'] += 1
			elif(button == 'Y'):
				body = {
					'commands': [
						'G90',
						'G1 X' + str(self.position['X']) + ' Y' + str(self.position['Y']) + ' Z' + str(self.position['Z'] - 1) + ' F1000'
					]
				}
				self.position['Z'] -= 1
			elif(button == 'LT'):
				body = {
					'commands': [
						'G90',
						'G1 M42 P16 S255',
					]
				}
				self.isExtruding = True
			elif(button == 'RT'):
				body = {
					'commands': [
						'G90',
						'G1 M42 P17 S255',
					]
				}
				self.isExtruding = True
			elif (self.isExtruding and button != 'RT' and button != 'LT'):
				body = {
					'commands': [
						'G90',
						'G1 M42 P16 S0',
						'G1 M42 P17 S0',
					]
				}
		
		if body:
			requests.post(
				self.bioprintBaseUrl + url,
				headers={
					'x-api-key': 'BIOBOTS_API_KEY',
					'x-socket-key': 'BIOBOTS_SOCKET_KEY',
					'Content-Type': 'application/json'
				},
				json=body
			)
		
		directions = data['thumpad']
		w_e = directions[0]
		n_s = directions[1]
		if not (not w_e and not n_s):
			self.deltaX = (1 if w_e == 'W' else -1) if w_e != '' else 0
			self.deltaY = (1 if n_s == 'N' else -1) if n_s != '' else 0
			if not self.isMoving:
				self.isMoving = True
		else:
			self.isMoving = False
			

	def __input_translate(self, data):
		values = {
			0: 'Released', 1: 'A', 2: 'B', 4: 'X', 8: 'Y', 16: 'LT', 32: 'RT'
		}

		def return_button_value():
			if 'buttons' in output.keys():
					output["buttons"].append(values[int(math.pow(2, curr_number))])
			else:
					output['buttons'] = [values[int(math.pow(2, curr_number))]]

		def return_we(value):
			if value > 63:
					return 'E'
			elif value < 63:
					return 'W'
			else:
					return ''

		def return_ns(value):
			if value > 63:
					return 'S'
			elif value < 63:
					return 'N'
			else:
					return ''

		output = {}
		binary_buttons = bin(data[2])[2:]
		curr_number = 0
		for integer in binary_buttons[::-1]:
				if int(integer) == 1:
						return_button_value()
				curr_number += 1
		if 'buttons' not in output.keys():
				output['buttons'] = values[0]

		output['thumpad'] = [return_we(data[0]), return_ns(data[1])]
		return output

	def _getRemoteAddress(self, info):
		forwardedFor = info.headers.get("X-Forwarded-For")
		if forwardedFor is not None:
			return forwardedFor.split(",")[0]
		return info.ip

	def on_open(self, info):
		self._remoteAddress = self._getRemoteAddress(info)
		self._logger.info("New connection from client: %s" % self._remoteAddress)

		plugin_signature = lambda impl: "{}:{}".format(impl._identifier, impl._plugin_version)
		template_plugins = map(plugin_signature, self._pluginManager.get_implementations(bioprint.plugin.TemplatePlugin))
		asset_plugins = map(plugin_signature, self._pluginManager.get_implementations(bioprint.plugin.AssetPlugin))
		ui_plugins = sorted(set(template_plugins + asset_plugins))

		import hashlib
		plugin_hash = hashlib.md5()
		plugin_hash.update(",".join(ui_plugins))

		# connected => update the API key, might be necessary if the client was left open while the server restarted
		self._emit("connected", {
			"apikey": bioprint.server.UI_API_KEY,
			"version": bioprint.server.VERSION,
			"display_version": bioprint.server.DISPLAY_VERSION,
			"branch": bioprint.server.BRANCH,
			"plugin_hash": plugin_hash.hexdigest()
		})

		self._printer.register_callback(self)
		self._fileManager.register_slicingprogress_callback(self)
		bioprint.timelapse.registerCallback(self)
		self._pluginManager.register_message_receiver(self.on_plugin_message)

		self._eventManager.fire(Events.CLIENT_OPENED, {"remoteAddress": self._remoteAddress})
		for event in bioprint.events.all_events():
			self._eventManager.subscribe(event, self._onEvent)

		bioprint.timelapse.notifyCallbacks(bioprint.timelapse.current)
		self.deviceReadingThread = threading.Thread(name='Device Reader', target=self.initializeDevice)
		self.collectInput = True
		self.deviceReadingThread.daemon = True
		self.deviceReadingThread.start()

	def on_close(self):
		self._logger.info("Client connection closed: %s" % self._remoteAddress)
		self._printer.unregister_callback(self)
		self._fileManager.unregister_slicingprogress_callback(self)
		bioprint.timelapse.unregisterCallback(self)
		self._pluginManager.unregister_message_receiver(self.on_plugin_message)

		self._eventManager.fire(Events.CLIENT_CLOSED, {"remoteAddress": self._remoteAddress})
		for event in bioprint.events.all_events():
			self._eventManager.unsubscribe(event, self._onEvent)
		self.collectInput = False

	def on_message(self, message):
		pass

	def on_printer_send_current_data(self, data):
		# add current temperature, log and message backlogs to sent data
		with self._temperatureBacklogMutex:
			temperatures = self._temperatureBacklog
			self._temperatureBacklog = []

		with self._logBacklogMutex:
			logs = self._logBacklog
			self._logBacklog = []

		with self._messageBacklogMutex:
			messages = self._messageBacklog
			self._messageBacklog = []

		busy_files = [dict(origin=v[0], name=v[1]) for v in self._fileManager.get_busy_files()]
		if "job" in data and data["job"] is not None \
				and "file" in data["job"] and "name" in data["job"]["file"] and "origin" in data["job"]["file"] \
				and data["job"]["file"]["name"] is not None and data["job"]["file"]["origin"] is not None \
				and (self._printer.is_printing() or self._printer.is_paused()):
			busy_files.append(dict(origin=data["job"]["file"]["origin"], name=data["job"]["file"]["name"]))

		data.update({
			"serverTime": time.time(),
			"temps": temperatures,
			"logs": logs,
			"messages": messages,
			"busyFiles": busy_files,
		})

		self._emit("current", data)

	def on_printer_send_initial_data(self, data):
		data_to_send = dict(data)
		data_to_send["serverTime"] = time.time()
		self._emit("history", data_to_send)

	def sendEvent(self, type, payload=None):
		self._emit("event", {"type": type, "payload": payload})

	def sendTimelapseConfig(self, timelapseConfig):
		self._emit("timelapse", timelapseConfig)

	def sendSlicingProgress(self, slicer, source_location, source_path, dest_location, dest_path, progress):
		self._emit("slicingProgress",
		           dict(slicer=slicer, source_location=source_location, source_path=source_path, dest_location=dest_location, dest_path=dest_path, progress=progress)
		)

	def on_plugin_message(self, plugin, data):
		self._emit("plugin", dict(plugin=plugin, data=data))

	def on_printer_add_log(self, data):
		with self._logBacklogMutex:
			self._logBacklog.append(data)

	def on_printer_add_message(self, data):
		with self._messageBacklogMutex:
			self._messageBacklog.append(data)

	def on_printer_add_temperature(self, data):
		with self._temperatureBacklogMutex:
			self._temperatureBacklog.append(data)

	def _onEvent(self, event, payload):
		self.sendEvent(event, payload)

	def _emit(self, type, payload):
		try:
			self.send({type: payload})
		except Exception as e:
			self._logger.warn("Could not send message to client %s: %s" % (self._remoteAddress, str(e)))
