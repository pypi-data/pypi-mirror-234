"""!
@file 
Background sources for SZ effect.
"""

import numpy as np
import MockSZ.Constants as ct

def getSpecificIntensityCMB(freqs):
    """!
    Generate a blackbody with CMB temperature.

    @param freqs Frequencies at which to obtain intensities, in Hz.

    @returns out CMB spectrum.
    """

    prefac = 2 * ct.h * freqs**3 / ct.c**2
    distri = (np.exp(ct.h * freqs / (ct.k * ct.Tcmb)) - 1)**(-1)

    return prefac * distri
