import os
import urllib

from setuptools import setup, Command

class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import sys,subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)

setup(
    name='blitzem',
    version='0.1.0',
    author='Richard North',
    author_email='rich.north@gmail.com',
    packages=['blitzem','blitzem.test'],
    license='BSD',
    long_description=open('README.rst').read(),
    install_requires=[
        "apache_libcloud == 0.7.1",
        "paramiko == 1.7.7.1",
    ],
    entry_points = {
        'console_scripts': [
            'blitzem = blitzem.console:main',
        ],
    },
    test_suite = "blitzem.test"
)
