import pickle as pk

import matplotlib.pyplot as plt
import numpy as np

from EDA.functions import normalization

from functions import (simulation, inverse_p_box_lower, inverse_p_box_upper, inverse_p_box_lower_a_b_loc,
                       inverse_p_box_upper_a_b_loc, calculate_epsilon, filtering)
from variables import fix_rate_values, break_rate_values, colors

from scipy import stats

def plot_prevalence_rate(simulation_type, upper_file, fix_rates, break_rates, lower_file):
    fig, ax = plt.subplots(1, 1)

    for fix_rate in fix_rates:
        for break_rate in break_rates:
            filtered_df_upper = filtering(simulation_type, fix_rate, break_rate, upper_file)
            filtered_df_lower = filtering(simulation_type, fix_rate, break_rate, lower_file)

            prev_rate_first_upper = stats.ecdf(filtered_df_upper['prevalence_rate_first_analyzer'])
            prev_rate_first_lower = stats.ecdf(filtered_df_lower['prevalence_rate_first_analyzer'])

            prev_rate_second_upper = stats.ecdf(filtered_df_upper['prevalence_rate_second_analyzer'])
            prev_rate_second_lower = stats.ecdf(filtered_df_lower['prevalence_rate_second_analyzer'])

            ax.plot(prev_rate_first_upper.cdf.quantiles, prev_rate_first_upper.cdf.probabilities,
                    label="CDF Prevalence Rate First Analyzer Upper")
            ax.plot(prev_rate_first_lower.cdf.quantiles, prev_rate_first_lower.cdf.probabilities,
                    label="CDF Prevalence Rate First Analyzer Lower")

            ax.plot(prev_rate_second_upper.cdf.quantiles, prev_rate_second_upper.cdf.probabilities,
                    label="CDF Prevalence Rate Second Analyzer Upper")
            ax.plot(prev_rate_second_lower.cdf.quantiles, prev_rate_second_lower.cdf.probabilities,
                    label="CDF Prevalence Rate Second Analyzer Lower")

            fig.suptitle(f"CDF Prevalence Rate Fix Rate: {fix_rate} Break Rate: {break_rate}")
            plt.legend()

    plt.show()

def prevalence_rate(simulation_type, upper_file, lower_file):

    for fix_rate in fix_rate_values:
        for break_rate in break_rate_values:
            print(f"\nFix rate: {fix_rate}, Break rate: {break_rate}")
            filtered_df_upper = filtering(simulation_type, fix_rate, break_rate, upper_file)
            filtered_df_lower = filtering(simulation_type, fix_rate, break_rate, lower_file)

            print(f"Lower first: {round(filtered_df_lower['prevalence_rate_first_analyzer'].mean(axis=0), 3)}, "
                  f"Lower second: {round(filtered_df_lower['prevalence_rate_second_analyzer'].mean(axis=0), 3)}")

            print(f"Upper first: {round(filtered_df_upper['prevalence_rate_first_analyzer'].mean(axis=0), 3)}, "
                  f"Upper second: {round(filtered_df_upper['prevalence_rate_second_analyzer'].mean(axis=0), 3)}")


def p_box_simulation(simulation_type, file_upper, file_lower, rounds):

    with open('../EDA/binary_files/p_boxes/p_boxes_parameters_spec.pk', 'rb') as f:
        parameters = pk.load(f)

    print(parameters)
    p_list = stats.uniform.rvs(loc=0, scale=1, size=20, random_state=42)
    epsilons = calculate_epsilon(0, 1, parameters['data_loc_spec'], parameters['data_var_spec'])
    print(epsilons)

    specificity_values_upper_bound = inverse_p_box_upper(0.00, 1.00, parameters['data_loc_spec'],
                                                         parameters['data_var_spec'],  p_list, epsilons['epsilon2'])
    specificity_values_lower_bound = inverse_p_box_lower(0.00, 1.00, parameters['data_loc_spec'],
                                                         parameters['data_var_spec'], p_list, epsilons['epsilon1'])


    print(specificity_values_upper_bound)
    print(specificity_values_lower_bound)

    simulation(simulation_type, file_upper, rounds, specificity_values_upper_bound, fix_rate_values, break_rate_values)
    simulation(simulation_type, file_lower, rounds, specificity_values_lower_bound, fix_rate_values, break_rate_values)

def see_results_p_box(simulation_type, upper_file, lower_file):

    print("\nLet's see the first prevalence rate after the first analyzer and second analyzer")
    prevalence_rate(simulation_type, upper_file, lower_file)

    fix_rates = fix_rate_values[0:1]
    break_rates = break_rate_values[0:1]

    plot_prevalence_rate(simulation_type, upper_file, fix_rates, break_rates, lower_file)