import asyncio
import json

import websockets


class Client:
	"""
	MeowerBot.py's async websocket wrapper.
	"""
	ws: websockets.WebSocketClientProtocol
	message_condition: asyncio.Condition
	_packets: list

	def __init__(self):
		self.ws = None
		self._packets = []
		self.message_condition = asyncio.Condition()
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
		loop = asyncio.get_event_loop()
		async for websocket in websockets.connect(server, ping_interval=None): # Meower uses its own implementation, crashes the connection if left on.
			try:

				self.ws = websocket
				try:
					_task = loop.create_task(self._connect()) # noqa
				except Exception as e:
					await self._error(e)

				async for message in websocket:
					try:
						data = json.loads(message)
						async with self.message_condition:
							self._packets.append(data)
							self.message_condition.notify_all()
							self._packets = self._packets[:50]


						await self._message(data)


					except websockets.ConnectionClosed:
						await self._disconnect()

					except Exception as e:

						await self._error(e)

			except websockets.ConnectionClosed:
				await self._disconnect()
				pass

			except Exception as e:
				await self._error(e)

		await self._disconnect()
