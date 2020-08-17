import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='fakir',
    description='a mildly monadic module for fast faking',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Derrick W. Turk',
    author_email='dwt@terminusdatascience.com',
    url='https://github.com/derrickturk/fakir',
    version='0.1',
    packages=setuptools.find_packages(),
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    package_data={'fakir': ['py.typed']},
    zip_safe=False,
)
