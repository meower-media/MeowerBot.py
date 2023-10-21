import websockets
import orjson
import json
import asyncio
import random
import time
class Client:
	ws: websockets.WebSocketClientProtocol
	message_condition = asyncio.Condition()
	__messages: str

	def __init__(self):
		self.ws = None
		self.__messages = []
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

	async def _wait_for_packet(self, conditions, expected_count=None, timeout=None):
		"""
		Wait for multiple JSON packets, each meeting a specific condition, in the bot's messages list.
		Args:
		- conditions (list of dict): A list of dictionaries, each representing a condition to check for.
		- expected_count (int): Optional. The number of conditions to wait for. If None, wait for all conditions.
		- timeout (float): Optional. Maximum time to wait in seconds for the specified conditions. If None, it will wait indefinitely.
		Returns:
		- A list of messages that meet the specified conditions, or None if timeout is reached.
		"""

		
		start_time = time.time()
		received_packets = []

		while True:
			async with self.message_condition:
				await self.message_condition.wait()
				for condition in conditions:
					if expected_count is not None and len(received_packets) >= expected_count:
						return received_packets
					found = False
					for message in self.__messages:
						if all(message.get(key) == value for key, value in condition.items()):
							received_packets.append(message)
							found = True
							break
						elif message["cmd"] == "statuscode":
							return ([None]*expected_count - 1) + [message]
					if not found:
						break

				if expected_count is None and len(received_packets) == len(conditions):
					return received_packets
				if timeout is not None and time.time() - start_time >= timeout:
					return None
	
	async def send_data_request(self, packet, timeout = None):
		if packet.get("listener") == None:
			# This does not need to be sucure lmao
			packet["listener"] = random.random() # nosec

		await self.sendPacket(packet)
		return await self._wait_for_packet({"listener": packet["listener"]}, expected_count=2,  timeout=timeout)

	async def send_statuscode_request(self, packet, timeout = 0):
		if packet.get("listener") == None:
			# This does not need to be sucure lmao
			packet["listener"] = random.random() # nosec

		await self.sendPacket(packet)
		return (await self._wait_for_packet({"listener": packet["listener"]}, expected_count=1,  timeout=timeout))[0]

	async def close(self, reason=None):
		await self.ws.close(reason=reason)

	async def connect(self, server, cookies=None):
		async for websocket in websockets.connect(server, ping_interval = None): # Meower uses its own implementation, crashes the connection if left on.
			try:

				self.ws = websocket
				try:
					await self._connect()
				except Exception as e:
					print(e)

				async for message in websocket:
					try:
						data = json.loads(message)
						with self.message_condition:
							self.__messages.append(data)
							self.message_condition.notify_all()
							self.__messages = self.__messages[:50]
							

						await self._message(data)


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


