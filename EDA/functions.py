import matplotlib.pyplot as plt
from scipy.stats import *
from scipy import stats
import numpy as np
import pandas as pd
import seaborn as sns
import statistics
import pickle as pk
from itertools import product


def write_binary_files(path, file):
    """
    :param path: path were to write the file
    :param file: file to write in binary
    :return: None
    """
    with open(path, 'wb') as f:
        pk.dump(file, f)

def normalization(values):
    """
    :param values: values to normalize
    :return: values normalized. Each one between 0 and 1
    """
    values = (values - min(values)) / (max(values) - min(values))
    return values

def plot_tpr_fpr(values, specificity, sensitivity):
    """
    This function plot the relation between Sensitivity (TPR) and the FPR.
    :param values:
    :param specificity:
    :param sensitivity:
    :return:
    """
    plt.scatter(pow(np.ones(len(values[specificity])) - values[specificity], 1),
                values[sensitivity])
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')

    plt.savefig('figures/tpr_fpr.png')

    plt.show()

def calculate_loc_scale(pd_values, column):
    """
    :param pd_values: dataframe containing values
    :param column: column of the dataframe to consider
    :return: [x1, x2]: x1 is the loc and x2 is the scale of the data
    """
    values = pd_values[column].dropna()

    print(len(values))

    loc = statistics.mean(values)
    scale = statistics.pstdev(values)
    var = statistics.pvariance(values)
    min_value = values.min()
    max_value = values.max()

    return [loc, scale, var, min_value, max_value]

def eliminate_outliers(values):
    """
    :param values: values containing outliers
    :return: returns the values without outliers
    """
    z_scores = stats.zscore(values)
    mask = np.abs(z_scores) <= 3
    values = values[mask]

    return values

def qq_plot(values, dist_par, column):
    """
    Functions to generate and plot qq-plots for the normal, exponential, levy_l and beta distributions
    :param values: empirical values for which to build the plot
    :param dist_par: parameters of the distribution with which to build the theoretical quantiles
    :return: None
    """
    q = np.linspace(0, 0.99, )
    size = len(values)

    norm_theory_quantiles = np.quantile(
        normalization(norm.rvs(loc=dist_par['norm']['loc'], scale=dist_par['norm']['scale'], size=size)), q)

    expon_theory_quantiles = np.quantile(
        normalization(expon.rvs(loc=dist_par['expon']['loc'], scale=dist_par['expon']['scale'], size=size)), q)

    levy_l_theory_quantiles = np.quantile(
        normalization(levy_l.rvs(loc=dist_par['levy_l']['loc'], scale=dist_par['levy_l']['scale'], size=size)), q)

    beta_theory_quantiles = np.quantile(
        beta.rvs(loc=dist_par['beta']['loc'], scale=dist_par['beta']['scale'], a=dist_par['beta']['alpha'],
                 b=dist_par['beta']['beta'], size=size), q)

    data_quantiles = np.quantile(values, q)

    fig, axes = plt.subplots()

    axes.scatter(norm_theory_quantiles, data_quantiles, label='norm')
    axes.scatter(expon_theory_quantiles, data_quantiles, label='expon')
    axes.scatter(levy_l_theory_quantiles, data_quantiles, label='levy_l')
    axes.scatter(beta_theory_quantiles, data_quantiles, label='beta')

    axes.legend()

    plt.savefig('figures/qq_plot_{}.png'.format(column))
    plt.show()


def kolmogorov_smirnov_test_1(values, size, dist_par):
    """
    Function to implement the kolmogorov test between the sample values and the theoretical distribution
    :param values: empirical values with which to do the kolmogorov test
    :param size:
    :param dist_par: parameters of the distributions to build the theoretical distribution
    :return:
    """
    n = 20

    # H0: the data possesses normal distribution
    norm_frozen = stats.norm(loc=dist_par['norm']['loc'], scale=dist_par['norm']['scale'])
    result_norm = ks_1samp(values.sample(n=n), norm_frozen.cdf)

    # H0: the data possesses exponential distribution
    expon_frozen = stats.expon(loc=dist_par['expon']['loc'], scale=dist_par['expon']['scale'])
    result_expon = ks_1samp(values.sample(n=n), expon_frozen.cdf)

    # H0: the data possesses levy_l distribution
    levy_l_frozen = stats.levy_l(loc=dist_par['levy_l']['loc'], scale=dist_par['levy_l']['scale'])
    result_levy_l = ks_1samp(values.sample(n=n), levy_l_frozen.cdf)

    # H0: the data possesses beta distribution
    beta_frozen = stats.beta(a=dist_par['beta']['alpha'], b=dist_par['beta']['beta'], loc=dist_par['beta']['loc'],
                             scale=dist_par['beta']['scale'])
    result_beta = ks_1samp(values.sample(n=n), beta_frozen.cdf)

    print("Result norm: {}\nResult expon: {}"
          "\nResult levy_l: {}\nResult beta: {}".format(result_norm, result_expon, result_levy_l, result_beta))


