import websockets
import orjson
import json

import asyncio

class Client:
	__waiting = {}
	__packets = []
	ws: websockets.WebSocketClientProtocol
	def __init__(self):
		self.ws = None
		pass

	async def _connect(self):
		pass

	async def _disconnect(self):
		pass

	async def _message(self, message):
		pass

	async def _error(self, error):
		pass

	async def sendPacket(self, message):
		await self.ws.send(json.dumps(message))
	
	async def sendPacketAndWait(self, message):
		await self.ws.send(json.dumps(message))

		self.__waiting[message["listener"]] = asyncio.Event()

		got_response = False
		statuscode = ""
		waited = None

	

		async def predicate():
			
			
			nonlocal got_response
			nonlocal statuscode

			#get the last added packet
			packet = self.__packets[-1]

			if message["listener"] != packet["listener"]:
				return False

			if packet["cmd"] == "statuscode":
				statuscode = packet["val"]
			
			else:
				got_response = True
				nonlocal waited
				waited = waitedPacked.WaitedPacked(statuscode == "I: 100 | OK", packet, packet["listener"])

				


			return message["listener"] in self.__waiting and got_response
		
		await self.__waiting[message["listener"]].wait_for(predicate)

		return waited




	async def close(self, reason=None):
		await self.ws.close(reason=reason)



	async def connect(self, server):
		async for websocket in websockets.connect(server):
			try:

				self.ws = websocket
				await self._connect()
				
				async for message in websocket:
					try:

						packet = json.loads(message)

						for listener in self.__waiting:
							if listener == packet["listener"]:
								self.__waiting[listener].notify_all()


						await self._message(json.loads(message))

						#cut packet queue to 50
						if len(self.__packets) > 50:
							self.__packets = self.__packets[-50:]
							
					
					except websockets.ConnectionClosed:
						raise

					except Exception as e:
					
						await self._error(e)
						pass

			except websockets.ConnectionClosed:
				await self._disconnect()
				pass

			except Exception as e:
				await self._error(e)
				pass

		
		await self._disconnect()
