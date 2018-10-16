# RetroUFO
[![Platform](https://img.shields.io/badge/Platform-Linux--64-yellow.svg)](https://getfedora.org/en/workstation/download/)
[![Python Version](https://img.shields.io/pypi/pyversions/Django.svg)](https://www.python.org/downloads/) [![License.](https://img.shields.io/github/license/mashape/apistatus.svg)](https://opensource.org/licenses/MIT)

A ~~messy~~ Python script that grabs the latest version of every libretro core from the [build bot](https://buildbot.libretro.com/).  
(As of right now it only downloads the 64-Bit Linux cores)
***
### Usage

Just run the script with _Python 3_:

```bash
python3 ./RetroUFO.py
```

It will then download and extract all the (latest version) of each  core to: `~/.config/retroarch/cores/`
***
### TO-DO

- Set where cores downloaded
- Set where cores are extracted for RA Usage
- Choose which architecture you are downloading format
- Choose what platform you are downloading format
- Download progress bar
- Keep downloaded archives
