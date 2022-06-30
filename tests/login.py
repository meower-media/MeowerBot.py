from MeowerBot import CantConnectError, Client
from sys import orig_argv as argv

try:
    c = Client(argv[1], argv[2], debug=True, reconect_time=10)

    c.start()
except CantConnectError as e:
    print("we cant connect to meower rn")
    print("original error:", e.__class__.__name__, ":", e)
