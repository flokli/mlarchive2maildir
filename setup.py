from setuptools import setup

setup(
    name='mlarchive2maildir',
    version='0.0.2',
    description='Imports mail from (pipermail) archives into a maildir',
    install_requires=['bs4', 'requests', 'cleo'],
    tests_require=[],
    packages=['mlarchive2maildir'],
    entry_points={
        'console_scripts': {
            'mlarchive2maildir = mlarchive2maildir.commands:main'
        }
    },
    author='Florian Klink',
    author_email='flokli@flokli.de',
    license='MIT'
)
