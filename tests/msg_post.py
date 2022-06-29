from MeowerBot import CantConnectError, Client


def on_raw_msg(msg: dict):

    print(f'msg: {msg["u"]}: {msg["p"]}')
    if not msg["u"] == c.username:
        if msg["u"] == "Discord":
            msg["u"] = msg["p"].split(":")[0]
            msg["p"] = msg["p"].split(":")[1].strip()
        if msg["p"].startswith(f"@{c.username}"):
            c.send_msg(f'Hello, {msg["u"]}!')


try:
    c = Client("ShowierDataTest", "password")

    c.callback(on_raw_msg)

    c.start()
except CantConnectError as e:
    print("we cant connect to meower rn")
    print("original error: ", e)
