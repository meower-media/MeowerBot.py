import unittest
from unittest.mock import MagicMock, patch
from MeowerBot.API import MeowerAPI

class TestMeowerAPI(unittest.TestCase):
	def setUp(self):
		self.api = MeowerAPI("testuser")
		self.mock_session = MagicMock()
		self.api.session = self.mock_session
		self.api.session.headers = {}

	def test_login(self):
		# Test that the login method sets the token header
		self.api.login("testtoken")

		self.assertIn("token", self.mock_session.headers)
		self.assertEqual(self.mock_session.headers["token"], "testtoken")

	def test_get_page_home(self):
		# Test that the get_page method returns the correct response for home page
		self.mock_session.get.return_value.json.return_value = {"page": 1}

		response = self.api.get_page()

		self.mock_session.get.assert_called_with(
			"https://api.meower.org/home?autoget&page=1"
		)
		self.assertEqual(response, {"page": 1})

	def test_get_page_chat(self):
		# Test that the get_page method returns the correct response for chat page
		self.mock_session.get.return_value.json.return_value = {"page": 1}

		response = self.api.get_page(chatid="testchat")

		self.mock_session.get.assert_called_with(
			"https://api.meower.org/posts/testchat?autoget&page=1"
		)
		self.assertEqual(response, {"page": 1})

	def test_get_user(self):
		# Test that the get_user method returns the correct response
		self.mock_session.get.return_value.json.return_value = {"username": "testuser"}

		response = self.api.get_user("testuser")

		self.mock_session.get.assert_called_with(
			"https://api.meower.org/users/testuser"
		)
		self.assertEqual(response, {"username": "testuser"})

	def test_get_user_posts(self):
		# Test that the get_user_posts method returns the correct response
		self.mock_session.get.return_value.json.return_value = {"page": 1}

		response = self.api.get_user_posts("testuser")

		self.mock_session.get.assert_called_with(
			"https://api.meower.org/users/testuser/posts?autoget&page=1"
		)
		self.assertEqual(response, {"page": 1})

	def test_statistics(self):
		# Test that the statistics method returns the correct response
		self.mock_session.get.return_value.json.return_value = {"users": 10}

		response = self.api.statistics()

		self.mock_session.get.assert_called_with(
			"https://api.meower.org/statistics"
		)
		self.assertEqual(response, {"users": 10})

	def test_status(self):
		# Test that the status method returns the correct response
		self.mock_session.get.return_value.json.return_value = {"status": "ok"}

		response = self.api.status()

		self.mock_session.get.assert_called_with(
			"https://api.meower.org/status"
		)
		self.assertEqual(response, {"status": "ok"})


if __name__ == "__main__":
	unittest.main()