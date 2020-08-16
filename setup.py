from distutils.core import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='fakir',
    description='a mildly monadic module for fast faking',
    long_description=long_description,
    author='Derrick W. Turk',
    url='https://github.com/derrickturk/fakir',
    version='0.1',
    py_modules=['fakir'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],
)
