"""
MeowerBot.py

MIT License

"""

from ._version import __version__

# Public library imports
from . import bot as botm

from .bot import Bot, cbids, CallBackIds

__all__ = ["__version__", "Bot", "botm", "cbids", "CallBackIds"]