def cramer_von_mises_test_1(values, size, dist_par):
    """
    Function to implement the Cramer von Mises test between the values and the theoretical distribution
    :param values: empirical values
    :param size:
    :param dist_par: parameters to have the theoretical distribution
    :return:
    """
    n = 20

    norm_frozen = stats.norm(loc=dist_par['norm']['loc'], scale=dist_par['norm']['scale'])
    result_norm = cramervonmises(values.sample(n=n), norm_frozen.cdf)

    # H0: the data possesses exponential distribution
    expon_frozen = stats.expon(loc=dist_par['expon']['loc'], scale=dist_par['expon']['scale'])
    result_expon = cramervonmises(values.sample(n=n), expon_frozen.cdf)

    # H0: the data possesses levy_l distribution
    levy_l_frozen = stats.levy_l(loc=dist_par['levy_l']['loc'], scale=dist_par['levy_l']['scale'])
    result_levy_l = cramervonmises(values.sample(n=n), levy_l_frozen.cdf)

    # H0: the data possesses beta distribution
    beta_frozen = stats.beta(a=dist_par['beta']['alpha'], b=dist_par['beta']['beta'], loc=dist_par['beta']['loc'],
                             scale=dist_par['beta']['scale'])
    result_beta = cramervonmises(values.sample(n=n), beta_frozen.cdf)

    print("Result norm: {}\nResult expon: {}"
          "\nResult levy_l: {}\nResult beta: {}".format(result_norm, result_expon, result_levy_l, result_beta))


def kolmogorov_smirnov_test_2(values, size, dist_par):
    """
    Function to implement the kolmogorov test between two samples one empirical and the other coming from the
    distribution to test
    :param values: empirical values with which to do the kolmogorov test
    :param size:
    :param dist_par: parameters of the distributions to build the theoretical distribution
    :return:
    """

    n = 20

    p_values = {'norm': [], 'expon': [], 'levy_l': [], 'beta': []}

    norm = stats.norm(loc=dist_par['norm']['loc'], scale=dist_par['norm']['scale'])
    expon = stats.expon(loc=dist_par['expon']['loc'], scale=dist_par['expon']['scale'])
    levy_l = stats.levy_l(loc=dist_par['levy_l']['loc'], scale=dist_par['levy_l']['scale'])
    beta = stats.beta(a=dist_par['beta']['alpha'], b=dist_par['beta']['beta'],
                      loc=dist_par['beta']['loc'], scale=dist_par['beta']['scale'])

    for i in range(100):
        # H0: the data possesses normal distribution
        result_norm = ks_2samp(values.sample(n=n), norm.rvs(size=n))
        p_values['norm'].append(result_norm.pvalue)

        # H0: the data possesses exponential distribution
        result_expon = ks_2samp(values.sample(n=n), expon.rvs(size=n))
        p_values['expon'].append(result_expon.pvalue)

        # H0: the data possesses levy_l distribution
        result_levy_l = ks_2samp(values.sample(n=n), levy_l.rvs(size=n))
        p_values['levy_l'].append(result_levy_l.pvalue)

        # H0: the data possesses beta distribution
        result_beta = ks_2samp(values.sample(n=n), beta.rvs(size=n))
        p_values['beta'].append(result_beta.pvalue)

    print("Result norm: {}\nResult expon: {}"
          "\nResult levy_l: {}\nResult beta: {}".format(np.mean(p_values['norm']),
                                                         np.mean(p_values['expon']),
                                                         np.mean(p_values['levy_l']),
                                                         np.mean(p_values['beta'])))


