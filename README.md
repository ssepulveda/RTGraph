# RTGraph

A simple Python application for plotting and storing data from a serial port in real time, formatted as [CSV](https://en.wikipedia.org/wiki/Comma-separated_values).
The application uses the [mutliprocessing](https://docs.python.org/3/library/multiprocessing.html) package to allow better usage of the host resources, overcoming limitations such as [GIL](https://docs.python.org/3/glossary.html#term-global-interpreter-lock) in Python.  

## Dependencies
- Python 3 (3.2 or later).
- PyQt5.
- PySerial.
- [PyQtGraph](http://www.pyqtgraph.org/).

## Installation instructions
### Using Anaconda or Miniconda (Windows, macOS, Linux)
1. Install [Anaconda](https://www.continuum.io/downloads) or [Miniconda](https://conda.io/miniconda.html). Remember to add conda to your path.
2. Open a terminal and type:
    - `conda install pyqtgraph pyserial`

### Using Pip (Windows, macOS, Linux)
1. Verify you have installed pip.
2. Open a terminal and type:
    - `pip install PyQt5 pyqtgraph pyserial`

### Linux (Apt based distros)
1. Open a terminal and type:
    - `sudo apt-get install python3-pyqt5 python3-pyqtgraph python3-serial`

## Usage
From a terminal, on the root folder of the project, run:
- `python -m rtgraph`

## Links
- [Visualizing Physiological Signals in Real Time. SciPy 2015](https://www.youtube.com/watch?v=yNOJ_NfzI64&index=1&list=PLiOqvn0zxKhOy6WKGYMz3wHxJRN_zGCvD&t=896s)
- [Visualizing physiological signals in real-time](http://conference.scipy.org/proceedings/scipy2015/pdfs/sebastian_sepulveda.pdf)

## License and Citations
The project is distributed under MIT License. A DOI is attached to the project for citations.
[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.12789.svg)](http://dx.doi.org/10.5281/zenodo.12789)
