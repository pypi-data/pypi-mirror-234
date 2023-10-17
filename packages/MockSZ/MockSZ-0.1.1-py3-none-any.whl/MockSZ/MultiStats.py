"""!
@file
Expressions for calculating multi-electron scattering statistics.
"""

import numpy as np
import os

import MockSZ.SingleStats as MSingle
import MockSZ.ElectronDistributions as EDist

from multiprocessing import Pool
from functools import partial

import matplotlib.pyplot as pt

def getP1_RM(s, Te, num_beta=1000, num_mu=100):
    """!
    Generate the one-scattering ensemble scattering kernel P1.
    This kernel corresponds to a relativistic Maxwellian.

    @param s Range of log frequency shifts over which to evaluate P1.
    @param Te Electron temperature of plasma in Kelvin.
    @param num_beta Number of beta factor points to evaluate.
    @param num_mu Number of direction cosines to evaluate for single electron scattering cross-section.

    @returns P1 The P1 scattering kernel.
    """

    beta_lim = (np.exp(np.absolute(s)) - 1) / (np.exp(np.absolute(s)) + 1)

    dbeta = (1 - beta_lim) / num_beta
    
    numThreads = os.cpu_count()# if numThreads is None else numThreads
    
    chunks_beta = np.array_split(np.arange(num_beta), numThreads)
    args = chunks_beta

    _parallelFuncPartial = partial(_MJ_parallel, 
                                   beta_lim=beta_lim,
                                   num_mu=num_mu,
                                   s=s,
                                   dbeta=dbeta,
                                   Te=Te)
        
    pool = Pool(numThreads)
    res = np.sum(np.array(pool.map(_parallelFuncPartial, args)), axis=0)
    
    return res

def _MJ_parallel(args, beta_lim, num_mu, s, dbeta, Te):
    """!
    Function to be called in multiprocessing.
    Calculates chunks of the scattering, as function of s, over beta.
    Uses the Maxwell-Juttner distribution for the electron population.

    @param args Chunk of array to be calculated in parallel.
    @param beta_lim Array with lower limits on beta, as function of s.
    @param num_mu Number of scattering angles to consider in integration.
    @param s Array with s values.
    @param dbeta Steps between beta values.
    @param Te electron temperature, in Kelvin.

    @returns P1 Calculated contribution of beta chunk to scattering kernel.
    """

    beta = args

    P1 = np.zeros(s.shape)
    for i in beta:
        be = beta_lim + (i + 0.5)*dbeta

        Psb = MSingle.getPsbThomson(s, be, num_mu, grid=False)

        Pe = EDist.relativisticMaxwellian(be, Te)
        P1 += Pe * Psb * dbeta

    return P1

def getP1_PL(s, alpha, num_beta=1000, num_mu=100):
    """!
    Generate the one-scattering ensemble scattering kernel P1.
    This kernel corresponds to a power law.

    @param s Range of log frequency shifts over which to evaluate P1.
    @param alpha Slope of power law.
    @param num_beta Number of beta factor points to evaluate.
    @param num_mu Number of direction cosines to evaluate for single electron scattering cross-section.

    @returns P1 The P1 scattering kernel.
    """
    beta_lim = (np.exp(np.absolute(s)) - 1) / (np.exp(np.absolute(s)) + 1)

    dbeta = (1 - beta_lim) / num_beta
    numThreads = os.cpu_count()# if numThreads is None else numThreads
    
    chunks_beta = np.array_split(np.arange(num_beta), numThreads)
    args = chunks_beta

    _parallelFuncPartial = partial(_PL_parallel, 
                                   beta_lim=beta_lim,
                                   num_mu=num_mu,
                                   s=s,
                                   dbeta=dbeta,
                                   alpha=alpha)
        
    pool = Pool(numThreads)
    res = np.sum(np.array(pool.map(_parallelFuncPartial, args)), axis=0)
    
    return res

def _PL_parallel(args, beta_lim, num_mu, s, dbeta, alpha):
    """!
    Function to be called in multiprocessing.
    Calculates chunks of the scattering, as function of s, over beta.
    Uses the powerlaw distribution for the electron population.

    @param args Chunk of array to be calculated in parallel.
    @param beta_lim Array with lower limits on beta, as function of s.
    @param num_mu Number of scattering angles to consider in integration.
    @param s Array with s values.
    @param dbeta Steps between beta values.
    @param alpha Powerlaw spectral index.

    @returns P1 Calculated contribution of beta chunk to scattering kernel.
    """

    beta = args

    P1 = np.zeros(s.shape)
    for i in beta:
        be = beta_lim + (i + 0.5)*dbeta

        Psb = MSingle.getPsbThomson(s, be, num_mu, grid=False)

        Pe = EDist.relativisticPowerlaw(be, np.min(beta_lim), alpha=alpha)
        P1 += Pe * Psb * dbeta * be * (1 - be**2)**(-3/2)

    return P1
