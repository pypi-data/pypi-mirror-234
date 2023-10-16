from setuptools import setup, find_packages

setup(
    name='QDetect',
	description='A library for detecting Quaran verses in any text',
    author='Samhaa El-Beltagy',
    version='0.7',
    packages=find_packages(),
	#packages=['qdetect'],
	include_package_data=True,
    package_data={'': ['dfiles/*']},
	install_requires=['levenshtein==0.12.0'],
	
)
