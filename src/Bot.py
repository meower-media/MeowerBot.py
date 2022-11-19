import cloudlink
import sys

import json
import traceback

import requests

class Bot:
	BOT_TAKEN_LISTENERS = ["__meowerbot__send_ip", "__meowerbot__send_message", "__meowerbot__login", "__meowerbot__cloudlink_trust" ]
	def __init__(self, debug=False, debug_out=sys.__stdout__):
		self.wss = cloudlink.Cloudlink(debug = debug)
		self._stdout = sys.__stdout__
		self.debug = debug
		self.debug_out = debug_out 

		self.callbacks = {}

		self.wss.callback("on_packet", self._debug_fix) # self._debug_fix catches all errors
		self.wss.callback("on_error", self.__handle_error__) #handle uncought errors
		self.wss.callback("on_close", self.__handle_close__) # Websocket disconnected
		self.wss.callback("on_connect", self.__handle_on_connect__) # signing in and stuff like that


	def run_cb(cbid, args=(), kwargs=None):
		if not cbid in self.callbacks: return #ignore
		if not kwargs: kwargs = {}

		kwargs['bot'] = self

		for callback in self.callbacks[cbid]:
			callback(*args, **kwargs) # multi callback per id is supported (unlike cloudlink 0.1.7.3 LOL)

	def __handle_error__(self, e):
		self.run_cb("error", args=(e))

	def _debug_fix(self, packet):
		packet = json.loads(packet) # Server bug workaround

		try:
			self.__handle_packet__(packet)
		except Exeption as e:
			if self.debug:
				self.debug_out.write(traceback.format_exc())
			self.run_cb("error", args=(e))

		try:
			self.run_cb("__raw__", args=(packet)) #raw packets
		except Exeption as e:
			if self.debug:
				self.debug_out.write(traceback.format_exc())
			self.run_cb("error", args=(e))


	def __handle_on_connect__(self):
		self.wss.sendPacket(
    		{
				"cmd": "direct",
				"val": {
    				"cmd": "ip",
    				"val": requests.get("https://api.meower.org/ip").text,
				},
			"listener":"__meowerbot__send_ip"
    		}
		)


	def _handle_status(self, status,  listener):
		if listener == "__meowerbot__send_ip":
			if not status == "I:100 | OK":
				raise RuntimeError("Sending IP FAILED")
			self.wss.sendPacket(
    			{
					"cmd": "direct",
					"val": {"cmd": "type", "val": "py"},
    			}
			)
       
			self.wss.sendPacket(
    			{
					"cmd": "direct",
    	    		"val": "meower",
					"listener": "__meowerbot__cloudlink_trust"
    			}
			)

		elif  listener == "__meowerbot__cloudlink_trust":
			if not status == "I:100 | OK":
				raise RuntimeError("CloudLink Trust Failed")

			self.wss.sendPacket({
				"cmd": "direct",
				"val": {
    				"cmd": "authpswd",
   				 	"val": {"username": self.username, "pswd": self.password},
				},
					"listener":"__meowerbot__login"
			    })

		elif listener == "__meowerbot__login":
			if not status == "I:100 | OK":
				raise RuntimeError("Password Or Username Is Incorrect")

			self.run_cb("login")

		elif listener == "__meowerbot__send_message":
			if status == "I:100 | OK": return # This is just checking if a post went OK

			raise RuntimeError("Post Failed to send")

	def callback(self, callback, cbid=None):
		cbid = cbid if not cbid is None else callback.__name__

		if not cbid in self.callbacks:
			self.callbacks[cbid] = [callback]
			return
		self.callbacks[cbid].append(callback)


	def  __handle_close__(self, *args, **kwargs):
		self.run_cb("close", args=args, kwargs=kwargs)

	def __handle_packet__(self, packet):
		if packet['cmd'] == "statuscode":
			if packet.get('listener', None) in self.BOT_TAKEN_LISTENERS: # Requried listeners for the bot
				self._handle_status(packet['val'], packet['listener'])
				return 
			else:
				listener = packet.get("listener", None)
				return self.run_cb("statuscode", args=(packet['val'], listener))

		elif packet['cmd'] == "ulist":
			self.run_cb("ulist", self.wss.statedata['ulist']['usernames'])



		elif packet['cmd'] == "direct" and 'post_origin' in packet['val']: # Message Handler
			# TODO: MAKE A CTX/MESSAGE OBJ SYSTEM. 
			# POSSIBLY MAKE A BUILTIN CMD SYSTEM


			self.run_cb("message", args=(packet['val']))
		elif packet['cmd'] == "direct":
			listener = packet.get("listener")
			self.run_cb("direct", args=(packet['val'], lister))

		else:
			listener = packet.get("listener")
			self.run_cb(packet['cmd'], args=(packet['val'], listener))

	def send_msg(msg, to="home"):
		if to == "home":
			self.wss.sendPacket({
				"cmd":"direct",
				"val":{"cmd":"post_home", "val":msg}
			})
		else:
			self.wss.sendPacket({"cmd":"direct", "val":{"cmd":"post_chat", "val":{"chatid":to, "p":msg}}})

	def run(self, username, password, server="server.meower.org"):
		with self.debug_out as sys.stdout:
			self.wss.connect(server)


