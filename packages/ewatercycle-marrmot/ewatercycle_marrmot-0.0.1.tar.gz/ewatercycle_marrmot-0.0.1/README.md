# eWaterCycle plugin for MARRMoT hydrological model

[![Research Software Directory Badge](https://img.shields.io/badge/rsd-00a3e3.svg)](https://www.research-software.nl/software/ewatercycle-marrmot)

MARRMoT plugin for [eWatercycle](https://ewatercycle.readthedocs.io/).

MARRMoT documentation at https://github.com/wknoben/MARRMoT .

## Installation

eWaterCycle must be installed in a [mamba](https://conda-forge.org/miniforge/) environment. The environment can be created with

```console
wget https://raw.githubusercontent.com/eWaterCycle/ewatercycle/main/environment.yml
mamba env create --name ewatercycle-marrmot --file environment.yml
conda activate ewatercycle-marrmot
```

Install this package alongside your eWaterCycle installation

```console
pip install ewatercycle-marrmot
```

Then MARRMoT models become available as eWaterCycle models

```python
from ewatercycle.models import MarrmotM01, MarrmotM14
```

## Usage

Example notebooks:

* Forcing generation at [docs/generate_forcing.ipynb](https://github.com/eWaterCycle/ewatercycle-marrmot/tree/main/docs/generate_forcing.ipynb)
* Marrmot Collie River 1 (traditional bucket) model [docs/MarrmotM01.ipynb](https://github.com/eWaterCycle/ewatercycle-marrmot/tree/main/docs/MarrmotM01.ipynb)
* Marrmot Top Model hydrological model [docs/MarrmotM14.ipynb](https://github.com/eWaterCycle/ewatercycle-marrmot/tree/main/docs/MarrmotM14.ipynb)

## License

`ewatercycle-marrmot` is distributed under the terms of the [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html) license.
