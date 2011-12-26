import os
import urllib

from distutils.core import setup, Command

# this function borrowed from https://bitbucket.org/wnielson/django-chronograph
def setup_distribute():
    """
    This will download and install Distribute.
    """
    try:
        import distribute_setup
    except:
        # Make sure we have Distribute
        if not os.path.exists('distribute_setup'):
            urllib.urlretrieve('http://nightly.ziade.org/distribute_setup.py',
                               './distribute_setup.py')
        distribute_setup = __import__('distribute_setup')
    distribute_setup.use_setuptools()

# Make sure we have Distribute installed
setup_distribute()

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
    cmdclass = {'test': PyTest},
)
