# coding=utf-8
from __future__ import absolute_import

__author__ = "Gina Häußge <osd@foosel.net>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2014 The bioprint Project - Released under terms of the AGPLv3 License"

from flask import request, jsonify, abort, make_response, session
from werkzeug.exceptions import BadRequest
from flask.ext.login import current_user

import bioprint.users as users

from bioprint.server import SUCCESS, admin_permission, userManager
from bioprint.server.api import api
from bioprint.server.util.flask import restricted_access

import requests
from requests.auth import HTTPDigestAuth

#~~ user settings


@api.route("/users", methods=["GET"])
@restricted_access
@admin_permission.require(403)
def getUsers():
	if userManager is None:
		return jsonify(SUCCESS)

	return jsonify({"users": userManager.getAllUsers()})


@api.route("/users", methods=["POST"])
@restricted_access
@admin_permission.require(403)
def addUser():
	if userManager is None:
		return jsonify(SUCCESS)

	if not "application/json" in request.headers["Content-Type"]:
		return make_response("Expected content-type JSON", 400)

	try:
		data = request.json
	except BadRequest:
		return make_response("Malformed JSON body in request", 400)

	name = data["name"]
	password = data["password"]
	active = data["active"]

	roles = ["user"]
	if "admin" in data.keys() and data["admin"]:
		roles.append("admin")

	try:
		userManager.addUser(name, password, active, roles)
	except users.UserAlreadyExists:
		abort(409)
	return getUsers()


@api.route("/users/<username>", methods=["GET"])
@restricted_access
def getUser(username):
	if userManager is None:
		return jsonify(SUCCESS)

	if current_user is not None and not current_user.is_anonymous() and (current_user.get_name() == username or current_user.is_admin()):
		user = userManager.findUser(username)
		if user is not None:
			return jsonify(user.asDict())
		else:
			abort(404)
	else:
		abort(403)


@api.route("/users/<username>", methods=["PUT"])
@restricted_access
@admin_permission.require(403)
def updateUser(username):
	if userManager is None:
		return jsonify(SUCCESS)

	user = userManager.findUser(username)
	if user is not None:
		if not "application/json" in request.headers["Content-Type"]:
			return make_response("Expected content-type JSON", 400)

		try:
			data = request.json
		except BadRequest:
			return make_response("Malformed JSON body in request", 400)

		# change roles
		roles = ["user"]
		if "admin" in data.keys() and data["admin"]:
			roles.append("admin")
		userManager.changeUserRoles(username, roles)

		# change activation
		if "active" in data.keys():
			userManager.changeUserActivation(username, data["active"])
		return getUsers()
	else:
		abort(404)


@api.route("/users/<username>", methods=["DELETE"])
@restricted_access
@admin_permission.require(http_exception=403)
def removeUser(username):
	if userManager is None:
		return jsonify(SUCCESS)

	try:
		userManager.removeUser(username)
		return getUsers()
	except users.UnknownUser:
		abort(404)


@api.route("/users/<username>/password", methods=["PUT"])
@restricted_access
def changePasswordForUser(username):
	if userManager is None:
		return jsonify(SUCCESS)

	if current_user is not None and not current_user.is_anonymous() and (current_user.get_name() == username or current_user.is_admin()):
		if not "application/json" in request.headers["Content-Type"]:
			return make_response("Expected content-type JSON", 400)

		try:
			data = request.json
		except BadRequest:
			return make_response("Malformed JSON body in request", 400)

		if not "password" in data.keys() or not data["password"]:
			return make_response("password is missing from request", 400)

		try:
			userManager.changeUserPassword(username, data["password"])
		except users.UnknownUser:
			return make_response(("Unknown user: %s" % username, 404, []))

		return jsonify(SUCCESS)
	else:
		return make_response(("Forbidden", 403, []))


@api.route("/users/<username>/settings", methods=["GET"])
@restricted_access
def getSettingsForUser(username):
	if userManager is None:
		return jsonify(SUCCESS)

	if current_user is None or current_user.is_anonymous() or (current_user.get_name() != username and not current_user.is_admin()):
		return make_response("Forbidden", 403)

	try:
		return jsonify(userManager.getAllUserSettings(username))
	except users.UnknownUser:
		return make_response("Unknown user: %s" % username, 404)

