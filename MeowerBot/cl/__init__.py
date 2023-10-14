import websockets
import orjson
import json
import asyncio


class Client:
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


	async def close(self, reason=None):
		await self.ws.close(reason=reason)

	async def connect(self, server):
		async for websocket in websockets.connect(server):
			try:

				self.ws = websocket
				await self._connect()

				async for message in websocket:
					try:


						await self._message(json.loads(message))


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


