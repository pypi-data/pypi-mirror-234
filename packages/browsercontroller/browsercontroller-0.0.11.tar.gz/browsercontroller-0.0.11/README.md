# Selenium Browser Controller for apt Firefox on Ubuntu 22.10

[!\[Python 3.10\]\[python_badge\]](https://www.python.org/downloads/release/python-3106/)
[!\[License: AGPL v3\]\[agpl3_badge\]](https://www.gnu.org/licenses/agpl-3.0)
[!\[Code Style: Black\]\[black_badge\]](https://github.com/ambv/black)
[!\[Code Coverage\]\[codecov_badge\]](https://codecov.io/gh/a-t-0/snnalgos)

Initialises a Selenium browser controller for a specific firefox profile on an
Ubuntu 22.10 system for an `apt` installation of Firefox.

Put into a separate pip package to remove boiler-plate code from other
repositories that control the browser.

## Usage

First install this pip package with:

```
pip install browsercontroller
```

Then run:

```py
from browsercontroller.get_controller import (
    get_ubuntu_apt_firefox_controller,
)

get_ubuntu_apt_firefox_controller(url="https://www.startpagina.nl")
```

## Hide automation/"are u human?"

Some entities use checks to verify you are human. at 20223-09-19 those can be
evaded using either:

- playwright
- puppeteer

## Installation playwright

```sh
pip install playwright
playwright install
```

## Installation puppeteer

```sh
npm install puppeteer
npm install puppeteer-extra-plugin-stealth
npm install puppeteer puppeteer-extra puppeteer-extra-plugin-stealth
# Then run the example script with:
node puppeteer_stealth.js
```

## Drawback playwright implementation

An example of each of those two options is included. One drawback of the way
playwright is used in this repository, is that the entire sequence of actions
must occur within a single method, because the playwright browsercontroller is
created within a Python `with` statement, and returning the `Page` object from
the initialisation function: `initialise_playwright_browsercontroller()` yields
"loop closed error."

## Drawback puppeteer

It is implemented in javascript. Pypeteer is an archived Python approximation
of puppeteer. However, that is limited in its functionalities and not supported anymore.

**Warning:**
Checks whether a `snap` version of Firefox is installed, and if yes, removes it
and installs an `apt` version of Firefox instead. You'll lose browser history,
logins and bookmarks if you don't have an `apt` version of Firefox.

## Updating

Build the pip package with:

```
pip install --upgrade pip setuptools wheel
pip install twine
```

Install the pip package locally with:

```
pip install -e .
```

Upload the pip package to the world with:

```
rm -r dist
rm -r build
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/\*
```
