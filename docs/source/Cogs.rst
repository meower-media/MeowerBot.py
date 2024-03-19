.. _cogs:

####
Cogs
####

Cogs are an advanced feature of MeowerBot.py. They alow you to make & load reuseable commands and callbacks.

--------------
Creating a Cog
--------------

First thing you need to do is import a few things

.. code-block:: python

    from MeowerBot.cog import Cog
    from MeowerBot.command import command, callback # callback is equivelent to listen 
    from MeowerBot import CallbackIds


To create a cog, it is as simple as defining a class. This is the basis for the reuseable part.
Cogs are a singleton object. So when you define them they will only be defined once.

.. code-block:: python

    class YourCogName(Cog): pass

To create a command in a cog, you use the :func:`MeowerBot.command.command` decorator. 
It has the exact same interface as :meth:`MeowerBot.bot.Bot.command`

.. code-block:: python

    from MeowerBot.context import Context
    
    class YourCogName(Cog): 
        @command(name="hello")
        async def hello(ctx: Context):
            await ctx.reply("Hello, World!")


For creating listeners, its slightly more involved as it is done as the class instead of the instance. 
It is stil relitivly simple though, as you can just get the instance.

.. code-block:: python

    class YourCogName(Cog): 
        @callback(CallbackIds.login)
        async def on_login(cls, token: str):
            self = cls.__instance__
            ...

--------------------------
Creating and loading a cog
--------------------------


Creating a cog is easy, as it takes no arguments by default.
Loading it is also easy, as you just call a single function with the cog instance on the bot object

.. code-block:: python

    bot.register_cog(YourCogName())

:ref:`extras`