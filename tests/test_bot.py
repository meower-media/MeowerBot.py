import json
import unittest
from unittest import IsolatedAsyncioTestCase

from unittest.mock import AsyncMock, patch, Mock
import asyncio
from MeowerBot import Bot, CallBackIds
from MeowerBot import bot
from httpx import Response
import httpx

from MeowerBot.api import MeowerAPI


class BotTest(IsolatedAsyncioTestCase):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.bot = Bot()
		self.bot.send_packet = AsyncMock()
		self.bot.api = MeowerAPI('')
		self.bot.api.client  = AsyncMock()
		self.bot.connect = AsyncMock()

	async def test_bots(self):
		# Mocking a successful response for the bot "Bot"
		bot_response = {
			"_id": "Bot",
			"owner": "EngineerRunner",
			"verified": True,
			"library": "MeowerBot.py"
		}
		bot_mock_response = Mock(status_code=200)
		bot_mock_response.json.return_value = bot_response
		bot_mock_response.text = "mocked response"
		bot_mock_response.raise_for_status.return_value = None
		bot_mock_get = Mock(return_value=bot_mock_response)

		# Mocking a failed response for a non-bot user "NotBot"
		not_bot_mock_response = Mock(status_code=404)
		not_bot_mock_response.raise_for_status.return_value = None
		not_bot_mock_get = Mock(return_value=not_bot_mock_response)

		# Patching httpx.get to return the mocked responses
		with patch('httpx.get', bot_mock_get) as mock_httpx_get:
			# Triggering _check_user for "Bot"
			await self.bot._check_user("Bot")
			# Asserting that "Bot" is in the cache
			self.assertIn("Bot", self.bot.cache.bots.keys())

		with patch('httpx.get', not_bot_mock_get) as mock_httpx_get:
			# Triggering _check_user for "NotBot"
			await self.bot._check_user("NotBot")
			# Asserting that "NotBot" is not in the cache
			self.assertNotIn("NotBot", self.bot.cache.bots.keys())

	async def test_ulist(self):
		# Mocking responses for bot and user API calls
		bot_response = {
			"_id": "Bot",
			"owner": "EngineerRunner",
			"verified": True,
			"library": "MeowerBot.py"
		}
		bot_mock_response = Mock(status_code=200)
		bot_mock_response.json.return_value = bot_response
		bot_mock_response.text = "mocked response"
		bot_mock_response.raise_for_status.return_value = None
		bot_mock_get = Mock(return_value=bot_mock_response)

		user_api_response = {
			"_id": "ShowierData9978",
			"avatar": "76rI2XjHKGXRX8qt9gtIdBib",
			"avatar_color": "000000",
			"banned": False,
			"created": 1656462125,
			"error": False,
			"experiments": 0,
			"flags": 0,
			"last_seen": 1710820932,
			"lower_username": "showierdata9978",
			"lvl": 0,
			"permissions": 65534,
			"pfp_data": 21,
			"quote": "Owns MeowerBot.py and RoboMeowy. Is Part of the Meower team, don't add me to random chats",
			"uuid": "4f4d986b-63ef-4f7d-9b8b-87368c6e0280"
		}

		bot_api_mock = AsyncMock(return_value=Mock(status_code=200))
		bot_api_mock.return_value.text = json.dumps(user_api_response)

		# Patching httpx.get for bot API call and bot API call wrapper
		with patch('httpx.get', bot_mock_get) as httpx_get_patch:
			with patch('MeowerBot.api.user.User._get', bot_api_mock) as bot_api_patch:
				# Triggering _message with a ulist command
				await self.bot._message({
					"cmd": "ulist",
					"val": "A;B;C;D;E"
				})

				# Asserting that httpx.get is called 5 times (once for each user)
				bot_api_mock.assert_called()
if __name__ == "__main__":
	unittest.main()
