'''
ndplot
A tool to perform n-dimensional plot from a collection of figures
'''

__version__ = 0.1

import os
import re
from PIL import Image
import numpy as np
from functools import lru_cache
import matplotlib.pyplot as plt
import argparse



@lru_cache(maxsize=256)
def load_image(path):
    '''
    Load image using PIL. This is convenient over plt.imread() or others because the image is *lazy* loaded.
    On top of this, the decorator saves the image on the cache for later quicker access.
    
    Parameters

    path: str
        image path
    
    Returns
        image: PIL.Image
    '''
    img = Image.open(path).convert("RGBA")
    return img

def getArgs():
    parser = argparse.ArgumentParser(
        prog = "ndplot",
        description = "A tool to perform n-dimensional plots from a collection of figures.")
    
    parser.add_argument("-d", "--directory", default='.', help="Directory containing the figures, the default is the current directory.")
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    return parser.parse_args()

# prepare figure
# fig, ax = plt.subplots(figsize=(8,5))
# ax.set_position([0.25, 0.02, 0.73, 0.97])
# ax.axis('off')

# IMG_FOLDER = 'figs'
# file_name = 'fig_p0=0_p1=0_p2=0.png'

# img = load_image(os.path.join(IMG_FOLDER, file_name))
# ax.imshow(img)
# plt.show()

# example filename
file_name = 'ampolla=1.0_g1=-3_g2=.5_k0=+3.14.png'

# regex to identify all parameters in the filename
# <par>=<value>
# e.g. `amp4=+1.37`
regex_params = r"""
# group 1
(
[a-zA-Z]+[0-9]*    # name of the parameter, at least one char and optional numbers
)
=                  # equal sign
# group 2
(
[-+]?              # optional plus or minus signs
\d*                # optional first digits
\.?                # optional floating point
\d+                # at least one significant digit
)
"""

# regex to identify a valid filename
# <par1>_<par2>_..._<parN>.[png|jpg|gif]
# e.g. `amp1=3_p1=-3.1_p2=10.png`
regex_filename = r"^([a-zA-Z]+[0-9]*=[-+]?\d*\.?\d+)(\_[a-zA-Z]+[0-9]*=[-+]?\d*\.?\d+)*\.(png|jpg|gif)$"

regex_params_compiled = re.compile(regex_params, re.VERBOSE)
regex_filename_compiled = re.compile(regex_filename)

params = regex_params_compiled.findall(file_name)
fname = regex_filename_compiled.match(file_name)

# print(fname)
# print(fname.group())
# print(fname.span())

# print('\nparameters')
# for par, val in params:
#     print(f' {par:5.5s} = {float(val):+.2f}')

args = getArgs()

print(args)