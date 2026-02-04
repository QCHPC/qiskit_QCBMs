# This code is a QAMP project based on Qiskit.
"""Create datasets to model with a QCBM."""

import numpy as np


class MixtureGaussianData():
    """Create a Bimodal Normal Dataset."""

    def __init__(self, x, mus, sigmas):
        pass

    @classmethod
    def mixture_gaussian_pdf(cls, x, mus, sigmas):
        """
        Creates probability density values of a mixture of Normal distributions
        """
        mus, sigmas = np.array(mus), np.array(sigmas)
        vars = sigmas**2
        # Say, there are 2 mu's and 1 sd, then values will have length 2,
        # and each element will have len(x)
        values = [
                  (1 / np.sqrt(2 * np.pi * v)) *
                  np.exp(-((x - m) ** 2) / (2 * v))
                  for m, v in zip(mus, vars)
        ]
        # values will now be collapsed over the multiple dims,
        # if any, and will have len(x)
        values = np.sum([val / sum(val) for val in values], axis=0)

        # values be returned will again have len(x)
        return values / np.sum(values)
