.. _extras:

############
Extra Things
############

This file is meant to say a few extra things that are to small to be in other files

---------
debugging
---------

MeowerBot.py uses `logging` as its logger. Its a standard practice to log to a file and stdout (standard out).

.. code-block:: python

    import logging
    
    logging.basicConfig(
            level=logging.DEBUG,
            handlers=[
                    logging.FileHandler("debug.log", encoding='utf8'),
                    logging.StreamHandler()
            ]
    )
    
    # websockets spams alot more stuff, so its disabled.
    logging.getLogger("websockets.client").setLevel(logging.INFO)

You can also use the :ref:` error` callback to send a message on error, but you dont get the command that caused the error.

------------
The Help Cog
------------

The help cog is a cog that adds a `help` command to your bot. It is a standard practice to load that cog into bots.

.. code-block:: python
        
        from MeowerBot.ext.help import Help
        
        bot.register_cog(Help())

-------------
The websocket
-------------

MeowerBot.py uses a custom `websockets.client` wrapper. The bot class subclasses it.

The exported interfaces are:

- :meth:`MeowerBot.cl.Client.sendPacket`

everything there except :meth:`MeowerBot.cl.Client.sendPacket` is not considered public; Because of that, it can be changed at any time.

-------------------
Publishing your bot
-------------------


The best way to publish a meower bot is to put it on the `meower community organization <https://github.com/meower-community/>`_ as people can audit the code, helping with finding issues, and rule breaks before they ever occur.
