from setuptools import setup

setup(
	name='tellprox',
	version='0.28',
	author='Pete Cracknell',
	author_email='p3tecracknell@gmail.com',
	packages=['tellprox'],
	include_package_data=True,
	install_requires=[
		'CherryPy==3.2.5',
		'Werkzeug==0.9.4',
		'beaker==1.6.4',
		'bottle==0.12.5',
		'configobj==4.7.0',
		'tellcore-py==1.0.3',
		'tellprox==0.28'],
	url='https://github.com/p3tecracknell/tellprox',
	license='LICENSE.txt',
	description='Python API to replicate Telldus Live',
	long_description=open('README.md').read(),
)