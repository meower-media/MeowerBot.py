# nosec
import unittest
from unittest.mock import MagicMock

from MeowerBot import Bot, botm

from io import StringIO
from unittest.mock import patch

#Import the bot module here


class TestBot(unittest.TestCase):
    def setUp(self):
        self.bot = Bot()
        self.bot.username = "testuser"
        self.bot._password = "testpassword" # nosec
        self.bot.wss = MagicMock()

    def test_handle_packet_statuscode(self):
        packet = {"cmd": "statuscode", "val": 200, "listener": None}

        run_cb = self.bot.run_cb
        self.bot.run_cb = MagicMock()

        try:
            result = self.bot.__handle_packet__(packet)

            self.bot.run_cb.assert_called_with("statuscode", args=(200, None))
        except:
            raise
        finally:
            self.bot.run_cb = run_cb

    
    def test_handle_packet_ulist(self):
        packet = {"cmd": "ulist", "val":"a;b;c;d"}
        runcb = self.bot.run_cb 
        self.bot.run_cb = MagicMock()
        
        try:
            result = self.bot.__handle_packet__(packet)
            self.bot.run_cb.assert_called_with("ulist", self.bot.wss.statedata["ulist"]["usernames"])
        except:
            raise
        finally:
            self.bot.run_cb = runcb

        
        


    def test_handle_packet_direct_with_message_callback(self):
        packet = {"cmd": "direct", "val": {"u":"aa", "p":"aa", "origin":"a","post_origin":"a"}}
        
        self.bot.run_command = MagicMock()

        

        #edit bots imports
        
        botm.CTX = MagicMock()
        botm.CTX.return_value = botm.CTX
        botm.CTX.message = MagicMock()

        run_cb = self.bot.run_cb
        self.bot.run_cb = MagicMock()
        self.bot.prefix = "!"
        
        try:
            result = self.bot.__handle_packet__(packet)

            self.bot.run_cb.assert_called_with("raw_message", args=(packet["val"], ))
            
        except:
            raise
        finally:
            self.bot.run_cb = run_cb

    def test_handle_packet_direct_without_message_callback(self):
        packet = {"cmd": "direct", "val": {"p": "!help", "u": "A", "origin": "123", "post_origin": "123"}}
        self.bot.callbacks = {}
        self.bot.run_command = MagicMock()
        self.bot.prefix = "!"

        #edit bots imports
        
        botm.CTX = MagicMock()
        botm.CTX.return_value = botm.CTX
        
        result = self.bot.__handle_packet__(packet)
        

        botm.CTX.assert_called_with(packet["val"], self.bot)

        assert self.bot.run_command.called # nosec 
        assert self.bot.run_command.call_args[0][0] == botm.CTX.message # nosec

        

    def test_handle_packet_direct_with_prefix(self):
        packet = {"cmd": "direct", "val": {"p": ".help","u":"A", "origin": "123", "post_origin": "123"}}
        self.bot.callbacks = {}

        
        self.bot.run_command = MagicMock()
        self.bot.prefix = "!"

        result = self.bot.__handle_packet__(packet)

        self.assertTrue(self.bot.run_command.called)

    def test_handle_packet_other_command(self):
        packet = {"cmd": "other", "val": "value", "listener": None}
        self.bot.run_cb = MagicMock()

        result = self.bot.__handle_packet__(packet)

        self.bot.run_cb.assert_called_with("other", args=("value", None))

    def test_handle_packet_pmsg(self):
        packet = {"cmd": "pmsg", "val": "Hello, world!", "origin": "123" }
        self.bot.BOT_NO_PMSG_RESPONSE = [""]
        self.bot.wss.sendPacket = MagicMock()
        self.bot.prefix = "!"
        result = self.bot.__handle_packet__(packet)

        self.bot.wss.sendPacket.assert_called_with({"cmd": "pmsg", "val": "I:500 | Bot", "id": "123"})
        botm.requests = MagicMock()

        

    def test_handle_bridges_with_bridge(self):
        packet = {"val": {"u": "user", "p": "user: message", "origin": "123", "post_origin": "123"}}
        self.bot.__bridges__ = ["user"]

        self.bot.prefix  = "!"
        result = self.bot.handle_bridges(packet)

        self.assertEqual(result["val"]["u"], "user")
        self.assertEqual(result["val"]["p"], "message")

    def test_handle_bridges_without_bridge(self):
        packet = {"val": {"u": "user", "p": "message"}}
        self.bot.__bridges__ = ["False"]

        self.bot.prefix = "!"
        result = self.bot.handle_bridges(packet)

        self.assertEqual(result["val"]["u"], "user")
        self.assertEqual(result["val"]["p"], "message")

    def test_handle_bridges_with_prefix(self):
        packet = {"val": {"u": "user", "p": "!#0000command"}}
        self.bot.__bridges__ = ["False"]

        self.bot.prefix = "!"

        result = self.bot.handle_bridges(packet)

        self.assertEqual(result["val"]["u"], "user")
        self.assertEqual(result["val"]["p"], "!command")


    def test_handle_status_trusted_access_enabled(self):
        status = "I:112 | Trusted Access enabled"
        listener = None

        result = self.bot._handle_status(status, listener)

        self.assertIsNone(result)

    def test_handle_status_logger_in(self):
        status = "I:100 | OK"
        listener = None
        self.bot.logger_in = True
        self.bot.wss.sendPacket = MagicMock()

        result = self.bot._handle_status(status, listener)

        self.bot.wss.sendPacket.assert_called_with(
            {
                "cmd": "direct",
                "val": {
                    "cmd": "authpswd",
                    "val": {"username": self.bot.username, "pswd": self.bot._password},
                },
                "listener": "__meowerbot__login",
            }
        )
        self.assertFalse(self.bot.logger_in)

    def test_handle_status_login_success(self):
        status = "I:100 | OK"
        listener = "__meowerbot__login"
        self.bot.run_cb = MagicMock()

        result = self.bot._handle_status(status, listener)

        self.bot.run_cb.assert_called_with("login", args=(), kwargs={})

    def test_handle_status_login_failure(self):
        status = "E:104 | Internal"
        listener = "__meowerbot__login"
        


        
        with patch("builtins.print", MagicMock()):
            self.bot._handle_status(status, listener)

        assert self.bot.bad_exit # nosec
 
    def test_handle_status_send_message_success(self):
        status = "I:100 | OK"
        listener = "__meowerbot__send_message"
        self.bot.autoreload_time = 10

        result = self.bot._handle_status(status, listener)

        self.assertEqual(self.bot.autoreload_time, self.bot.autoreload_original)

    def test_handle_status_send_message_failure(self):
        status = "E:100 | Internal"
        listener = "__meowerbot__send_message"

        with self.assertRaises(RuntimeError):
            self.bot._handle_status(status, listener)

