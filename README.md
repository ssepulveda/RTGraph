# RTGraph

A simple Python application for plotting and storing data from a serial port in real time, formatted as [CSV](https://en.wikipedia.org/wiki/Comma-separated_values).
The application uses the [mutliprocessing](https://docs.python.org/3/library/multiprocessing.html) package to allow better usage of the host resources, overcoming limitations such as [GIL](https://docs.python.org/3/glossary.html#term-global-interpreter-lock) in Python.  

## Dependencies
- Python 3 (3.10 or later).
- PyQt6.
- PySerial.
- [PyQtGraph](http://www.pyqtgraph.org/).

## Installation instructions
TODO

## Usage
From a terminal, on the root folder of the project, run:
```python3 rtgraph```

## Development
1. Setup environment and activate it using
    ```
    ```
2. Install QtDesigner
    ```
    pip install pyqt6-tools
    ```
3. Run desginer
    ```
    venv/lib/python3.10/site-packages/qt6_applications/Qt/bin/designer
    ```

## Links
- [Presentation on SciPy 2015](https://www.youtube.com/watch?v=yNOJ_NfzI64&index=1&list=PLiOqvn0zxKhOy6WKGYMz3wHxJRN_zGCvD&t=896s)
- [Proceedings on SciPy 2015](http://conference.scipy.org/proceedings/scipy2015/pdfs/sebastian_sepulveda.pdf)

## License and Citations
The project is distributed under MIT License. A DOI is attached to the project for citations.
[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.12789.svg)](http://dx.doi.org/10.5281/zenodo.12789)
