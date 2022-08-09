from MeowerBot import CantConnectError, Client


def on_raw_msg(msg: dict, handler):

    print(f'msg: {msg["u"]}: {msg["p"]}')
    if not msg["u"] == c.username:
        if msg["u"] == "Discord":
            msg["u"] = msg["p"].split(":")[0]
            msg["p"] = msg["p"].split(":")[1].strip()
        if msg["p"].startswith(f"@{c.username}"):
            c.send_msg(f'Hello, {msg["u"]}!')


def on_error(e):
    print(e)


try:
    c = Client("ShowierDataTest", "password", debug=True)

    c.callback(on_raw_msg)
    c.callback(on_error)

    c.start()
except CantConnectError as e:
    print("we cant connect to meower rn")
    print("original error: ", e)
