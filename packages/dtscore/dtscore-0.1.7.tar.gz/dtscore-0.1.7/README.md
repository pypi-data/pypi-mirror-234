# Prep
Project folder structure
```
pyexample
├── LICENSE
├── pyexample
│   ├── __init__.py
│   ├── module_mpi4py_1.py
│   ├── module_numpy_1.py
│   └── module_numpy_2.py
├── README.rst
└── setup.py
```
Tools install
```
pip install setuptools
pip install wheel
pip install twine
```

# Create
 .pypirc file in $home (c:/users/dgsmith) directory<br/>
 ```
[testpypi]
username = __token__
password = token from test.pypi.org goes here
 ```
then under project folder create setup.py
 ```
 from setuptools import setup

setup(
    name='dtscore',
    version='0.1.0',    
    description='DTS core',
    long_description='The core constants library for DTS Python routines.',
    long_description_content_type='text/x-rst',
    url='https://github.com/shuds13/pyexample',
    author='Dale Smith',
    author_email='dg@xxyy.th',
    license='BSD 2-clause',
    packages=['dtscore'],
    install_requires=[],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.5',
    ],
)
 ```

# Create distribution material in dist/
| Command | Result |
| --- | --- |
| python setup.py sdist |<- to setup source distribution<br/> |
| python setup.py bdist-wheel --universal | <- to setup binary distribution, or<br/> |
| python setup.py sdist bdist-wheel | <- to setup source and binary |
| python setup.py check | <- check setup is correct |

## Upload to repo
| Command | Result |
| --- | --- |
| twine upload --repository testpypi dist/* | <- upload to repo |