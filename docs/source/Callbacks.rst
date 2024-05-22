.. _callbacks:

#########
Callbacks
#########


Callbacks in MeowerBot.py are a way to configure what the bot does when a specific event in Meower happens (ie someone sends a message or logs in & out)

There are 2 ways to do callbacks in MeowerBot.py, both are in :py:class:`MeowerBot.Bot`.

------------------------
The first Method: Events
------------------------


This method replaces the original bot functionality. By replacing it you can add extra conditions, or even removing that functionality entirely.

it is done with :meth:`MeowerBot.Bot.event` It has no arguments that you can pass in, as it is a raw decorator. The only important part is the name of the function it is decorating. (and that the function is asynchronous)

----------------------------
The second Method: Listeners
----------------------------


This method is basically the same as events. The only diffrence is it takes 1 argument (of type :class:`MeowerBot.CallBackIds`).
The function it uses is :meth:`MeowerBot.Bot.listen`.

-------------------------------
Callback specific documentation
-------------------------------

There are a plethera of callbacks in MeowerBot.py!. This part of the docs explains all of them, and their intended purpose.

All callbacks for this area use the first method.

=======
message
=======


This callback is fired when a meower user sends a post in any chat the bot user is a user of. 
It uses one argument of type :class:`MeowerBot.context.Post`.

.. code-block:: python


    from MeowerBot.context import Post
    
    @bot.event
    async def message(message: Post):
        message = await bot.handle_bridges(message) # Allows discord users to use your bot (Discord uses a special format for sending posts to meower, so this normalises it)
    
        # checks if the start of the message starts with your prefix
        if not message.data.startswith(self.prefix):
            return
    
        # removes the prefix from the command 
        message.data = message.data.removeprefix(self.prefix)
    
        # trys to run the a command, fails if a command is not in the message.
        await bot.run_commands(message)

=====
error
=====

.. _error:

The error callback is fired when any non :py:exc:`BaseExeption` is raised in a bot controlled environment (incl. Callbacks & Commands)

The error callback takes exactly one argument. It is the exception object that was raised, and substantially caught.

.. code-block:: python

    import traceback
    
    @bot.event
    async def error(err: Exception):
        print(traceback.print_exc())
    
===========
\_\_raw\_\_
===========

.. _raw:

This callback is called every single time a packet is recieved by the bot, 
and therfore it is spammed. It takes a single :py:data:`dict` as an argument. 
More docs on what this can contain can be found on `the meower server documentation <https://docs.meower.org>`_

.. code-block:: python

    @bot.event
    async def __raw__(packet: dict):
        if "post_origin" in packet["val"]:
            print("Packet is a Post!")

=====
login
=====


The login callback is called when the bot is connected 
& logged into the meower websocket. 
The only argument that the callback takes is the bot's session token, which is a string.

.. code-block:: python

    @bot.event
    async def login(token: str):
        # You are not allowed to send a startup message in home. You can send a 
        # startup message anywhere else though!
        await bot.get_chat("livechat").send_msg(f"Hello, World! I am {bot.username}")
    

==========
disconnect
==========


This callback is called when the bot disconnects from the websocket. 
When it happens, the bot cannot receve new posts from meower, 
but it can still send messages. Do not rely on that feature though, as the meower server could be offline.

.. code-block:: python

    @bot.event
    async def disconnect():
        print("Disconnected from the meower Websocket!")

=====
ulist
=====


Ulist, otherwise known as userlist, is a callback that gets called when any user connects or disconnects from the meower websocket. 
The only argument is a list of strings signifing the currently online users.

.. code-block:: python
    
    @bot.event
    async def ulist(userlist: list[str]):
        print(f"Currently online users: {", ".join(*userlist)}")

===========
raw_message
===========
It takes a single dictinary, 
and the layout of this dictinary is the raw form of a post,
which can be found in the `the meower server documentation <https://docs.meower.org>`_

.. code-block:: python

    @bot.event
    async def raw_message(post: dict):
        print(f"{post["u"]}: {post["p"]}") # Username: Message
    
======
direct
======


This callback is a less spammed version of :ref:` raw`. As it only gets called when meower sends a custom command like chat states. 
It works exactly the same as :ref:` raw`, just 1 val deep

==========
statuscode
==========

Statuscode is a callback that gets called when meower receves, and proccessses a command sent from the websocket connection. 
The only argument is the statuscode & listener used for it.

.. code-block:: python

    @bot.event
    async def statuscode(code, listener):
        print(f"I got '{code}' for listener '{listener}'")
    
:ref:` cogs`