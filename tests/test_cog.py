import unittest
from unittest.mock import MagicMock
from MeowerBot.cog import Cog
from MeowerBot.command import command, AppCommand

class CogTestingCog(Cog):
	@command("command1")
	def command1(self):
		pass

	@command("command2")
	def command2(self):
		pass

class TestCog(unittest.TestCase):
    def setUp(self):
        self.cog = CogTestingCog()

    def test_commands(self):
        # Test that all commands are registered
        self.assertEqual(len(self.cog.__commands__), 2)

		


        # Test that the commands are registered correctly
        self.assertIn("command1", self.cog.__commands__)
        self.assertIn("command2", self.cog.__commands__)

    def test_get_info(self):
        # Test that the get_info method returns the correct commands
        info = self.cog.get_info()

        self.assertIn("command1", info)
        self.assertIn("command2", info)


if __name__ == "__main__":
	unittest.main()