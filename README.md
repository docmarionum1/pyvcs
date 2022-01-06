# pyvcs

pyvcs (Python Video Computer System) is a fantasy console inspired by the Atari VCS (2600), written
in Python and developed using Python.

## Setup

1. Install the pyvcs-python interpreter following the instructions in the
[pyvcs-python](https://github.com/docmarionum1/pyvcs-python) repo.
1. Once pyvcs-python is installed and working, follow the platform-specific instructions to setup a
virtual env and install the required dependencies.

For the following commands substitute these with your actual paths:

- `path_to_pyvcs-python` is where you cloned the `pyvcs-python` repository
- `path_to_virtual_env` is a new directory to create a virtual env for `pyvcs-python`
- `path_to_pyvcs` is where you cloned this repository

### Windows

From PowerShell run:

```bash
<path_to_pyvcs-python>\PCBuild\amd64\python.exe -m venv <path_to_virtual_env>
<path_to_virtual_env>\Scripts\activate
pip install -r <path_to_pyvcs>\requirements.txt
```

### Ubuntu (Untested)

From bash run:

```bash
<path_to_pyvcs-python>/python -m venv <path_to_virtual_env>
source <path_to_virtual_env>/bin/activate
pip install cython
pip install --no-binary :all: --upgrade cffi==1.14.6 --no-use-pep517
pip install --no-binary :all: -U numpy==1.21.2 --no-use-pep517
pip install -r <path_to_pyvcs>/requirements.txt
```
### Fedora

From bash run:

```bash
<path_to_pyvcs-python>/python -m venv <path_to_virtual_env>
pip install cython
pip install --no-binary :all: --upgrade cffi==1.14.6 --no-use-pep517
pip install --no-binary :all: -U numpy==1.21.2 --no-use-pep517
pip install -r <path_to_pyvcs>/requirements.txt
```
### Mac (Untested)

From bash run:

```bash
<path_to_pyvcs-python>/python.exe -m venv <path_to_virtual_env>
source <path_to_virtual_env>/bin/activate
pip install cython
pip install --no-binary :all: --upgrade cffi==1.14.6 --no-use-pep517
OPENBLAS="$(brew --prefix openblas)" pip install --no-binary :all: -U numpy==1.21.2 --no-use-pep517
pip install -r <path_to_pyvcs>/requirements.txt
```

## Running games with pyvcs

With your pyvcs virtual env active, run a game with the following:

```bash
python <path_to_pyvcs>/pyvcs.py <path_to_game>
```

For example:

```bash
python <path_to_pyvcs>/pyvcs.py <path_to_pyvcs>/examples/game.py
```


## Examples

The `examples` directory has example games and examples for specific features.

- `game.py` - Contains a full example game Shꚙter.
[Here is video](https://www.youtube.com/watch?v=rapFVHA_rxA) of how it should run.
- `colors.py` - Basic graphics and timing demo
- `colors_unrolled.py` - unrolls the loop to fit more transitions into each line
- `font.py` - Demo of build-in text display functionality
- `audio.py` - Demo of the built-in audio functionality