import unittest
from unittest.mock import MagicMock
from MeowerBot import Bot

class TestBotRun(unittest.TestCase):
    def setUp(self):
        self.bot = Bot()
        self.bot._t_ping_thread = MagicMock()
        self.bot.logger = MagicMock()
        self.bot.api = MagicMock()
        self.bot.wss = MagicMock()

    def test_run_sets_username_and_password(self):
        self.bot.run("testuser", "testpassword")

        self.assertEqual(self.bot.username, "testuser")
        self.assertEqual(self.bot._password, "testpassword")

    def test_run_starts_ping_thread(self):
        self.bot.run("testuser", "testpassword")

        self.bot._t_ping_thread.start.assert_called_once()

    def test_run_sets_prefix_if_none(self):
        self.bot.run("testuser", "testpassword")

        self.assertEqual(self.bot.prefix, "@testuser")

    def test_run_sets_logger_in_to_true(self):
        self.bot.run("testuser", "testpassword")

        self.assertTrue(self.bot.logger_in)

    def test_run_sets_logger_name(self):
        self.bot.run("testuser", "testpassword")

        self.assertEqual(self.bot.logger.name, "MeowerBot testuser")

    def test_run_sets_server(self):
        self.bot.run("testuser", "testpassword", server="wss://testserver.com")

        self.assertEqual(self.bot.server, "wss://testserver.com")

    def test_run_calls_wss_client_with_server(self):
        self.bot.run("testuser", "testpassword", server="wss://testserver.com")

        self.bot.wss.client.assert_called_once_with("wss://testserver.com")

    def test_run_raises_exception_if_bad_exit(self):
        self.bot.bad_exit = True

        with self.assertRaises(BaseException):
            with patch("print", MagicMock()):
                self.bot.run("testuser", "testpassword")


if __name__ == '__main__':
    unittest.main()