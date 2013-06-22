tellprox
========

A local server to use in place of Tellstick Live. Based on remotestick-server (https://github.com/pakerfeldt/remotestick-server)

All settings are contained within config.ini

Requirements
============
You will need telldus-core. On Windows it comes with TelldusCenter:
http://www.telldus.se/products/nativesoftware

There are instructions online for installing telldus-core on Mac/Linux. For example, to install on Raspbian:
http://elinux.org/R-Pi_Tellstick_core

Windows Dependancies
====================
Python for Windows (source needed)

http://www.pip-installer.org/en/latest/installing.html

Use pip to install python module dependancies:

pip install cherrypy configobj bottle

Windows Installation
====================

Download the source and unzip.

In a command prompt, change to the telldus-py folder and run:

python setup.py install

Change to the  root of the project and run:

python -m tellprox

Use pip install [module] for any missing modules

Linux Installation
==================

cd ~

sudo apt-get install python-cherrypy3 python-bottle python-oauth python-configobj git

git clone --recursive git://github.com/p3tecracknell/tellprox.git

cd tellprox/telldus-py/

sudo python setup.py install

cd ..

sudo python -m tellprox
