# Hue sunrise

[![pipeline status](https://gitlab.com/marvin.vanaalst/hue-sunrise/badges/main/pipeline.svg)](https://gitlab.com/marvin.vanaalst/hue-sunrise/-/commits/main)
[![coverage report](https://gitlab.com/marvin.vanaalst/hue-sunrise/badges/main/coverage.svg)](https://gitlab.com/marvin.vanaalst/hue-sunrise/-/commits/main)
[![PyPi](https://img.shields.io/pypi/v/hue-sunrise)](https://pypi.org/project/hue-sunrise/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Downloads](https://pepy.tech/badge/hue-sunrise)](https://pepy.tech/project/hue-sunrise)

Enjoy waking up more gently by having your [philips hue](https://www.philips-hue.com/de-de) lights simulate a sunrise.

## Installation

```bash
pip install hue-sunrise
```

## Usage

First register your Hue bridge interactively

```bash
hue-sunrise register
```

Then simply call it with

```bash
hue-sunrise run
```

And view the config using

```bash
hue-sunrise config show
```

If you want to change the configuration use

```bash
hue-sunrise config ip               # IP address of your Hue bridge
hue-sunrise config lights           # lights which should participate
hue-sunrise config scene-length     # how many minutes the sunrise should take
hue-sunrise config afterglow        # how many minutes to stay lit after the sunrise
```

or, if you want to change where the configuration files are stored use the following environment variables

```bash
HS_CONFIG_PATH
HS_LOG_PATH
```


And finally if anything failed an you need to manually switch of the lights use

```bash
hue-sunrise shutdown
```

## Thanks

The beautiful CLI is due to [typer](https://typer.tiangolo.com/).
