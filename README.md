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

Python for Windows (http://www.activestate.com)

Click on 'Download Zip' and extract. Open a command prompt, change to the extracted folder and type the following

python setup.py install

Run with:

python -m tellprox


Linux Installation
==================

cd ~

sudo apt-get install python-cherrypy3 python-setuptools git

git clone git://github.com/p3tecracknell/tellprox.git

cd tellprox

sudo python setup.py install

Run with:

python -m tellprox
