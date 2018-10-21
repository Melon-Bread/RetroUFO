# RetroUFO
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20windows-yellow.svg)]()
[![Python Version](https://img.shields.io/pypi/pyversions/Django.svg)](https://www.python.org/downloads/) [![License.](https://img.shields.io/github/license/mashape/apistatus.svg)](https://opensource.org/licenses/MIT)

A ~~messy~~ Python script that grabs the latest version of every libretro core from the [build bot](https://buildbot.libretro.com/).  

***
### Usage

Just run the script with _Python 3_:

```bash
python3 ./RetroUFO.py
```

It will then download and extract all the latest versions of each core to their default location based on `retroarch.default.cfg` for each platform  
_(Which is only Linux & Windows for right now)_

If you are more of a advance user, and want to do things a bit more manually, you can view all the scripts arguments by:
```bash
python3 ./RetroUFO.py --help
```


***
### TO-DO

- Set where cores are downloaded
- ~~Set where cores are extracted for RA Usage~~
- ~~Choose which architecture you are downloading format~~
- ~~Choose what platform you are downloading format~~
- ~~Auto detect platform & architecture~~
- Download progress bar
- ~~Keep downloaded archives~~
- Give better console output
- Real error handling
