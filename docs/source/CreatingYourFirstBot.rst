.. _creatingabot:

#######################
Creating your First Bot
#######################

.. role:: python(code)
   :language: python

Creating a bot in MeowerBot.py is relatively simple.

The first thing you need to do is import the bot class.


.. code-block:: python

    from MeowerBot import Bot


Then create the bot. The bot class has a very important option. It is the prefix. It is None by default, but will be auto filled in by MeowerBot.py to `@{BOT_USERNAME}`.

.. note::
    Replace `BOT_USERNAME` with your bot's username

.. code-block:: python

    bot = Bot(prefix=f"@{BOT_USERNAME}")



After creating the bot, You can create commands for it. :meth:MeowerBot.Bot.command . It is a wrapped decorator function (a decorator that is wrapped as to pass extra arguments)

The arguments  are:

    - `name` which is a string, and defaulting to the function name
    - `args` which is an integer, defaulting to `0`. The default signifies unlimited arguments.
    - `aliases` which is an optional list of strings (`Optional[List[str]]`), defaulted to None
    - The function that command decorated needs to follow a basic structure to function. (depending on number of arguments)
  
.. code-block:: python
    
    from MeowerBot.context import Context
    
    # Creating a command that sends a ping to your pong
    @bot.command(name="ping", args=0)
    async def ping(ctx: Context): # Context is a class that wraps sending messages, and getting information about when the command was invoked
        await ctx.reply("Pong!") # sends Pong! to the chat the command was called from


The command name is how a user of your bot will use the command. It would go something like this.

- User1: @bot ping
- Bot: Pong!

For you to finish off your basic bot, you need to make the bot login. It is necessary to place this at the bottom of your main file, as it is a blocking function.

.. caution:: 
    It is also recommended to not put your password right in the source code,
    as that could lead to it getting leaked. For that reason you should use `python-dotenv <https://pypi.org/project/python-dotenv/>`_

    USERNAME And PASSWORD should be replaced with your username as password respectfully.

.. code-block:: text
    :name: env
    :caption: .env

    MEOWER_USERNAME="USERNAME"
    MEOWER_PASSWORD="PASSWORD"

.. code-block:: python
    
    from os import environ as env
    from dotenv import load_dotenv
    
    load_dotenv()
    
    bot.run(env["MEOWER_USERNAME"], env["MEOWER_PASSWORD"])

:ref:` callbacks`