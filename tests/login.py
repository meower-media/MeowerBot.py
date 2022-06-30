

from MeowerBot import Client,CantConnectError

try:
    c = Client("ShowierDataTest","",debug = False, reconect_time= 10)

    c.start()
except CantConnectError as e:
    print("we cant connect to meower rn")
    print("original error:",e.__class__.__name__,":", e)
