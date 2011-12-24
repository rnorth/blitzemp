import distribute_setup
distribute_setup.use_setuptools()
from distutils.core import setup

setup(
    name='blitzem',
    version='0.1.0',
    author='Richard North',
    author_email='rich.north@gmail.com',
    packages=['blitzem','blitzem.test'],
    license='BSD',
    long_description=open('README.txt').read(),
    scripts=['scripts/blitzem'],
    install_requires=[
        "apache_libcloud == 0.7.1",
        "paramiko == 1.7.7.1",
    ],
)
