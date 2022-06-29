
from sys import path

path.append("C:\\Users\\mellf\\Desktop\\MeowerBot.py\\")

from src.MeowerBot import Client

c = Client("ShowierDataTest","password")

c.start()