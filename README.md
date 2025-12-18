# N-dimensional plotting: `ndplot`

[![GitHub Release Date](https://img.shields.io/github/release-date/t3n0/ndplot)](https://github.com/t3n0/ndplot/releases/latest)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/t3n0/ndplot)](https://github.com/t3n0/ndplot/releases/latest)
[![GitHub all releases](https://img.shields.io/github/downloads/t3n0/ndplot/total)](https://github.com/t3n0/ndplot/releases/download/v0.2/ndplot-v0.2.zip)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

![showcase_gif](./showcase.gif)

This post-processing tool generates an n-dimensional plot from a given colletion of figures.
There are many other tools out there that perform the very same task (e.g. [napari](https://napari.org/stable/), [paraview](https://www.paraview.org/), [visit](https://visit-dav.github.io/visit-website/)). But they all have very steep learning curves. On the other hand, `ndplot` is designed to be *extremely* easy to use, simply run
```bash
ndplot -d /dir/with/the/figures/to/plot
```
Equivalently, running the tool with no flags will scan the current directory. **That's it!**

