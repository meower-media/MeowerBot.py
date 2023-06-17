import unittest
from unittest.mock import MagicMock
from MeowerBot.command import AppCommand

class TestAppCommand(unittest.TestCase):
	def setUp(self):
		self.mock_connected = MagicMock()
		self.command = AppCommand(lambda ctx,a,b: None, name="testcmd", args=2)

	def test_call(self):
		# Test that calling an AppCommand raises a RuntimeError
		cmd = AppCommand(lambda: None)
		with self.assertRaises(RuntimeError):
			cmd()

	def test_register_class(self):
		# Test that registering a class sets the connected attribute
		cmd = AppCommand(lambda: None)
		cmd.register_class(self.mock_connected)
		self.assertEqual(cmd.connected, self.mock_connected)

	def test_subcommand(self):
		# Test that adding a subcommand updates the subcommands dictionary
		
		self.command.subcommand(name="subcmd")(lambda: None)

		self.assertIn("subcmd", self.command.subcommands)
		self.assertEqual(len(self.command.subcommands), 1)

	def test_run_cmd(self):
		# Test that running a command calls the correct function with the correct arguments
		mock_func = MagicMock()
		mock_func.__annotations__  =  {}
		mock_func.__name__ = "mock_func"
		cmd = AppCommand(mock_func, args=2)

		cmd.run_cmd(None, "arg1", "arg2")
		mock_func.assert_called_with(None, "arg1", "arg2")



if __name__ == "__main__":
	unittest.main()