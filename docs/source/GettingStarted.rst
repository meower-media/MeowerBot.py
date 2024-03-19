.. _gettingstarted:

###############
Getting Started
###############


.. _MeowerBot.py: https://github.com/Meower-Community/MeowerBot.py/ 


`MeowerBot.py`_ is a library for making Meower Bots with python \<3.12. This guide will tell you how everything works. It is also a guide for setting up a bot

--------------------------
Installing `MeowerBot.py`_
--------------------------

Installing the library is the first step.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Checking your Python version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: shell

    showierdata9978@fedora:~$ python --version

It should say something like this when you run the command

.. code-block:: 

    Python 3.12.2

If it doesn't, then you need to update your python version.

^^^^^^^^^^^^^^^^^^^^^^
Installing the library
^^^^^^^^^^^^^^^^^^^^^^

Installing `MeowerBot.py`_ is easy, as it is on pypi.

It is as simple as running

.. code-block:: shell

    showierdata9978@fedora:~$ python3.12 -m pip install MeowerBot

You can check the version of `MeowerBot.py`_ by running this python script

.. code-block:: python

    from MeowerBot import __verson__

    print(__version__)

:ref:` creatingabot`