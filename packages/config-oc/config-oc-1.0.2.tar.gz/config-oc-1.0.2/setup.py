from setuptools import setup

with open('README.md', 'r') as oF:
	long_description=oF.read()

setup(
	name='config-oc',
	version='1.0.2',
	description='Handles loading loading configuration files based on hostname',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://ouroboroscoding.com/config/',
	project_urls={
		'Documentation': 'https://ouroboroscoding.com/config/',
		'Source': 'https://github.com/ouroboroscoding/config-python',
		'Tracker': 'https://github.com/ouroboroscoding/config-python/issues'
	},
	keywords=['config', 'configuration', 'host specific configuration'],
	author='Chris Nasr - Ouroboros Coding Inc.',
	author_email='chris@ouroboroscoding.com',
	license='MIT',
	packages=['config'],
	python_requires='>=3.10',
	install_requires=[
		'jsonb>=1.0.0,<1.1',
		'tools-oc>=1.2.2,<1.3'
	],
	zip_safe=True
)