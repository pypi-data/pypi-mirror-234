#!/usr/bin/env python
# vi:si:et:sw=4:sts=4:ts=4
# encoding: utf-8

try:
    from setuptools import setup
except:
    from distutils.core import setup

def get_git_version():
    import subprocess
    version = subprocess.check_output(['git', 'describe', '--tags']).decode().strip().replace('-', '.')
    return '.'.join((version.split('.') + ['0'])[:3])

def get_version():
    return '3.0.9' #import os
    import re
    _git = os.path.join(os.path.dirname(__file__), '.git')
    __version = os.path.join(os.path.dirname(__file__), 'ox/__version.py')
    changelog = os.path.join(os.path.dirname(__file__), 'debian/changelog')
    if os.path.exists(_git):
        version = get_git_version()
        if version:
            with open(__version, 'w') as fd:
                fd.write('VERSION="%s"' % version)
            return version
    elif os.path.exists(__version):
        with open(__version) as fd:
            data = fd.read().strip().split('\n')[0]
            version = re.compile('VERSION="(.*)"').findall(data)
            if version:
                version = version[0]
                return version
    elif os.path.exists(changelog):
        f = open(changelog)
        head = f.read().strip().split('\n')[0]
        f.close()
        rev = re.compile('\d+\.\d+\.(\d+)').findall(head)
        if rev:
            return '3.0.%s' % rev[0]
    return '3.0.x'


setup(
    name="ox",
    version=get_version(),
    description="python-ox - the web in a dict",
    author="0x2620",
    author_email="0x2620@0x2620.org",
    url="https://code.0x2620.org/0x2620/python-ox",
    license="GPLv3",
    packages=['ox', 'ox.torrent', 'ox.web'],
    install_requires=['chardet', 'requests'],
    keywords=[
    ],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

