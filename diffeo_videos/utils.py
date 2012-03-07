import scipy.signal
import numpy as np
from procgraph import simple_block, COMPULSORY

def gauss_kern(size, sizey=None):
    """ Returns a normalized 2D gauss kernel array for convolutions """
    size = int(size)
    if not sizey:
        sizey = size
    else:
        sizey = int(sizey)
    x, y = np.mgrid[-size:size+1, -sizey:sizey+1]
    g = np.exp(-(x**2/float(size)+y**2/float(sizey)))
    return g / g.sum()

@simple_block
def blur_image(im, n=COMPULSORY, ny=None) :
    """ blurs the image by convolving with a gaussian kernel of typical
        size n. The optional keyword argument ny allows for a different
        size in the y direction.
    """
    g = gauss_kern(n, sizey=ny)
    if im.ndim == 2:
        return scipy.signal.convolve(im, g, mode='same')
    elif im.ndim == 3:
        res = np.empty_like(im)
        for i in range(3):
            res[:,:,i] = scipy.signal.convolve(im[:,:,i], g, mode='same')
        return res
    assert False
        
        

