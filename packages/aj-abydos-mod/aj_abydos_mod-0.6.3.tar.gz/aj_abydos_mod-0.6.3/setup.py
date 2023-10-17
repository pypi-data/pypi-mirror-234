# Copyright 2014-2020 by Christopher C. Little.
# This file is part of Abydos.
#
# Abydos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Abydos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Abydos. If not, see <http://www.gnu.org/licenses/>.

"""setup.py.

setuptools configuration file for Abydos
"""
import importlib
import os
from codecs import open
from os import path
from pathlib import Path

from setuptools import find_packages, setup

HERE = Path(path.abspath(path.dirname(__file__)))

__package_name__ = 'abydos'
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def import_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_version(package_name):
    version = import_file('version',
                          os.path.join(__location__, package_name, 'version.py'))
    return version.__version__


__version__ = get_version(__package_name__)


def readfile(fn):
    return (HERE / fn).read_text(encoding='utf8')


def read_requirements(reqs_path):
    with open(reqs_path, encoding='utf8') as f:
        reqs = [line.strip() for line in f
                if not line.strip().startswith('#') and not line.strip().startswith('--')]
    return reqs


def get_extra_requires(path, add_all=True, ext='*.txt'):
    main_reqs = read_requirements(HERE / 'requirements.txt')

    extra_deps = {}
    for filename in path.glob(ext):
        # convention of naming requirements files: requirements.{module}.txt
        package_suffix = filename.suffixes[-2].strip('.')
        reqs = list({*main_reqs, *read_requirements(filename)})
        extra_deps[package_suffix] = reqs

    if add_all:
        extra_deps['all'] = set(vv for v in extra_deps.values() for vv in v)
    return extra_deps

try:
    from setuptools import Extension
    from Cython.Build import cythonize
    use_cython = True
except ImportError:
    use_cython = False

if use_cython:
    ext_modules = cythonize([Extension('abydos.distance.affinegap', ['abydos/distance/affinegap.pyx']),
                             Extension('abydos.distance.cython_affine', ['abydos/distance/cython_affine.pyx'])])
else:
    ext_modules = [Extension('abydos.distance.affinegap', ['abydos/distance/affinegap.c']),
                   Extension('abydos.distance.cython_affine', ['abydos/distance/cython_affine.c'])]

setup(
    name='aj_abydos_mod',
    packages=find_packages(exclude=['tests*']),
    version=__version__,
    description='Fork of the Abydos NLP/IR library',
    author='Christopher C. Little',
    author_email='chrisclittle+abydos@gmail.com',
    ext_modules=ext_modules,
    url='https://github.com/anuj1508/abydos',
    download_url='https://github.com/anuj1508/abydos/archive/master.zip',
    keywords=[
        'nlp',
        'ai',
        'ir',
        'language',
        'linguistics',
        'phonetic algorithms',
        'string distance',
    ],
    license='GPLv3+',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or \
later (GPLv3+)',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Text Processing :: Linguistic',
        'Natural Language :: English',
    ],
    long_description_content_type='text/x-rst',
    long_description='\n\n'.join(
        [readfile(f) for f in ('README.rst', 'HISTORY.rst', 'AUTHORS.rst')]
    ),
    python_requires='>=3.8',
    install_requires=read_requirements(HERE / 'requirements.txt'),
    extras_require=get_extra_requires(HERE / 'requirements')
)
