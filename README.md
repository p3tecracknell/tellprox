tellprox
========

A local server to use in place of Tellstick Live. Based on remotestick-server (https://github.com/pakerfeldt/remotestick-server)


Installation
============

Make sure TelldusCenter is installed (TelldusCore.dll is needed for Windows)

Ensure Python is installed and setup (tested on Python 2.7 only).
All settings are contained within config.ini

cd~
sudo apt-get install python-cherrypy3 python-bottle python-oauth python-configobj
git clone git://github.com/p3tecracknell/telldus-py.git
cd telldus-py
sudo python setup.py install
cd ..
git clone git clone git://github.com/p3tecracknell/tellprox.git
cd tellprox
sudo python -m tellprox
