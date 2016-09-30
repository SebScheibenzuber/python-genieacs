from setuptools import setup
from os import path
from io import open

#with open(path.join(here, 'README.MD'), encoding='utf-8') as f:
#	long_description = f.read()

setup(
 	name = 'genieacs',

	version = '0.1.5',

	description = 'A Python API to interact with the GenieACS REST API, but with the easiness and comfort of Python.',
#	long_description = long_descritpion,

	url = 'https://github.com/SebScheibenzuber/python-genieacs',
	download_url = 'https://github.com/SebScheibenzuber/python-genieacs/tarball/0.1' ,

	author = 'Oliver Kraitschy',
	author_email = 'okraitschy@tdt.de',

	license = 'GNU General Public License v2',

	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
    	'Programming Language :: Python',
    	'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
		'Natural Language :: English',
    	'Operating System :: OS Independent',
		'Topic :: Software Development :: Libraries :: Python Modules',
    ],

	#keywords = ''

	packages = ['genieacs'],

    package_data = {
        'genieacs': ['data/example.py', 'data/LICENSE.txt', 'data/README.md']
    },

	install_requires = ['requests'],

)
