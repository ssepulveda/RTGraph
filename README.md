#RTGraph

A simple and lightweight Python application for plotting data from the output of a program.
The application uses mutliprocessing to allow better performance using different process for each task.

This code is a fork of https://github.com/ssepulveda/RTGraph.

## Operation
The program reads the standard output of the specified script. It expects the format:
[timestamp (int)]\t[val 0]\t... [val 511]\t

Each line represents a series of acquired values. These values are represented as a 2D matrix using reshape()
In integration mode, a ring buffer is used. It integrates over a certain number of acquisition and displays their sum.

##Dependencies
- Python 3 (3.4 or later).
- Numpy.
- PyQt4.

###Manual Installing

##Usage
The project is distributed under MIT License. A DOI is attached to the project for citations.

Link to the the source repository documentation:
[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.12789.svg)](http://dx.doi.org/10.5281/zenodo.12789)
