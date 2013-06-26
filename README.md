tellprox
========

A local server to use in place of Tellstick Live. Based on remotestick-server (https://github.com/pakerfeldt/remotestick-server)

All settings are contained within config.ini which will be created after the first time the process is stopped.

Note that the setup.py is not ready yet.

Requirements
============
You will need telldus-core. On Windows it comes with TelldusCenter:
http://www.telldus.se/products/nativesoftware

There are instructions online for installing telldus-core on Mac/Linux. For example, to install on Raspbian:
http://elinux.org/R-Pi_Tellstick_core


Windows Installation
====================

Python for Windows (source needed)

Install CherryPy

http://download.cherrypy.org/cherrypy/3.2.2/CherryPy-3.2.2.win32.exe

Download (this) Tellprox source and unzip.

In a command prompt, change to the tellcore-py folder and run:

python setup.py install

Change to the  root of the project and run:

python -m tellprox


Linux Installation
==================

cd ~

sudo apt-get install python-cherrypy3 git

git clone --recursive git://github.com/p3tecracknell/tellprox.git

Then alternative 1 or 2 below.

Alternative 1
-------------

cd tellprox/tellcore-py/

sudo python setup.py install

cd ..

python -m tellprox

Alternative 2
-------------

cd tellprox

PYTHONPATH=tellcore-py python -m tellprox
