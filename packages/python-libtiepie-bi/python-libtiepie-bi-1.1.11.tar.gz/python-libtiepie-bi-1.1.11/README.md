# python-libtiepie
[![PyPI](https://img.shields.io/pypi/v/python-libtiepie-bi.svg)](https://pypi.org/project/python-libtiepie-bi/)
[![License](https://img.shields.io/github/license/hennjanssen/python-libtiepie-bi.svg)](LICENSE)

Python bindings for [LibTiePie SDK](https://www.tiepie.com/node/930). The LibTiePie SDK is a library to easily interface with TiePie engineering [USB oscilloscopes](https://www.tiepie.com/node/4). Using the LibTiePie SDK the user has full control over all aspects of the USB oscilloscope and can perform measurements easily on Windows and Linux. Examples for different measurements are available to get started easily.

## Installation on Windows and Linux

To install the Python bindings for LibTiePie on Windows or Linux:

1. Install the Python bindings by executing `pip install python-libtiepie`
    * The required binaries are shipped with the python package (for Windows and Linux).
1. Download the [python-libtiepie examples](https://minhaskamal.github.io/DownGit/#/home?url=https://github.com/TiePie/python-libtiepie/tree/master/examples).
1. Unpack them using an extractor.
1. Connect your [USB oscilloscope](https://www.tiepie.com/node/4).
1. Run an example by executing e.g. `python OscilloscopeBlock.py`

## Examples

See the [examples directory](examples).

**Attention**: With the change from version 0.X.Y to 1.X.Y the examples might not work anymore.
Please take a look for the documentation to implement your own application.

## About this fork

This fork was created to build a python package which contains all the required binaries; for Windows as well as Linux.
There is no need anymore to manually set-up additional package sources under Linux.