from setuptools import setup

with open('README.md', 'r') as oF:
	long_description=oF.read()

setup(
	name='namedredis',
	version='1.0.1',
	description='A library to make sharing the same redis connection easier',
	long_description=long_description,
	long_description_content_type='text/markdown',
	project_urls={
		'Source': 'https://github.com/ouroboroscoding/namedredis',
		'Tracker': 'https://github.com/ouroboroscoding/namedredis/issues'
	},
	keywords=['redis', 'config'],
	author='Chris Nasr - Ouroboros Coding Inc.',
	author_email='chris@ouroboroscoding.com',
	license='MIT',
	packages=['nredis'],
	python_requires='>=3.10',
	install_requires=[
		'config-oc>=1.0.2,<1.1',
		'redis>=5.0.0,<5.1',
		'hiredis>=2.2.3,<2.3',
		'tools-oc>=1.2.2,<1.3'
	],
	zip_safe=True
)