@api.route("/users/<username>/settings", methods=["PATCH"])
@restricted_access
def changeSettingsForUser(username):
	if userManager is None:
		return jsonify(SUCCESS)

	if current_user is None or current_user.is_anonymous() or (current_user.get_name() != username and not current_user.is_admin()):
		return make_response("Forbidden", 403)

	try:
		data = request.json
	except BadRequest:
		return make_response("Malformed JSON body in request", 400)

	try:
		userManager.changeUserSettings(username, data)
		return jsonify(SUCCESS)
	except users.UnknownUser:
		return make_response("Unknown user: %s" % username, 404)

@api.route("/users/<username>/apikey", methods=["DELETE"])
@restricted_access
def deleteApikeyForUser(username):
	if userManager is None:
		return jsonify(SUCCESS)

	if current_user is not None and not current_user.is_anonymous() and (current_user.get_name() == username or current_user.is_admin()):
		try:
			userManager.deleteApikey(username)
		except users.UnknownUser:
			return make_response(("Unknown user: %s" % username, 404, []))
		return jsonify(SUCCESS)
	else:
		return make_response(("Forbidden", 403, []))


@api.route("/users/<username>/apikey", methods=["POST"])
@restricted_access
def generateApikeyForUser(username):
	if userManager is None:
		return jsonify(SUCCESS)

	if current_user is not None and not current_user.is_anonymous() and (current_user.get_name() == username or current_user.is_admin()):
		try:
			apikey = userManager.generateApiKey(username)
		except users.UnknownUser:
			return make_response(("Unknown user: %s" % username, 404, []))
		return jsonify({"apikey": apikey})
	else:
		return make_response(("Forbidden", 403, []))



###############################
# NEW METHODS
###############################

# Environment vairables to be defines
BIOBOTS_API_URL = "http://localhost:8080/"


@api.route("/user/entries/extruder", methods=["POST"])
def getExtruderEntries():
	if userManager is None:
		return jsonify(SUCCESS)

	if not (isNetworkAvailable()):
		return jsonify({"status": False})
	
	try:
		url = BIOBOTS_API_URL + "user/entries"
		
		payload = {
			"filters": {
				
			}
		}

		headers = {
			"Content-Type": "application/json",
			"Authorization": "Bearer " + session["BIOBOTS_API_TOKEN"] 
		}

		r = requests.post(url, headers=headers, json=payload)

		if (r.status_code == 200):
			return jsonify({
				"status": True, 
				"result": r.json()
				})		
		else:
			return jsonify({
				"status": False, 
				"result": None
			})

	except requests.exceptions.RequestException as e:  
		return jsonify({
				"status": False, 
				"result": None
			})


@api.route("/user/entry/update", methods=["POST"])
def updateEntry():
	print jsonify(request.get_json(force=True))

	if not "application/json" in request.headers["Content-Type"]:
		return make_response("Expected content-type JSON", 400)

	try:
		data = request.json
	except BadRequest:
		return make_response("Malformed JSON body in request", 400)

	print '\n\n\n\n\n', data, '\n\n\n\n'

	if userManager is None:
		return jsonify(SUCCESS)

	if not (isNetworkAvailable()):
		return jsonify({"status": False})

	
	try:
		url = BIOBOTS_API_URL + "entry/update"
		
		payload = {
			# This needs to be request.json.id (NOT WORKING)
			"id": "580ef4b4eb77ec88005a774e",

			# This needs to be request.json.content (NOT WORKING)
			"content": {
		      "xPosition": 5,
		      "yPosition": 11,
		      "zPosition": 15,
		      "temperature": 71,
		      "pressure": 27,
		      "revision": 1,
		      "type": [
		        'extruder1',
		        'extruder2',
		      ],
		    }
		}

		headers = {
			"Content-Type": "application/json",
			"Authorization": "Bearer " + session["BIOBOTS_API_TOKEN"] 
		}

		r = requests.post(url, headers=headers, json=payload)

		if (r.status_code == 200):
			return jsonify({
				"status": True, 
				"result": r.json()
				})		
		else:
			return jsonify({
				"status": False, 
				"result": None
			})

	except requests.exceptions.RequestException as e:  
		return jsonify({
				"status": False, 
				"result": None
			})

def isNetworkAvailable():
	try:
		url = BIOBOTS_API_URL
		r = requests.get(url)
		return True
	except requests.exceptions.RequestException as e:  
		return False

def getActiveUser():
	if userManager is not None:
		for users in userManager.getAllUsers():
			if users["active"]:
				return users["email"]
	else:
		return None

def createAPIUser(email, password):
	url = BIOBOTS_API_URL + "user/new"
	payload = {
	"email": email,
	"password": password,
	"kind": "STANDARD"
	}

	try:
		r = requests.post(url, json=payload)
		return True
	except requests.exceptions.RequestException as e:  
		return False



