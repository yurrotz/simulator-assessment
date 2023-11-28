"""
This script is related to probability bound analysis
"""

import pba

import pickle as pk
import matplotlib.pyplot as plt

from scipy.stats import beta, levy_l
import numpy as np


def beta_pba(dist_par):
    box = pba.beta(pba.I(dist_par['beta']['alpha'] - 0.05, dist_par['beta']['alpha'] + 0.05),
                   pba.I(dist_par['beta']['beta'] - 0.05, dist_par['beta']['beta'] + 0.05),
                   pba.I(dist_par['beta']['loc'] - 0.05, dist_par['beta']['loc'] + 0.5),
                   pba.I(dist_par['beta']['scale'] - 0.05, dist_par['beta']['scale'] + 0.5))
    return box


def levy_l_pba(dist_par):
    box = pba.levy_l(pba.I(dist_par['levy_l']['loc'] - 0.05, dist_par['levy_l']['loc'] + 0.05),
                     pba.I(dist_par['levy_l']['scale'] - 0.05, dist_par['levy_l']['scale'] + 0.05))

    return box


if __name__ == '__main__':
    with open('../binary_files/p_boxes/p_boxes_interval_specificity_no_outliers.pk', 'rb') as f:
        par = pk.load(f)

    spec_box = pba.min_max_mean_var(0, 1,
                                    pba.I(par['conf_int_loc'][0], par['conf_int_loc'][1]),
                                    pba.I(pow(par['conf_int_scale'][0], 2), pow(par['conf_int_scale'][1], 2)))
    spec_box.show()

    """
    x = np.linspace(0, 2, 1000)
    plt.plot(x, beta.cdf(x, a=sens_dist_par['beta']['alpha'] - 0.05,
                         b=sens_dist_par['beta']['beta'] - 0.05,
                         loc=sens_dist_par['beta']['loc'] - 0.05,
                         scale=sens_dist_par['beta']['scale'] - 0.05))

    plt.plot(x, beta.cdf(x, a=sens_dist_par['beta']['alpha'] + 0.05,
                         b=sens_dist_par['beta']['beta'] + 0.05,
                         loc=sens_dist_par['beta']['loc'] + 0.96,
                         scale=sens_dist_par['beta']['scale'] + 0.05))

    plt.show()
    """