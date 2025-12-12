import os
from PIL import Image
import numpy as np
from functools import lru_cache
import matplotlib.pyplot as plt

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

# prepare figure
fig, ax = plt.subplots(figsize=(8,5))
ax.set_position([0.25, 0.02, 0.73, 0.97])
# plt.subplots_adjust(left=0.25, bottom=0.02, right=0.98, top=0.98)
# ax.axis('off')

IMG_FOLDER = 'figs'
file_name = 'fig_p0=0_p1=0_p2=0.png'

img = load_image(os.path.join(IMG_FOLDER, file_name))
arr = np.asarray(img)
ax.imshow(arr)
plt.show()