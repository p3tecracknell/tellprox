tellprox
========

A local server to use in place of Tellstick Live. Based on remotestick-server (https://github.com/pakerfeldt/remotestick-server)

Trello: https://trello.com/b/YAE4Zk9h

All settings are contained within config.ini which will be created after the first time the process is stopped.

Requirements
============
You will need telldus-core. On Windows it comes with TelldusCenter:
http://www.telldus.se/products/nativesoftware

There are instructions online for installing telldus-core on Mac/Linux. For example, to install on Raspbian:
http://elinux.org/R-Pi_Tellstick_core

To install Telldus-core on OpenWRT, follow:
http://blog.stfu.se/binary-openwrt-packages-for-telldus-core/

Essentially: opkg install [url]

Installation
============

Make sure python is installed (windows: http://www.activestate.com)

Download the source:

--Windows users, click on 'Download Zip' and extract.

--Linux users should install git and setuptools, for example:

--$sudo apt-get update

--$sudo apt-get install python-setuptools git

--$git clone git://github.com/p3tecracknell/tellprox.git

Then open a command prompt in the source and type:

$sudo python setup.py install

Finally, run with:

$python -m tellprox

Authentication is not set by default. To turn it on set the username and password in the config page
