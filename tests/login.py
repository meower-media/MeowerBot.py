from sys import orig_argv as argv

from MeowerBot import CantConnectError, Client


c = Client(argv[2], argv[3], debug=True, reconect_time=10)

def on_login():
    c.send_msg("logginedin (test")

try:
    
    c.start()
except CantConnectError as e:
    print("we cant connect to meower rn")
    print("original error:", e.__class__.__name__, ":", e)
