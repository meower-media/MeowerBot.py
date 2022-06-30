# MeowerBot.py

A bot lib for Meower

## How to use

```py

from MeowerBot import Client

c = Client("Username","password",False) 

def on_raw_msg(msg:dict):

        print(f'msg: {msg["u"]}: {msg["p"]}')
        if not msg["u"] == c.username:
            if msg["u"] == "Discord":
                msg["u"] = msg["p"].split(":")[0]
                msg["p"] = msg["p"].split(":")[1].strip() 
            if msg["p"].startswith(f'@{c.username}'):   
                c.send_msg(f'Hello, {msg["u"]}!')

def on_close():
    ...

def on_error():
    ...

def on_login():
    ...


c.callback(on_login)
c.callback(on_close)
c.callback(on_error)
c.callback(on_raw_msg)


c.start()
```