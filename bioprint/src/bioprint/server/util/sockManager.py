# coding=utf-8
from __future__ import absolute_import

import logging
import threading
import sockjs.tornado
import time
import json
import yaml

import bioprint.timelapse
import bioprint.server
from bioprint.events import Events

import bioprint.printer
from bioprint.settings import settings
from socketIO_client import SocketIO, LoggingNamespace

from kafka import KafkaProducer
import json
import requests 
import os

from threading import Thread

class SocketManager(sockjs.tornado.SockJSConnection, bioprint.printer.PrinterCallback, Thread):

	# Initalize self variables for this class
	def __init__(self, bioprintHost, bioprintPort, printer, fileManager, analysisQueue, userManager, eventManager, pluginManager, session):
		Thread.__init__(self)
		sockjs.tornado.SockJSConnection.__init__(self, session) # not sure if this is necessary - testing once I go in on monday
		#	Environment Variables
		self.cloudSocketManagerURL = os.environ.get('BIOBOTS_CLOUD_SOCKET_MANAGER_URL', 'http://socket.biobots.io')		# Biobots cloud socket manager URL
		self.cloudSocketManagerPort = os.environ.get('BIOBOTS_CLOUD_SOCKET_MANAGER_PORT', 80)	#Biobots cloud socket manager PORT


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

		self.currentClient = None
		self.currentClientType = None
		self.connected = False
	
		self.bioprintBaseUrl = ''.join(['http://', bioprintHost, ':', str(bioprintPort), '/api/']) #	This instance's url
		self.bioprintAPIKey = bioprint.server.UI_API_KEY
		self.socketKey = bioprint.server.SOCKET_KEY
	
		#	Socket Events
		self.CONNECT = 'connect'
		self.DISCONNECT = 'disconnect'
		self.RECONNECT = 'reconnect'
		self.COMMAND = 'COMMAND'
		self.UNREACHABLE_TARGET = 'UNREACHABLE_TARGET'
		self.IDENTIFY_CLIENT = 'IDENTIFY_CLIENT'
		self.SEND_MESSAGE = 'SEND_MESSAGE'

	#	Fired on <thread>.start() event of this class
	def run(self):
		self.cloudManagerSocket = SocketIO(self.cloudSocketManagerURL, self.cloudSocketManagerPort, LoggingNamespace)	#	TODO: CHange to env variables


		self.cloudManagerSocket.on(self.CONNECT, self._on_connect_cloud)
		self.cloudManagerSocket.on(self.DISCONNECT, self._on_disconnect_cloud)
		self.cloudManagerSocket.on(self.RECONNECT, self._on_reconnect_cloud)
		self.cloudManagerSocket.on(self.COMMAND, self._on_command_cloud)
		self.cloudManagerSocket.on(self.UNREACHABLE_TARGET, self._on_unreachable_target)
		
		self.cloudManagerSocket.wait()
	
	#	Fired when bioprint is connected to BioBots Cloud Socket Manager
	def _on_connect_cloud(self):
		print "CONNECTED"
		self.connected = True
		__dir__ = '/usr/share/biobots-config/'
		__file__ = 'userdata'
		
		self.emailExists = False
		self.userEmail = None
		if os.path.isdir(__dir__):
			if os.path.exists(os.path.join(__dir__, __file__)):
				f = open(os.path.join(__dir__, __file__), 'r')	
				self.emailExists = True;
				lines = f.readlines()
				if len(lines) < 1:
					self.emailExists = False
				else:
					self.userEmail = lines[0]
				f.close()	
		else:
			self.userEmail = os.environ.get('BIOBOTS_EMAIL_ADDRESS')
			self.emailExists = True

		#	Let Biobots Cloud Socket Manager know that this instance 
		#	of bioprint is controlling printer: self.printerId
		self.cloudManagerSocket.emit(self.IDENTIFY_CLIENT, {
      "clientType": settings().get(["printerData", "clientType"]),
      "client": settings().get(["printerData", "serialNumber"]),
      "emailExists": self.emailExists,
      "email": self.userEmail,
      "model": settings().get(["printerData", "model"]),
      "version": settings().get(["printerData", "version"]), 
      "serialNumber": settings().get(["printerData", "serialNumber"])
    })
		self._logger.info("Connected to BioBots Cloud Socket Manager")

		plugin_signature = lambda impl: "{}:{}".format(impl._identifier, impl._plugin_version)
		template_plugins = map(plugin_signature, self._pluginManager.get_implementations(bioprint.plugin.TemplatePlugin))
		asset_plugins = map(plugin_signature, self._pluginManager.get_implementations(bioprint.plugin.AssetPlugin))
		ui_plugins = sorted(set(template_plugins + asset_plugins))

		import hashlib
		plugin_hash = hashlib.md5()
		plugin_hash.update(",".join(ui_plugins))

		self._emit("connected", {
			"apikey": self.bioprintAPIKey,
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

	#	Fired when bioprint is disconnected to BioBots Cloud Socket Manager
	def _on_disconnect_cloud(self):
		self.connected = False
		self._printer.unregister_callback(self)
		self._fileManager.unregister_slicingprogress_callback(self)
		bioprint.timelapse.unregisterCallback(self)
		self._pluginManager.unregister_message_receiver(self.on_plugin_message)

		self._eventManager.fire(Events.CLIENT_CLOSED, {"remoteAddress": self._remoteAddress})
		for event in bioprint.events.all_events():
			self._eventManager.unsubscribe(event, self._onEvent)

		self._logger.info("Disconnected from BioBots Cloud Socket Manager")

	#	Fired when bioprint is re-connected to BioBots Cloud Socket Manager
	def _on_reconnect_cloud(self):
		self.connected = False
		self._logger.info("Reconnecting to BioBots Cloud Socket Manager")
		self._on_connect_cloud()

	#	Fired when command from user is sent to this printer
	def _on_command_cloud(self, *args):
		self.currentClient = args[0]["callbackClientTarget"]
		self.currentClientType = args[0]["callbackClientType"]
		self._logger.info("Command: Client = %s, Client Type = %s", self.currentClient, self.currentClientType)

		if (args[0]['type'] == 'GET'):
			r = requests.get(
				self.bioprintBaseUrl + args[0]["urlExtension"],
				headers={
					'x-api-key': self.bioprintAPIKey,
					'x-socket-key': self.socketKey,
				},)
		elif (args[0]['type'] == 'POST'):
			r = requests.post(
					self.bioprintBaseUrl + args[0]["urlExtension"],
					headers={
		    		'x-api-key': self.bioprintAPIKey,
		    		'x-socket-key': self.socketKey,
		    		'Content-Type': 'application/json'
		  		},
		  		json=args[0]['body']
				)

		#	Updates user based on API request status to bioprint
		if (r.status_code >= 200 and r.status_code <= 300): 
			if r.status_code is not 204:
				json_resp = r.json()
			else:
				json_resp = json.dumps({})
			
			try:
				self._logger.info("BIOPRINT_MESSAGE {0} {1}".format("API_COMMAND_SUCCESSFUL", r.json()))
			except:
				print ""
				
			
			self.cloudManagerSocket.emit(self.SEND_MESSAGE, {
				'targetClientType': args[0]["callbackClientType"],
				'targetClient': args[0]["callbackClientTarget"],
				'command': args[0]["emitMessageResponseCallback"],
				'response':  json_resp,
			})

		else:
			try:
				self._logger.info("BIOPRINT_MESSAGE {0} {1}".format("API_COMMAND_FAILED", r.text()))
			except:
				print ""
				
			self.cloudManagerSocket.emit(self.SEND_MESSAGE, {
				'targetClientType': args[0]["callbackClientType"],
				'command': args[0]["emitMessageFailureCallback"],
				'targetClient': args[0]["callbackClientTarget"],
				'response' : "Could not complete bioprint api request",
			})

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

	#	This emit function is only used to emit updates the client e.g. events, current data... 
	#	i.e. this method should not be used to send general messages back to the user, rather user socketManager.emit(...)
	def _emit(self, type, payload):
		if not self.connected:
			self._logger.warn("Unable to emit data. Not connected to BioBots Cloud Socket Manager")	
		elif self.currentClient == None or self.currentClientType == None:	 
			self._logger.info("BIOPRINT_MESSAGE {0} {1}".format("UPDATE", json.dumps(payload)))
		else:
			try:
				self.cloudManagerSocket.emit(self.SEND_MESSAGE, {
					'targetClientType': self.currentClientType,
					'targetClient': self.currentClient,
					'command': 'UPDATE',
					'response': { 
						'type': type,
						'payload': payload,
					},
					'callbackClientTarget': settings().get(["printerData", "serialNumber"]),  	
					'callbackClientType': settings().get(["printerData", "clientType"]),		
					'unreachableTargetCallback': self.UNREACHABLE_TARGET,			
				})
				self._logger.info("BIOPRINT_MESSAGE {0} {1}".format("UPDATE", json.dumps(payload)))
			except Exception as e:
				self._logger.warn("Could not send update data to client - Update Socket Error")
				self._logger.warn(e) 

	def _on_unreachable_target(self, data):
		self._logger.warn("Unable to emit data. No client connected to printer (client will auto connect on first request)")


