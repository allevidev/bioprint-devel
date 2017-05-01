# coding=utf-8
from __future__ import absolute_import

import logging
import threading
import sockjs.tornado
import time

import bioprint.timelapse
import bioprint.server
from bioprint.events import Events

import bioprint.printer
from socketIO_client import SocketIO, LoggingNamespace
import json
import requests 

BIOPRINT_BASE_URL = 'http://localhost:8090/api/'
PRINTER_ID = '0001' #make env variable
CLIENT_TYPE = 'PRINTER' #make const
SOCKET_MANAGER_LOGGING_PREFIX = 'CLOUD SOCKET MANAGER: '
BIOBOTS_CLOUD_SOCKET_MANAGER = 'http://127.0.0.1'
BIOBOTS_CLOUD_SOCKET_MANAGER_PORT = 4000


def logSocketManager(stringToLog):
	print SOCKET_MANAGER_LOGGING_PREFIX , stringToLog



class SocketManager(sockjs.tornado.SockJSConnection, bioprint.printer.PrinterCallback):

	
	def __init__(self, eventManager):
		self.currentClient = None
		self.currentClientType = None
		self.connected = False

		#	NOT WORKING 
		#self._eventManager = eventManager
		#self._eventManager.fire(Events.CLIENT_OPENED, {"remoteAddress": "test"})
		#for event in bioprint.events.all_events():
		#	self._eventManager.subscribe(event, self._on_event)

		self.cloudManagerSocket = SocketIO(BIOBOTS_CLOUD_SOCKET_MANAGER, BIOBOTS_CLOUD_SOCKET_MANAGER_PORT, LoggingNamespace)	#	TODO: CHange to env variables

		self.cloudManagerSocket.on('connect', self._on_connect_cloud)
		self.cloudManagerSocket.on('disconnect', self._on_disconnect_cloud)
		self.cloudManagerSocket.on('reconnect', self._on_reconnect_cloud)
		self.cloudManagerSocket.on('COMMAND', self._on_command_cloud)
		self.cloudManagerSocket.wait()

	def _on_event(self, event, payload):
		if (self.currentClient == None or self.currentClientType == None or self.connected == False):
			pass

		self.cloudManagerSocket.emit('SEND_MESSAGE', {
      'targetClientType': self.currentClientType,
      'targetClient': self.currentClient,
      'command': 'UPDATE',
      'response': "SEND EVENT HERE",
		})
	
	def _on_connect_cloud(self):
		self.connected = True
		#	Let Biobots Cloud Socket Manager know that this instance 
		#	of bioprint is controlling printer: PRINTER_ID
		self.cloudManagerSocket.emit('IDENTIFY_CLIENT', {
      "clientType": CLIENT_TYPE,
      "client": PRINTER_ID
    })
		logSocketManager('Connected to BioBots Cloud Socket Manager')

	def _on_disconnect_cloud(self):
	  logSocketManager('Disconnected to BioBots Cloud Socket Manager')

	def _on_reconnect_cloud():
	  logSocketManager('Reconnecting to BioBots Cloud Socket Manager')

	#	Fired when command from user is sent to this printer
	def _on_command_cloud(self, *args):
		self.currentClient = args[0]["callbackClientTarget"]

		if (args[0]['type'] == 'GET'):
			r = requests.get(
				BIOPRINT_BASE_URL + args[0]["urlExtension"],
				headers={
					'x-api-key': 'F9C07883B62C41B888335D4A2A07B07E',
					'Content-Type': 'application/json'
				},)
		elif (args[0]['type'] == 'POST'):
			r = requests.post(
					BIOPRINT_BASE_URL + args[0]["urlExtension"],
					headers={
		    		'x-api-key': 'F9C07883B62C41B888335D4A2A07B07E',
		    		'Content-Type': 'application/json'
		  		},
		  		json=args[0]['body']
				)

		if (r.status_code >= 200 and r.status_code <= 300): 
			logSocketManager('API Request Successful')
			self.cloudManagerSocket.emit('SEND_MESSAGE', {
        'targetClientType': args[0]["callbackClientType"],
        'targetClient': args[0]["callbackClientTarget"],
        'command': args[0]["emitMessageResponseCallback"],
        'response':  r.json(),
			})
		else:
			logSocketManager('API Request Failed')
			self.cloudManagerSocket.emit('SEND_MESSAGE', {
	  		'targetClientType': args[0]["callbackClientType"],
	  		'command': args[0]["emitMessageFailureCallback"],
        'targetClient': args[0]["callbackClientTarget"],
	      'response' : "Could not complete bioprint api request",
			})





