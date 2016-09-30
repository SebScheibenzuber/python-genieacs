from setuptools import setup
from os import path
from io import open

readme_path = path.join(path.abspath(path.dirname(__file__)), 'README.txt')
long_description = open(readme_path, encoding='utf-8').read()

setup(
 	name = 'genieacs',

	version = '0.1.7',

	description = 'A Python API to interact with the GenieACS REST API, but with the easiness and comfort of Python.',
	long_description = long_description,

	url = 'https://github.com/SebScheibenzuber/python-genieacs',
	download_url = 'https://github.com/SebScheibenzuber/python-genieacs/tarball/0.1',

	author = 'Oliver Kraitschy',
	author_email = 'okraitschy@tdt.de',

	license = 'GNU General Public License v2',

	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
    	'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    	'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
		'Natural Language :: English',
    	'Operating System :: OS Independent',
		'Topic :: Software Development :: Libraries :: Python Modules',
    ],

	keywords = 'genieacs API REST'

	packages = ['genieacs'],

    package_data = {
        'genieacs': ['data/example.py', 'data/LICENSE.txt', 'data/README.md']
    },

	install_requires = ['requests'],

)
