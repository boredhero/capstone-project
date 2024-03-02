# Instance
## A game about subjective experiences of mental health issues

My DNID Capstone Project

### How to run the game?

Packaging is not ready at this time.
Please set up python + pipenv. Run `pipenv install` and `pipenv shell` from inside of the repository after cloning
`python3 instance.py` to run the game

Instructions for setting up pipenv: https://thinkdiff.net/how-to-use-python-pipenv-in-mac-and-windows-1c6dc87b403e

### How to build an installable package?

NOTE: At this time, only Arch Linux is supported; more options will be coming soon
NOTE: Due to limitations with pyinstaller, you must be ON the platform you wish to build for
NOTE: If you have not done the `pipenv` setup as described above, you will be unable to build

* To build, after being sure to have considered the above 3 warnings, `pipenv run buildscript.py`

### License

GPLv3, see LICENSE file