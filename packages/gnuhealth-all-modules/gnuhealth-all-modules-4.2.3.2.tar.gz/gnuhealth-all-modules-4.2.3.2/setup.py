#!/usr/bin/env python

from setuptools import setup
import configparser
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

config = configparser.ConfigParser()
config.read_file(open('tryton.cfg'))
deps_dict = dict(config.items('tryton'))
for key in ('depends_trytond', 'depends_gnuhealth', 'depends_pip'):
    if key in deps_dict:
        deps_dict[key] = deps_dict[key].strip().splitlines()
requires = []
for dep in deps_dict.get('depends_trytond', []):
    requires.append('%s>=%s,<%s' % (dep, deps_dict.get('trytond_version'), deps_dict.get('trytond_smaller')))
for dep in deps_dict.get('depends_gnuhealth', []):
    requires.append('%s==%s' % (dep, deps_dict.get('gnuhealth_version')))
for dep in deps_dict.get('depends_pip', []):
    requires.append(dep)
setup(
    name='gnuhealth-all-modules',
    version='4.2.3.2',
    description='GNU Health HMIS: Hospital Management Information System',
    long_description=read('README.rst'),
    author='GNU Solidario',
    author_email='health@gnusolidario.org',
    url='https://www.gnuhealth.org',
    project_urls = {
      'Homepage': 'https://www.gnuhealth.org/',
      'Source Code': 'https://gitlab.com/geraldwiese/gnu-health-all-modules-pypi'
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Tryton',
        'Intended Audience :: Developers',
        'Intended Audience :: Healthcare Industry',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        ],
    license='GPLv3+',
    install_requires=requires,
    python_requires=">=3.7, <4",
    packages=['gnuhealth-all-modules'],
    package_dir={'gnuhealth-all-modules': 'gnuhealth-all-modules'},
    package_data={'gnuhealth-all-modules': ['etc/*']}
)