def cramer_von_mises_test_2(values, size, dist_par):
    """
    Function to implement the Cramer von Mises test between samples.
    :param values: empirical values.
    :param size:
    :param dist_par: parameters to have the theoretical distribution.
    :return:
    """
    n = 20

    p_values = {'norm': [], 'expon': [], 'levy_l': [], 'beta': []}
    norm = stats.norm(loc=dist_par['norm']['loc'], scale=dist_par['norm']['scale'])
    expon = stats.expon(loc=dist_par['expon']['loc'], scale=dist_par['expon']['scale'])
    levy_l = stats.levy_l(loc=dist_par['levy_l']['loc'], scale=dist_par['levy_l']['scale'])
    beta = stats.beta(a=dist_par['beta']['alpha'], b=dist_par['beta']['beta'], loc=dist_par['beta']['loc'],
                      scale=dist_par['beta']['scale'])

    for i in range(100):
        result_norm = cramervonmises_2samp(values.sample(n=n), norm.rvs(size=n))
        p_values['norm'].append(result_norm.pvalue)

        # H0: the data possesses exponential distribution
        result_expon = cramervonmises_2samp(values.sample(n=n), expon.rvs(size=n))
        p_values['expon'].append(result_expon.pvalue)

        # H0: the data possesses levy_l distribution
        result_levy_l = cramervonmises_2samp(values.sample(n=n), levy_l.rvs(size=n))
        p_values['levy_l'].append(result_levy_l.pvalue)

        # H0: the data possesses beta distribution
        result_beta = cramervonmises_2samp(values.sample(n=n), beta.rvs(size=n))
        p_values['beta'].append(result_beta.pvalue)

    print("Result norm: {}\nResult expon: {}"
          "\nResult levy_l: {}\nResult beta: {}".format(np.mean(p_values['norm']),
                                                      np.mean(p_values['expon']),
                                                      np.mean(p_values['levy_l']),
                                                      np.mean(p_values['beta'])))


def choose_best_dist(pd_values, column, dist_par):
    """
    Function to help choosing the best distribution. Plot the qq-plots and calls the functions for the
    kolmogorov-smirnoff test and the cramer von mises test.
    :param pd_values: dataframe containing the values
    :param column:
    :param dist_par: parameters of the distribution to use
    :return:
    """
    values = pd_values[column].dropna()
    size = 100

    qq_plot(values, dist_par, column)

    print("\nKolmogorov Smirnov One Sample")
    kolmogorov_smirnov_test_1(values, size, dist_par)

    print("\nKolmogorov Smirnov Two Samples")
    kolmogorov_smirnov_test_2(values, size, dist_par)

    print("\nCramer One Sample")
    cramer_von_mises_test_1(values, size, dist_par)

    print("\nCramer Two Samples")
    cramer_von_mises_test_2(values, size, dist_par)


def sample_from_distribution(pd_values, column, dist_par, size):
    """
    :param pd_values: dataframe containing original data
    :param column: column of interest
    :param dist_par: parameters of the distributions (loc and scale)
    :param size: number of values to sample
    :return:
    """
    size = len(pd_values[column].dropna())
    pd_values[column + '_norm_sample'] = normalization(pd.Series(norm.rvs(loc=dist_par['norm']['loc'],
                                                                          scale=dist_par['norm']['scale'], size=size)))

    pd_values[column + '_expon_sample'] = normalization(pd.Series(expon.rvs(loc=dist_par['expon']['loc'],
                                                                            scale=dist_par['expon']['scale'],
                                                                            size=size)))

    pd_values[column + '_levy_l_sample'] = normalization(pd.Series(levy_l.rvs(loc=dist_par['levy_l']['loc'],
                                                                              scale=dist_par['levy_l']['scale'],
                                                                              size=size)))

    pd_values[column + '_beta_sample'] = pd.Series(beta.rvs(a=dist_par['beta']['alpha'], b=dist_par['beta']['beta'],
                                                            loc=dist_par['beta']['loc'],
                                                            scale=dist_par['beta']['scale'],
                                                            size=size))

