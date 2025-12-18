# N-dimensional plotting: `ndplot`

[![GitHub Release Date](https://img.shields.io/github/release-date/t3n0/ndplot)](https://github.com/t3n0/ndplot/releases/latest)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/t3n0/ndplot)](https://github.com/t3n0/ndplot/releases/latest)
[![GitHub all releases](https://img.shields.io/github/downloads/t3n0/ndplot/total)](https://github.com/t3n0/ndplot/releases/download/v1.0/ndplot-1.0.tar.gz)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/ndplot)](https://pypi.org/project/ndplot/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

![showcase_gif](https://raw.githubusercontent.com/t3n0/ndplot/refs/heads/main/showcase.gif)

This post-processing tool generates an n-dimensional plot from a given colletion of figures.
There are many other tools out there that perform the very same task (e.g. [napari](https://napari.org/stable/), [paraview](https://www.paraview.org/), [visit](https://visit-dav.github.io/visit-website/)), but they all have very steep learning curves. On the other hand, `ndplot` is designed to be *extremely* easy to use, simply run
```bash
ndplot -d /dir/with/the/figures/to/plot
```
with figures names that must respect the following format
```
<optional_prefix><par1>=<val1>_<par2>=<val2>_...<parN>=<valN>.[png|jpg|gif]
```
For example
```
/dir/with/the/figures/to/plot
x0=0.0_y0=0.0_a0=0.3_b0=1.0.png
x0=0.0_y0=0.0_a0=0.3_b0=2.0.png
x0=0.0_y0=0.0_a0=0.3_b0=3.0.png
...
```
Also, running the tool with *no flags* will scan the current directory.
**That's it!**

Finally, to navigate through the parameter space simply **click on the sliders** directly, or select a parameter with the numpad and **scroll using the mouse wheel**.

## Installation

You can install `ndplot` from the official PyPi repository using `pip`
```bash
pip install ndplot
```
Equivalently, you can download the most recent release from [here](https://github.com/t3n0/ndplot/releases/download/v0.2/ndplot-v0.2.zip) and install it manually.

## Features and performaces

This tool uses a few optimizations to plot and display the graphs interactively:
- figures are "lazy loaded", i.e. the system only reads a figure when it has to be displayed. In this way, `ndplot` can handle folder with **thousand of plots** without lagging.
- most recent figures are cached, so to further reduce I/O usage.
- parameters do not need to be equally spaced or to cover the whole parameter manifold. `ndplot` handles empty domains of the parameter space by simply falling back to the previously shown figure.

## Support

I developed this tool in my spare time as I needed something to quickly plot many many figures. If you also find it usefull please consider [buy me a coffee](https://buymeacoffee.com/tentacolo) and explore my other repos.

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.