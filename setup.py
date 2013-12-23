from setuptools import setup

setup(
    name='tellprox',
    version='0.26',
    author='Pete Cracknell',
    author_email='p3tecracknell@gmail.com',
    packages=['tellprox'],
    package_data={'tellprox': ['static/css/*.css']},
    install_requires=['cherrypy','tellcore-py','werkzeug'],
    url='https://github.com/p3tecracknell/tellprox',
    license='LICENSE.txt',
    description='Python API to replicate Telldus Live',
    long_description=open('README.md').read(),
)
