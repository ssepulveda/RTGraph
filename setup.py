from setuptools import setup, find_packages

import io

import rtgraph


DESCRIPTION = "TODO"


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

LONG_DESCRIPTION = read('README.md')


setup(
    name='RTGraph',
    version=rtgraph.__version__,
    url='http://github.com/ssepulveda/rtgraph/',
    license='MIT',
    author='Sebastian Sepulveda',
    author_email='ssepulveda.sm@gmail.com',
    install_requires=['numpy',
                      'pyserial',
                      'pyqtgraph'],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=['rtgraph'],
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Programming Language :: Python',
        "Programming Language :: Python :: 3",
        'Development Status :: 1 - Beta',
        'Environment :: Other Environment',
        "Intended Audience :: Science/Research",
        "License :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: User Interfaces",
        ]
)
