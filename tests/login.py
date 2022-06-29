from MeowerBot import CantConnectError, Client

try:
    c = Client("ShowierDataTest", "")


    c.start()
except CantConnectError as e:
    print("we cant connect to meower rn")
    print("original error:", e)