def fit_distributions(pd_values, column, loc_data, scale_data):
    """
    Function to fit distributions to data
    :param pd_values: dataframe with data
    :param column: column to consider (sensitivity or specificity)
    :param loc_data: initial guess for loc
    :param scale_data: initial guess for scale
    :return:
    """
    values = pd_values[column].dropna()

    norm_loc, norm_scale = norm.fit(values, loc=loc_data, scale=scale_data)
    expon_loc, expon_scale = expon.fit(values, loc=loc_data, scale=scale_data)
    levy_l_loc, levy_l_scale = levy_l.fit(values, loc=loc_data, scale=scale_data)
    beta_alpha, beta_beta, beta_loc, beta_scale = beta.fit(values, loc=loc_data, scale=scale_data)

    param_dict = {'norm': {'loc': norm_loc, 'scale': norm_scale}, 'expon': {'loc': expon_loc, 'scale': expon_scale},
                  'levy_l': {'loc': levy_l_loc, 'scale': levy_l_scale},
                  'beta': {'alpha': beta_alpha, 'beta': beta_beta, 'loc': beta_loc, 'scale': beta_scale}}

    return param_dict


def plot_distribution(pd_values, column):
    """
    Functions to plot distributions
    :param pd_values:
    :param column:
    :return:
    """
    fig, axes = plt.subplots(2, 2)

    sns.histplot(pd_values[[column, column + '_norm_sample']], kde=True, element='step', ax=axes[0, 0])
    sns.move_legend(axes[0, 0], 'upper left')

    sns.histplot(pd_values[[column, column + '_expon_sample']], kde=True, element='step', ax=axes[0, 1])
    sns.move_legend(axes[0, 1], 'upper left')

    sns.histplot(pd_values[[column, column + '_levy_l_sample']], kde=True, element='step', ax=axes[1, 0])
    sns.move_legend(axes[1, 0], 'upper left')

    sns.histplot(pd_values[[column, column + '_beta_sample']], kde=True, element='step', ax=axes[1, 1])
    sns.move_legend(axes[1, 1], 'upper left')

    plt.savefig('figures/distribution_{}.png'.format(column))

    plt.show()

def plot_p_boxes(dist_type, pd_values, column, conf_int):
    """
    This function plots the p-boxes related to the Sensitivity (TPR) and Specificity (TNR).
    :param dist_type: distribution type
    :param pd_values: dataframe containing empirical values
    :param column: column of interest, related to sensitivity or specificity
    :param conf_int: confidence interval for loc and scale
    :return:
    """
    x = np.linspace(0, 1, 100000)

    print(conf_int['conf_int_loc'], conf_int['conf_int_scale'])
    combinations = list(product(conf_int['conf_int_loc'], conf_int['conf_int_scale']))

    if dist_type == 'levy_l':
        for i, comb in enumerate(combinations):
            plt.plot(x, levy_l.cdf(x, loc=comb[0], scale=comb[1]), label='n' + str(i))
            plt.title(column)

    elif dist_type == 'beta':
        for i, comb in enumerate(combinations):
            a, b, beta_loc, beta_scale = beta.fit(pd_values[column], loc=comb[0], scale=comb[1])
            plt.plot(x, beta.cdf(x, a=a, b=b, loc=beta_loc, scale=beta_scale), label='n' + str(i))

    plt.legend()
    plt.savefig('figures/p-boxes_{}.png'.format(column))

    plt.show()

def confid_interval(pd_values, column):
    """
    :param pd_values: contains the dataframe with sensitivity and specificity values.
    :param column: contains the column we are interested in.
    :return: confidence interval related to the loc and the scale
    """
    values = pd_values[column].dropna()

    num_bootstrap_samples = 1000
    bootstrap_sample_means = []
    bootstrap_sample_stds = []

    for i in range(num_bootstrap_samples):
        bootstrap_sample = values.sample(n=len(values), replace=True)

        bootstrap_mean = np.mean(bootstrap_sample)
        boostrap_std = np.std(bootstrap_sample)

        bootstrap_sample_means.append(bootstrap_mean)
        bootstrap_sample_stds.append(boostrap_std)

    confidence_interval_mean = np.percentile(bootstrap_sample_means, [2.5, 97.5])
    confidence_interval_std = np.percentile(bootstrap_sample_stds, [2.5, 97.5])

    d = {'conf_int_loc': confidence_interval_mean, 'conf_int_scale': confidence_interval_std}
    write_binary_files(f'binary_files/p_boxes/p_boxes_interval_{column}.pk', d)

    return {'conf_int_loc': confidence_interval_mean, 'conf_int_scale': confidence_interval_std}
