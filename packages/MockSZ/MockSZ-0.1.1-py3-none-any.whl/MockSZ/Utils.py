"""!
@file
Utility functions for MockSZ.
"""

import numpy as np

def getXYGrid(x, y):
    """!
    Generate a grid of two (arrays of) values.

    @param x Float or array of size nx containing the value(s) along the abscissa.
    @param y Float or array of size ny containing the value(s) along the ordinate.
    
    @returns X C-style array of shape (nx, ny). If both x and y are float, returns a singleton.
    @returns Y C-style array of shape (nx, ny). If both x and y are float, returns a singleton.
    """

    if isinstance(y, float) and not isinstance(x, float):
        X, Y = np.mgrid[x[0]:x[-1]:x.size*1j, y:y:1j]

    elif not isinstance(y, float) and isinstance(x, float):
        X, Y = np.mgrid[x:x:1j, y[0]:y[-1]:y.size*1j]

    elif isinstance(y, float) and isinstance(x, float):
        X = np.array([x])
        Y = np.array([y])

    else:
        X, Y = np.mgrid[x[0]:x[-1]:x.size*1j, y[0]:y[-1]:y.size*1j]
   
    return X, Y

def getXYLogGrid(x, y):
    """!
    Generate a grid of two (arrays of) values.
    Note that this function is similar to getXYGrid.
    However, the y values are now interpreted as lying on a log scale.
    So, it is the exponent in base 10 that is evenly spaced.

    @param x Float or array of size nx containing the value(s) along the abscissa.
    @param y Float or array of size ny containing the value(s) along the ordinate.
    
    @returns X C-style array of shape (nx, ny). If both x and y are float, returns a singleton.
    @returns Y C-style array of shape (nx, ny). If both x and y are float, returns a singleton.
    """


    if isinstance(y, float) and not isinstance(x, float):
        X, Y = np.mgrid[x[0]:x[-1]:x.size*1j, y:y:1j]

    elif not isinstance(y, float) and isinstance(x, float):
        y_lo = np.log10(np.min(y))
        y_up = np.log10(np.max(y))
        X, Y = np.mgrid[x:x:1j, y_lo:y_up:y.size*1j]

        Y = 10**Y

    elif isinstance(y, float) and isinstance(x, float):
        X = np.array([x])
        Y = np.array([y])

    else:
        y_lo = np.log10(np.min(y))
        y_up = np.log10(np.max(y))
        X, Y = np.mgrid[x[0]:x[-1]:x.size*1j, y_lo:y_up:y.size*1j]
        Y = 10**Y
   
    return X, Y
