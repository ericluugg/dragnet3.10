#!/usr/bin/env python

# Copyright (c) 2012 SEOmoz
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os.path
import platform
from setuptools import setup
# have to import `Extension` after `setuptools.setup`
from distutils.extension import Extension
import sys

from Cython.Distutils import build_ext
from Cython.Build import cythonize
import lxml
from numpy import get_include

def find_libxml2_include():
    include_dirs = []
    for d in ['/usr/include/libxml2', '/usr/local/include/libxml2']:
        if os.path.exists(os.path.join(d, 'libxml/tree.h')):
            include_dirs.append(d)
    return include_dirs

# set min MacOS version, if necessary
if sys.platform == 'darwin':
    os_version = '.'.join(platform.mac_ver()[0].split('.')[:2])
    # this seems to work better than the -mmacosx-version-min flag
    os.environ['MACOSX_DEPLOYMENT_TARGET'] = os_version

ext_modules = [
    Extension('dragnet.lcs',
              sources=["dragnet/lcs.pyx"],
              include_dirs=[get_include()],
              language="c++"),
    Extension('dragnet.blocks',
              sources=["dragnet/blocks.pyx"],
              include_dirs=(lxml.get_include() + find_libxml2_include()),
              language="c++",
              libraries=['xml2']),
    Extension('dragnet.features._readability',
              sources=["dragnet/features/_readability.pyx"],
              include_dirs=[get_include()],
              extra_compile_args=['-std=c++11'],
              language="c++"),
    Extension('dragnet.features._kohlschuetter',
              sources=["dragnet/features/_kohlschuetter.pyx"],
              include_dirs=[get_include()],
              language="c++"),
    Extension('dragnet.features._weninger',
              sources=["dragnet/features/_weninger.pyx"],
              include_dirs=[get_include()],
              language="c++"),
]

setup(
    name='dragnet',
    version='2.1.0',
    description='Extract the main article content (and optionally comments) from a web page',
    author='Matt Peters, Dan Lecocq',
    author_email='matt@moz.com, dan@moz.com',
    url='http://github.com/seomoz/dragnet',
    license='MIT',
    platforms='Posix; MacOS X',
    keywords='automatic content extraction, web page dechroming, HTML parsing',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    packages=['dragnet', 'dragnet.features'],
    package_dir={'dragnet': 'dragnet', 'dragnet.features': 'dragnet/features'},
    package_data={'dragnet': ['pickled_models/*/*']},
    cmdclass={'build_ext': build_ext},
    ext_modules=cythonize(ext_modules, compiler_directives={'language_level': "2"}),
    install_requires=[
        'Cython>=3.0.0',
        'ftfy>=4.1.0',
        'lxml',
        'numpy<=1.26.3',
        'scikit-learn<=1.2.2',
        'scipy>=0.17.0',
    ]
)
