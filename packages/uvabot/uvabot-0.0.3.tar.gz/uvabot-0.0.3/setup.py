from setuptools import setup, find_packages;

with open('README.md', 'r', encoding='utf-8') as f:
	long_description = f.read();

setup(
	name='uvabot',
	version='0.0.3',
	description='Wrapper for Tradier API',
	long_description = long_description,
	long_description_content_type='text/markdown',
	author='Tom Hammons',
	author_email='qje5vf@virginia.edu',
	url='https://github.com/thammo4/tradier',
	license='Apache-2.0',
	packages=find_packages(),
	install_requires=['requests>=2.25.1', 'pandas>=1.2.4'],
	python_requires='>=3.6'
);
