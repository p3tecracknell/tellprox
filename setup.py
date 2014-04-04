from setuptools import setup

setup(
	name='tellprox',
	version='0.28',
	author='Pete Cracknell',
	author_email='p3tecracknell@gmail.com',
	packages=['tellprox'],
	include_package_data=True,
	install_requires=[
		'cherrypy',
		'tellcore-py ==1.0.3',
		'werkzeug',
		'beaker',
		'bottle ==0.12.5'],
	url='https://github.com/p3tecracknell/tellprox',
	license='LICENSE.txt',
	description='Python API to replicate Telldus Live',
	long_description=open('README.md').read(),
)