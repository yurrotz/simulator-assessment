import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import *
import numpy as np
from itertools import product
from numpy.random import uniform


from functions import (eliminate_outliers, choose_best_dist, sample_from_distribution, calculate_loc_scale,
                       fit_distributions, plot_distribution, plot_tpr_fpr, confid_interval, write_binary_files,
                       plot_p_boxes)

def choose_lower_upper_bound(dist_type, conf_int):
    combinations = list(product(conf_int['conf_int_loc'], conf_int['conf_int_scale']))
    print("Combinations: ", combinations)

    x = uniform(0, 1, size=10)

    if dist_type == 'levy_l':
        values_comb = {i: np.array(levy_l.cdf(loc=comb[0], scale=comb[1], x=x))
                       for i, comb in enumerate(combinations)}

        print("Values comb: ", values_comb)

        lower_bound = {}
        upper_bound = {}
        for key in values_comb.keys():
            lower_bound[key] = []
            upper_bound[key] = []
            for key1 in values_comb.keys():
                if key != key1:
                    if np.all(values_comb[key] >= values_comb[key1]):
                        upper_bound[key].append(key1)
                    if np.all(values_comb[key] <= values_comb[key1]):
                        lower_bound[key].append(key1)

        max_key_upper = max(upper_bound, key=lambda k: len(upper_bound[k]))
        max_key_lower = max(lower_bound, key=lambda k: len(lower_bound[k]))

        print("Upper bound: ", upper_bound)
        print("Lower bound: ", lower_bound)

        d = {'dist': dist_type, 'lower_loc': combinations[max_key_lower][0],
                'lower_scale': combinations[max_key_lower][1],
                'upper_loc': combinations[max_key_upper][0],
                'upper_scale': combinations[max_key_upper][1]}

        return d

    elif dist_type == 'beta':
        pass


def preproc_csv():
    pd_values = pd.read_csv('csv/sensitivity_specificity.csv')
    pd_values['sensitivity'] = pd.to_numeric(pd_values['sensitivity'].str.replace(',', '.', regex=True))
    pd_values['specificity'] = pd.to_numeric(pd_values['specificity'].str.replace(',', '.', regex=True))

    pd_values['sensitivity_no_outliers'] = eliminate_outliers(pd_values['sensitivity'])
    pd_values['specificity_no_outliers'] = eliminate_outliers(pd_values['specificity'])

    pd_values.dropna(inplace=True, axis=0)

    return pd_values

def mc_simulation_data():
    """
    In this function we calculate the parameters for the functions for the simple monte carlo simulation
    :return:
    """

    """Fitting distributions to data. This is necessary for the single MC simulation"""
    sens_dist_par = fit_distributions(pd_values, 'sensitivity_no_outliers', data_loc_sens, data_scale_sens)
    spec_dist_par = fit_distributions(pd_values, 'specificity_no_outliers', data_loc_spec, data_scale_spec)

    """Save binary files related to Sensitivity and Specificity distribution parameters"""
    write_binary_files('binary_files/dist_par/sens_dist_par.pk', sens_dist_par)
    write_binary_files('binary_files/dist_par/spec_dist_par.pk', spec_dist_par)

    """Choose the best distribution"""
    choose_best_dist(pd_values, 'sensitivity_no_outliers', sens_dist_par)
    choose_best_dist(pd_values, 'specificity_no_outliers', spec_dist_par)

    single_mc = {'mc_sens': sens_dist_par, 'mc_spec': spec_dist_par}

    return single_mc

def mc_simulation_interval_data(dist_type):
    """
    Calculate confidence interval for MC interval simulation
    """

    sens_conf_inter = confid_interval(pd_values, 'sensitivity_no_outliers')
    spec_conf_inter = confid_interval(pd_values, 'specificity_no_outliers')

    """Plot the p-boxes for the MC interval simulation, so that we know what are the p-boxes"""
    plot_p_boxes(dist_type, pd_values, 'sensitivity_no_outliers', sens_conf_inter)
    plot_p_boxes(dist_type, pd_values, 'specificity_no_outliers', spec_conf_inter)

    # For now we do it only for specificity because we are sampling only specificity
    return choose_lower_upper_bound(dist_type, spec_conf_inter)


if __name__ == '__main__':

    """Set the random seed"""
    np.random.seed(42)

    """Getting values from csv file"""
    pd_values = preproc_csv()

    """Plot True Positive Rate and False Positive Rate"""
    plot_tpr_fpr(pd_values, 'specificity_no_outliers', 'sensitivity_no_outliers')

    """Get the dimension of data without outliers"""
    size_sens = len(pd_values['sensitivity'])
    size_spec = len(pd_values['specificity'])

    """Calculation of mean, standard deviation from paper data for sensitivity and specificity."""
    data_loc_sens, data_scale_sens, data_var_sens, data_min_sens, data_max_sens = (
        calculate_loc_scale(pd_values, 'sensitivity_no_outliers'))
    data_loc_spec, data_scale_spec, data_var_spec, data_min_spec, data_max_spec = (
        calculate_loc_scale(pd_values, 'specificity_no_outliers'))

    print(data_loc_spec, data_scale_spec, data_var_spec)
    par_sens = {'data_loc_sens': data_loc_sens, 'data_scale_sens': data_scale_sens, 'data_var_sens': data_var_sens,
                'data_min_sens': data_min_sens, 'data_max_sens': data_max_sens}
    par_spec = {'data_loc_spec': data_loc_spec, 'data_scale_spec': data_scale_spec, 'data_var_spec': data_var_spec,
                'data_min_spec': data_min_spec, 'data_max_spec': data_max_spec}

    print("Ueue: ", par_sens)
    print("Ueue: ", par_spec)

    write_binary_files('binary_files/p_boxes/p_boxes_parameters_sens.pk', par_sens)
    write_binary_files('binary_files/p_boxes/p_boxes_parameters_spec.pk', par_spec)

    """Get the data to use for the MC simple simulation"""
    single_mc = mc_simulation_data()

    """Sample from distribution"""
    sample_from_distribution(pd_values, 'sensitivity_no_outliers', single_mc['mc_sens'], size_sens)
    sample_from_distribution(pd_values, 'specificity_no_outliers', single_mc['mc_spec'], size_spec)

    """Plot distributions"""
    plot_distribution(pd_values, 'sensitivity_no_outliers')
    plot_distribution(pd_values, 'specificity_no_outliers')

    plt.show()

    """Get the data to use for the interval MC simulation"""
    p_box_levy_l = mc_simulation_interval_data('levy_l')

    """Save the parameters for the lower and upper bound cdf for the levy l"""
    write_binary_files('binary_files/p_boxes/levy_l_p_boxes.pk', p_box_levy_l)
