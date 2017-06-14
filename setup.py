from setuptools import setup
from os import path
from MyRuns.version import __version__

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

exec(open('MyRuns/version.py').read())
setup(
    name='MyRuns',
    version=__version__,
    description='A small web app that connects to Strava and calculates your target for the week',
    long_description=long_description,
    author='Angelina Nikiforova',
    url='https://github.com/shakeyapants/MyRuns_stravaAPI',
    author_email='nikiforova.angelina@gmail.com',
    license='MIT',
    keywords=['strava', 'run', 'flask'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Flask',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6'
    ],
    packages=['MyRuns'],
    include_package_data=True,
    install_requires=[
        'stravalib>=0.6.0',
        'Flask>=0.12.1',
        'Flask_SQLAlchemy>=2.2',
        'Flask_login>=0.4.0',
        'SQLAlchemy>=1.1.9',
        'Click>=6.7',
    ],
    entry_points='''
            [console_scripts]
            MyRuns=MyRuns.cli_script:cli
        ''',
    setup_requires=[],
    tests_require=[],
)