# MeowerBot.py

A bot lib for Meower

## How to use

```py

from MeowerBot import Client

c = Client("Username","password",False) 

def on_raw_msg(msg:dict, listener:dict):

        print(f'msg: {msg["u"]}: {msg["p"]}')
        if not msg["u"] == c.username:
            if msg["u"] == "Discord":
                msg["u"] = msg["p"].split(":")[0]
                msg["p"] = msg["p"].split(":")[1].strip() 
            if msg["p"].startswith(f'@{c.username}'):   
                c.send_msg(f'Hello, {msg["u"]}!')

def on_close(exiting:bool):
    ...

def on_error(error):
    ...

def on_login():
    ...

def handle_pvar(pvar:dict, origin:str, var, lisserner):
    ...

def handle_pmsg(msg:dict, origin:str, lissiner):
    ...

def on_status_change(status, isserner):
    c.satuscodee = status

def on_raw_packet(packet:dict, lissener)
    ...

c.callback(handle_pmsg)
c.callback(handle_pvar)
c.callback(on_login)
c.callback(on_close)
c.callback(on_error)
c.callback(on_raw_msg)
c.callback(on_status_change)
c.callback(on_raw_packet)

c.start()
``` 
