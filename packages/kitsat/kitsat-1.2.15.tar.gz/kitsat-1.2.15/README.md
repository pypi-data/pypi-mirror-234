# Kitsat python library and CLI

## Overview

Kitsat python is a Python CLI and library for communicating with the Kitsat educational satellite manufactured by Arctic Astronautics Ltd.

 * Project Homepage: https://github.com/netnspace/Kitsat-Python-Library
 * Download Page: https://test.pypi.org/project/kitsat-python
 * Kitsat Homepage: http://kitsat.fi/
 * Get a Kitsat: https://holvi.com/shop/kitsat/

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install kitsat_python

```bash
pip install kitsat
```

### Additional installation steps

To access the USB port at ie. /dev/ttyS0 on Linux, you might have to add your user to dialout group with this command:
```
sudo usermod -a -G dialout <your_user_name>
```
And log off and on again.

## Usage

This package offers a CLI and a Python library for operating the satellite. The cli can be run from a terminal with the command

```bash
kitsat_cli
```

A list of commands for the cli can be found in the directory [docs](docs)


For using the library, here is a sample script that connects to a satellite on port /dev/ttyACM0, pings the satellite and prints its response. More example scripts can be found in the directory [examples](examples)

```python
from kitsat import Modem

mod = Modem()
mod.connect('/dev/ttyACM0')
mod.write('ping')
print(mod.read())

mod.disconnect()
```

## Contributors
 * Tuomas Simula - <tuomas@simu.la>
 * Tessa Nikander - <tessa@kitsat.fi>
 * Samuli Nyman - <samuli@kitsat.fi>

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0)