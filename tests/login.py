
from sys import path

path.append("C:\\Users\\mellf\\Desktop\\MeowerBot.py\\")

from src import Client

c = Client("username","password")

c.start()