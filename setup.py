from setuptools import setup

setup(
    name='mlarchive2maildir',
    use_scm_version={'write_to': 'mlarchive2maildir/version.py'},
    setup_requires=['setuptools_scm'],
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
