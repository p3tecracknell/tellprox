from setuptools import setup

setup(
    name='tellprox',
    version='0.27',
    author='Pete Cracknell',
    author_email='p3tecracknell@gmail.com',
    packages=['tellprox'],
    include_package_data=True,
    install_requires=['cherrypy','tellcore-py','werkzeug','beaker'],
    url='https://github.com/p3tecracknell/tellprox',
    license='LICENSE.txt',
    description='Python API to replicate Telldus Live',
    long_description=open('README.md').read(),
)
