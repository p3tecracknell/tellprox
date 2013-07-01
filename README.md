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

Installation
============

Make sure python is installed (windows: http://www.activestate.com)

Download the source:

  Windows users, click on 'Download Zip' and extract.

  Linux users should install git and setuptools:

  sudo apt-get install python-setuptools git

  git clone git://github.com/p3tecracknell/tellprox.git

Then open a command prompt in the source and type:

python setup.py install

Finally, run with:

python -m tellprox
