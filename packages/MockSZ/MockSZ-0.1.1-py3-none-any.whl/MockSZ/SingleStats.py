"""!
@file
Single electron scattering statistics.
"""

import numpy as np

import MockSZ.Utils as MUtils
import MockSZ.Conversions as MConv

def getPsbThomson(s, beta, num_mu=1000, grid=True):
    """!
    Get the probability of a logarithmic frequency shift s, given a beta factor of an electron.
    Note that this probability is calculated assuming Thomson scattering.

    @param s Logarithmic frequency shift. Float or numpy array.
    @param beta Beta factor of electron. Float or array.
    @param num_mu Number of points in mu to integrate over.
    @param grid Whether to evaluate on an S-BETA grid or Hadamard product. If False, length of s needs to be the same as beta.
    """

    if grid:
        S, BETA = MUtils.getXYGrid(s, beta)
    else:
        S = s
        BETA = beta

    s1_mask = S > 0 # Bool array, 1 where s > 0, 0 where s <= 0
    s2_mask = S <= 0 # Bool array, 0 where s > 0, 1 where s <= 0
    mu1 = np.ones(S.shape) * -1
    mu2 = np.ones(S.shape)

    mu1[s1_mask] = (1 - np.exp(-S[s1_mask]) * (1 + BETA[s1_mask])) / BETA[s1_mask]

    mu2[s2_mask] = (1 - np.exp(-S[s2_mask]) * (1 - BETA[s2_mask])) / BETA[s2_mask]

    dmu = (mu2 - mu1) / num_mu

    GAMMA = MConv.beta_gamma(BETA)
    prefac = 3 / (16 * GAMMA**4 * BETA)

    integrand = np.zeros(S.shape)
    for i in range(num_mu):
        mu = mu1 + (i + 0.5)*dmu
        mu_pr = (np.exp(S) * (1 - BETA * mu) - 1) / BETA

        integrand += (1 + BETA * mu_pr) * (1 + mu**2 * mu_pr**2 + 0.5 * (1 - mu**2) * (1 - mu_pr**2)) * (1 - BETA * mu)**(-3) * dmu

    out = prefac * integrand

    out[out < 0] = 0

    return out
