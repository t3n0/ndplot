'''
ndplot
Generates n-dimensional interactive plots from a collection of figures.
'''

__version__ = '1.0.5'

from functools import lru_cache
from PIL import Image
from argparse import ArgumentParser
from sys import exit, stderr
from matplotlib.widgets import Slider
import re, os
import matplotlib.pyplot as plt
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
    # For example: dict[ (1.3, 45, -3, 0.5) ] = '/path/to/dir/p1=1.3_p2=45_p3=-3_p4=0.5.png'

    # regex to identify a valid filename
    # <par1>_<par2>_..._<parN>.[png|jpg|gif]
    # e.g. `amp1=3_p1=-3.1_g23=10.png`
    filenameRegex = re.compile( r"([a-zA-Z]+[0-9]*=[-+]?\d*\.?\d+)(\_[a-zA-Z]+[0-9]*=[-+]?\d*\.?\d+)*\.(png|jpg|gif)$" )

    # regex to identify all parameters in the filename
    # <par>=<value>
    # e.g. `amp4=+1.37`
    parameterRegex = re.compile( r"([a-zA-Z]+[0-9]*)=([-+]?\d*\.?\d+)" )

    parameterDict = {}
    values = []
    names = []
    for filename in sorted(os.listdir(DIR)):
        matched = filenameRegex.search(filename) # this returns a match object (or None)
        if matched:
            aux = parameterRegex.findall(filename)
            paramNames = [aux[i][0] for i in range(len(aux))]      # this is a list           ['amp', 'p0', 'g2']
            parameters = [aux[i][1] for i in range(len(aux))]      # this is a list           ['3', '-0.5', '3.14']
            val = tuple([float(p) for p in parameters])            # cast to tuple of float    (3.0, -0.5, 3.14)
            values.append(val)                                     # list of tuples           [(3.0, -0.5, 3.14), (...), ...]
            names.append(paramNames)
            parameterDict[val] = os.path.join(DIR, filename)
    if not parameterDict:
        print("No matching images found.", file=stderr)
        exit(1)
    sameNames = all(sub == names[0] for sub in names)
    if not sameNames:
        print("Some parameters have mismatching names.", file=stderr)
        exit(1)
    values = np.asarray(values)                           # cast to np.array
    rangeValues = [np.unique(values[:, i]) for i in range(values.shape[1])]
    return parameterDict, values, rangeValues, paramNames

def initSliders(vals, rangeVals, paramNames):
    # This draws the slider axes and objects based on the loaded parameters.
    sliders = []
    slider_height = 0.06
    start = 0.15
    nParams = vals.shape[1]
    for i in range(nParams):
        tmp_ax = plt.axes([0.05, start + i*slider_height, 0.15, 0.04])
        # Use Slider but snap selection manually in callback
        if rangeVals[i].min() == rangeVals[i].max():
            s = Slider(tmp_ax, f"{paramNames[i]}", rangeVals[i].min()-0.1, rangeVals[i].max()+0.1, valinit=vals[0,i], valfmt='%.1f', initcolor='none')
            s.active = False
            s.poly.set_visible(False)
        else:
            s = Slider(tmp_ax, f"{paramNames[i]}", rangeVals[i].min(), rangeVals[i].max(), valinit=vals[0,i], valstep=rangeVals[i], valfmt='%.1f', initcolor='none')
        sliders.append(s)
    sliders[0].label.set_fontweight('bold')
    return sliders

def indexTuple(curr, rangeVals):
    idxs = []
    for t, v in zip(curr, rangeVals):
        idx = np.abs(t - v).argmin()
        idxs.append(idx)
    return idxs

def drawImage(fig, ax, filename):
    # if the filename is none, don't draw anything and keep the current image
    if filename:
        im = loadImage(filename)
        axTitle = ax.get_title() # sloppy workaround for the axes title
        ax.clear()
        ax.set_title(axTitle)
        ax.imshow(im)
        fig.canvas.draw_idle()

class eventTracker:
    def __init__(self, ax, fig, sliders, dic, vals, rangeVals, paramNames):
        self.ax = ax
        self.fig = fig
        self.sliders = sliders
        self.dic = dic
        self.vals = vals
        self.rangeVals = rangeVals
        self.paramNames = paramNames
        self.nParams = len(sliders)
        self.activeDim = 0
        self.currentTuple = tuple(vals[0])
        self.currentIdxs = indexTuple(self.currentTuple, self.rangeVals)
        im0 = loadImage(dic[self.currentTuple])
        self.ax.imshow(im0)

    def on_key(self, event):
        if event.key.isdigit():
            # when press a number key from 1...9
            k = int(event.key) - 1
            if 0 <= k < self.nParams:
                self.activeDim = k
                for i, s in enumerate(self.sliders):
                    s.label.set_text(f"{self.paramNames[i]}")
                    if i == k:
                        s.label.set_fontweight('bold')
                    else:
                        s.label.set_fontweight('normal')
                self.fig.canvas.draw_idle()

    def on_scroll(self, event):
        incr = 1 if event.button == 'up' else -1
        self.currentIdxs[self.activeDim] += incr
        if self.currentIdxs[self.activeDim] < 0:
            self.currentIdxs[self.activeDim] = 0
        elif self.currentIdxs[self.activeDim] > len(self.rangeVals[self.activeDim]) - 1:
            self.currentIdxs[self.activeDim] = len(self.rangeVals[self.activeDim]) - 1
        self.currentTuple = tuple([self.rangeVals[i][self.currentIdxs[i]] for i in range(self.nParams)])
        self.sliders[self.activeDim].set_val(self.rangeVals[self.activeDim][self.currentIdxs[self.activeDim]])
        filename = self.dic.get(self.currentTuple)
        drawImage(self.fig, self.ax, filename)

    def moveSlider(self, var=None):
        self.currentTuple = tuple([s.val for s in self.sliders])
        self.currentIdxs = indexTuple(self.currentTuple, self.rangeVals)
        filename = self.dic.get(self.currentTuple)
        drawImage(self.fig, self.ax, filename)

# command line interface entry point for the `ndplot` script
def cli():

    # plt style: remove ticks and labels, but keep the axes frame
    plt.rcParams.update({
        "xtick.bottom": False,
        "xtick.labelbottom": False,
        "ytick.left": False,
        "ytick.labelleft": False,
    })

    # init directory, dictionary and parameters
    DIR = getDirectory()
    dic, vals, rangeVals, paramNames = loadParameters(DIR)

    # prepare figure
    fig, ax = plt.subplots(figsize=(8,5))
    ax.set_position([0.25, 0.02, 0.73, 0.97])
    ax.set_title(os.path.basename(DIR))

    # create sliders
    sliders = initSliders(vals, rangeVals, paramNames)

    # event tracker
    et = eventTracker(ax, fig, sliders, dic, vals, rangeVals, paramNames)

    # catch events
    for s in sliders:
        s.on_changed(et.moveSlider)
    fig.canvas.mpl_connect('key_press_event', et.on_key)
    fig.canvas.mpl_connect('scroll_event', et.on_scroll)
    plt.show()

if __name__ == "__main__":
    cli()