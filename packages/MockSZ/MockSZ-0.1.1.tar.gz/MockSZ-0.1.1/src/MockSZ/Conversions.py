"""!
@file
Methods for unit conversions.
"""

import MockSZ.Constants as ct
import numpy as np

def eV_Temp(energy_eV):
    """!
    Convert an energy in electronvolt to temperature in Kelvin
    
    @param energy_eV Energy in electronvolt.
    
    @returns T temperature in Kelvin.
    """

    T = energy_eV / ct.k * ct.eV

    return T

def SI_JySr(I_freq):
    """
    Convert a specific brightness in SI units and convert to Jansky over steradian.

    @param I_freq Specific intensity in SI units.

    @returns JySr The specific intensity in Jansky / steradian
    """

    JySr = I_freq / 1e-26

    return JySr

def SI_Temp(I_freq, freqHz):
    """!
    Take specific intensity in SI units.
    Convert to a brightness temperature in Kelvin, assuming Rayleigh-Jeans tail.

    @param I_freq Specific intensity in SI units.
    @param freqHz Frequencies of I_freq in Hz.

    @returns Tb Brightness temperature.
    """

    Tb = I_freq * ct.c**2 / (2 * ct.k * freqHz**2)
    return Tb

def pc_m(l_pc):
    """!
    Convert a length in parsecs to meters.

    @param l_pc Length in parsecs.
    
    @returns l_m Length in meters.
    """

    conv = 3.0857e16
    l_m = l_pc * conv

    return l_m

def freq_x(freqHz):
    """!
    Convert frequency in Hertz to dimensionless frequency using CMB temperature.

    @param freqHz Frequencies in Hertz.
    
    @returns x The dimensionless frequency.
    """

    x = ct.h * freqHz / (ct.k * ct.Tcmb)

    return x

def x_freq(x):
    """!
    Convert dimensionless frequency to frequency in Hertz using CMB temperature.

    @param x Dimensionless frequency.
    
    @returns freqHz The frequency in Hertz.
    """

    freqHz = x / ct.h * ct.k * ct.Tcmb

    return freqHz

def Te_theta(Te):
    """!
    Get dimensionless electron temperature.

    @param Te Electron temperature in Kelvin.
    
    @returns theta Dimensionless electron temperature.
    """

    theta = ct.k * Te / (ct.me * ct.c**2)
    return theta

def v_beta(velocity):
    """!
    Obtain the beta factor from a velocity.

    @param velocity The electron velocity in m / s. Float or numpy array.

    @returns beta The beta factor. Float or numpy array.
    """
    
    beta = velocity / ct.c

    return beta

def v_gamma(velocity):
    """!
    Obtain the gamma factor from a velocity.

    @param velocity The electron velocity in m / s. Float or numpy array.

    @returns gamma The gamma factor. Float or numpy array.
    """

    beta = v_beta(velocity)
    gamma = beta_gamma(beta) 

    return gamma

def beta_gamma(beta):
    """!
    Obtain the gamma factor from a beta factor.

    @param beta The electron beta factor. Float or numpy array.

    @returns gamma The gamma factor. Float or numpy array.
    """

    gamma = 1 / np.sqrt(1 - beta**2)

    return gamma
