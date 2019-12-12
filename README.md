# RetroUFO
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-yellow.svg)](https://www.youtube.com/watch?v=NLGoKxh8Aq4)
[![Python Version](https://img.shields.io/pypi/pyversions/Django.svg)](https://www.python.org/downloads/) [![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://opensource.org/licenses/MIT) [![PyPI version](https://badge.fury.io/py/RetroUFO.svg)](https://pypi.org/project/RetroUFO/)

A ~~messy~~ Python script that grabs the latest version of every libretro core from the [build bot](https://buildbot.libretro.com/).  

***

### Installation

The package can be installed via pip:

```bash
python -m pip install --user RetroUFO
```


### Usage-CLI

Just run the script from the terminal:

```bash
RetroUFO
```

It will then download and extract all the latest versions of each core to their default location based on `retroarch.default.cfg` for each platform  
_(Which is only Linux, macOS, & Windows for right now)_

If you are more of a advance user, and want to do things a bit more manually, you can view all the scripts arguments by:
```bash
RetroUFO --help
```

### Usage-GUI

The GUI script uses [Qt for Python](https://wiki.qt.io/Qt_for_Python) ([PySide2](https://pypi.org/project/PySide2/)). So you can make sure you have that package installed if you plan to run the script manually:  
```bash
python -m pip install --user PySide2
```


After that you can just run the script like so:
```bash
RetroUFO-GUI
```

You can then just click the `Grab Cores` button at the bottom and then you should be all set.

![](screenshots/grab_cores.gif)

If you would like to grab cores for a different platform or architecture you can override which supported cores it grabs.

![](screenshots/custom_platform.gif)

If you have your core directory set somewhere special you can override where the cores extract to.

![](screenshots/custom_location.gif)

***
### TO-DO

- Set where cores are downloaded
- Real error handling
- Support for ARM detection
- Download progress bar
- Join the code base between the CLI & GUI
- ~~Set where cores are extracted for RA Usage~~
- ~~Choose which architecture you are downloading format~~
- ~~Choose what platform you are downloading format~~
- ~~Auto detect platform & architecture~~
- ~~Keep downloaded archives~~
- ~~Make GUI~~
- ~~Make a PyPi package~~
