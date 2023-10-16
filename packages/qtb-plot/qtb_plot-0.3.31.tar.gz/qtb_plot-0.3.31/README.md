# QTB Plot

[![pipeline status](https://gitlab.com/marvin.vanaalst/qtb-plot/badges/main/pipeline.svg)](https://gitlab.com/marvin.vanaalst/qtb-plot/-/commits/main)
[![coverage report](https://gitlab.com/marvin.vanaalst/qtb-plot/badges/main/coverage.svg)](https://gitlab.com/marvin.vanaalst/qtb-plot/-/commits/main)
[![PyPi](https://img.shields.io/pypi/v/qtb-plot)](https://pypi.org/project/qtb-plot/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Downloads](https://pepy.tech/badge/qtb-plot)](https://pepy.tech/project/qtb-plot)

This package is basically just a convenience matplotlib option setter.
You have two ways of using it.
With `set_style` you set the style for the entire notebook or whatever session
you are working in and with `plotting_context` you create a context manager
that will only set the style locally for the current plot.

Take a look at the supplied tutorial notebok to see how this is done.


The easiest way of installing the package is to cd into the package folder and to install it locally with
`pip install -e .`
