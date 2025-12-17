'''
ndplot
A tool to perform n-dimensional plot from a collection of figures
'''

__version__ = 0.1

from functools import lru_cache
from PIL import Image
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import re, os
from sys import exit, stderr
from matplotlib.widgets import Slider
import numpy as np

@lru_cache(maxsize=256)
def loadImage(path):
    # This loads an image using the PIL library.
    # It is convenient over, e.g., plt.imread() because the image is *lazy* loaded.
    # On top of this, the decorator saves the image on the cache for later quicker access.
    img = Image.open(path).convert("RGBA")
    return img

def getDirectory():
    # This returns the directory containing the figures.
    # Also, it checks for its existence and provides a nice argparse interface.
    parser = ArgumentParser(
        prog = "ndplot",
        description = "A tool to perform n-dimensional plots from a collection of figures.")
    parser.add_argument("-d", "--directory", default='.', help="Directory containing the figures, the default is the current directory.")
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    args = parser.parse_args()
    if os.path.isdir(args.directory):
        return os.path.abspath(args.directory)
    else:
        print(f"Directory `{args.directory}` not found.", file=stderr)
        exit(1)

def loadParameters(DIR):
    # This funciton defines a dictionary that couples a parameter tuple to a image file name.
    # For example: dict[ (1.3, 45, -3, 0.5) ] = 'p1=1.3_p2=45_p3=-3_p4=0.5.png'

    # regex to identify a valid filename
    # <par1>_<par2>_..._<parN>.[png|jpg|gif]
    # e.g. `amp1=3_p1=-3.1_g23=10.png`
    filenameRegex = re.compile( r"([a-zA-Z]+[0-9]*=[-+]?\d*\.?\d+)(\_[a-zA-Z]+[0-9]*=[-+]?\d*\.?\d+)*\.(png|jpg|gif)$" )

    # regex to identify all parameters in the filename
    # <par>=<value>
    # e.g. `amp4=+1.37`
    parameterRegex = re.compile( r"[a-zA-Z]+[0-9]*=([-+]?\d*\.?\d+)" )

    parameterDict = {}
    values = []
    for filename in sorted(os.listdir(DIR)):
        matched = filenameRegex.search(filename) # this returns a match object (or None)
        if matched:
            parameters = parameterRegex.findall(filename) # this is a list           ['3', '-0.5', '3.14']
            val = tuple([float(p) for p in parameters])   # cast to tuple of float    (3.0, -0.5, 3.14)
            values.append(val)                            # list of tuples           [(3.0, -0.5, 3.14), (...), ...]
            parameterDict[val] = os.path.join(DIR, filename)
    if not parameterDict:
        print("No matching images found.", file=stderr)
        exit(1)
    values = np.asarray(values)                           # cast to np.array
    rangeValues = [np.unique(values[:, i]) for i in range(values.shape[1])]
    return parameterDict, values, rangeValues

def initSliders(vals, rangeVals):
    # This draws the slider axes and objects based on the loaded parameters.
    sliders = []
    slider_height = 0.06
    start = 0.9
    nParams = vals.shape[1]
    for i in range(nParams):
        tmp_ax = plt.axes([0.05, start - i*slider_height, 0.18, 0.04])
        # Use Slider but snap selection manually in callback
        s = Slider(tmp_ax, f"p{i}", rangeVals[i].min(), rangeVals[i].max(), valinit=vals[0,i], valstep=rangeVals[i], initcolor='none')
        sliders.append(s)
    sliders[0].label.set_fontweight('bold')
    return sliders

class eventTracker:
    def __init__(self, ax, fig, sliders, dic, vals, rangeVals):
        self.ax = ax
        self.fig = fig
        self.sliders = sliders
        self.dic = dic
        self.vals = vals
        self.rangeVals = rangeVals
        self.nParams = len(sliders)
        self.activeDim = 0
        self.currentTuple = tuple(vals[0])
        im0 = loadImage(dic[self.currentTuple])
        self.ax.imshow(im0)

    def on_key(self, event):
        if event.key.isdigit():
            # when press a number key from 1...9
            k = int(event.key) - 1
            if 0 <= k < self.nParams:
                self.activeDim = k
                for i, s in enumerate(self.sliders):
                    s.label.set_text(f"p{i}")
                    if i == k:
                        s.label.set_fontweight('bold')
                    else:
                        s.label.set_fontweight('normal')
                self.fig.canvas.draw_idle()

    def on_scroll(self, event):
        incr = 1 if event.button == 'up' else -1
        idxs = []
        for t, v in zip(self.currentTuple, self.rangeVals):
            idx = np.abs(t - v).argmin()
            idxs.append(idx)
        idxs[self.activeDim] += incr
        if idxs[self.activeDim] < 0:
            idxs[self.activeDim] = 0
        elif idxs[self.activeDim] >= len(self.rangeVals[self.activeDim]):
            idxs[self.activeDim] = len(self.rangeVals[self.activeDim]) - 1
        self.currentTuple = tuple([self.rangeVals[i][idxs[i]] for i in range(self.nParams)])
        im = loadImage(self.dic[self.currentTuple])
        self.ax.clear()
        self.ax.axis('off')
        self.ax.imshow(im)
        self.fig.canvas.draw_idle()

# command line interface entry point for the `ndplot` script
def cli():
    DIR = getDirectory()
    dic, vals, rangeVals = loadParameters(DIR)

    # prepare figure
    fig, ax = plt.subplots(figsize=(8,5))
    ax.set_position([0.25, 0.02, 0.73, 0.97])
    ax.axis('off')

    # create sliders
    sliders = initSliders(vals, rangeVals)

    et = eventTracker(ax, fig, sliders, dic, vals, rangeVals)

    fig.canvas.mpl_connect('key_press_event', et.on_key)
    fig.canvas.mpl_connect('scroll_event', et.on_scroll)
    plt.show()

if __name__ == "__main__":
    cli()