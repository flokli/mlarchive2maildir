from setuptools import setup, find_packages

setup(
    name='mlarchive2maildir',
    description='Imports mail from (pipermail) archives into a maildir',
    url='https://github.com/flokli/mlarchive2maildir',
    author='Florian Klink',
    author_email='flokli@flokli.de',
    license='MIT',
    use_scm_version={'write_to': 'mlarchive2maildir/version.py'},
    setup_requires=['setuptools_scm'],
    install_requires=[
        'beautifulsoup4',
        'click',
        'click-log',
        'requests',
        'six'
    ],
    tests_require=[],
    packages=find_packages(),
    entry_points={
        'console_scripts': {
            'mlarchive2maildir = mlarchive2maildir.commands:cli'
        }
    },
)
