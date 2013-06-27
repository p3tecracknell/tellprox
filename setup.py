#from distutils.core import setup
from setuptools import setup
import py2exe

setup(
    name='tellprox',
    version='0.23',
    author='Pete Cracknell',
    author_email='p3tecracknell@gmail.com',
    packages=['tellprox'],
    package_data={'tellprox': ['static/css/*.css']},
    install_requires=['cherrypy','tellcore-py'],
    url='https://github.com/p3tecracknell/tellprox',
    license='LICENSE.txt',
    description='Python API to replicate Telldus Live',
    long_description=open('README.md').read(),
)
