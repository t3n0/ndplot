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
# import numpy as np

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
    for filename in sorted(os.listdir(DIR)):
        matched = filenameRegex.search(filename) # this returns a match object (or None)
        if matched:
            parameters = parameterRegex.findall(filename) # findall returns a list e.g. ['3', '-0.5', '3.14']
            parameterDict[tuple(parameters)] = filename
    return parameterDict

# img = load_image(os.path.join(IMG_FOLDER, file_name))
# ax.imshow(img)
# plt.show()

# command line interface entry point for the `ndplot` script
def cli():
    DIR = getDirectory()

    # prepare figure
    # fig, ax = plt.subplots(figsize=(8,5))
    # ax.set_position([0.25, 0.02, 0.73, 0.97])
    # ax.axis('off')

    loadParameters(DIR)

if __name__ == "__main__":
    cli()