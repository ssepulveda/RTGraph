#RTGraph

A simple and lightweight Python application for plotting data from a serial port, ouputed as CSV.
The application uses mutliprocessing to allow better performance using different process for each task.


##Dependencies
- Python (2.7.x).
- PySerial.
- Numpy.
- PyQt4.
- [PyQtGraph](http://www.pyqtgraph.org/).

###Manual Installing

#### Ubuntu / Debian based distributions
- The basic dependencies can be installed with ```sudo apt-get install python python-pip python-serial numpy python-qt4```.
- Then, install the pyqtgraph library with ```sudo pip install pyqtgraph```.
- To modify the UI aspect, install ```sudo apt-get install pyqt4-dev-tools qt4-designer```.

#### Windows
- Download and install [Python 2.7.x](https://www.python.org/downloads/windows/), make sure to install include pip (by default) and the add the binary to the path (not enabled by default).
- Download and install [Microsoft Visual C++ Compiler for Python 2.7](http://aka.ms/vcpython27) needed for compiling numpy.
- Download and install [PyQt4](http://www.riverbankcomputing.com/software/pyqt/download) binary packages for installing PyQt4 on Python 2.7.x for your appropiate architecture.
- Open a command window and install the missing dependencies, ```pip install pyserial numpy pyqtgraph```.

#### Mac OS
- See general

### General
- Download and install [Anaconda Scientific Python Distribution](https://store.continuum.io/cshop/anaconda/) for your OS/architecture.
- Install missing dependencies, ```pip install pyserial pyqtgraph```.

##Usage
The project is distributed under MIT License. A DOI is attached to the project for citations.
[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.12789.svg)](http://dx.doi.org/10.5281/zenodo.12789)
