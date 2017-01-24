#RTGraph

A simple Python application for plotting and storing data from a serial port in real time, formatted as [CSV](https://en.wikipedia.org/wiki/Comma-separated_values).
The application uses the [mutliprocessing](https://docs.python.org/3/library/multiprocessing.html) package to allow better usage of the host resources, overcoming limitations such as [GIL](https://docs.python.org/3/glossary.html#term-global-interpreter-lock) in Python.  

##Dependencies
- Python 3 (3.2 or later).
- PySerial.
- Numpy.
- [PyQtGraph](http://www.pyqtgraph.org/).

##Usage
The project is distributed under MIT License. A DOI is attached to the project for citations.

[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.12789.svg)](http://dx.doi.org/10.5281/zenodo.12789)
