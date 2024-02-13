import pickle as pk

import matplotlib.pyplot as plt
import numpy as np

from functions import simulation, inverse_p_box_lower_a_b_loc, inverse_p_box_upper_a_b_loc, filtering
from variables import fix_rate_values, break_rate_values, colors

from scipy import stats

def plot_prevalence_rate(simulation_type, fix_rates, break_rates, upper_file, lower_file):
    fig, ax = plt.subplots(1, 1)

    for fix_rate in fix_rates:
        for break_rate in break_rates:
            filtered_df_upper = filtering(simulation_type, fix_rate, break_rate, upper_file)
            filtered_df_lower = filtering(simulation_type, fix_rate, break_rate, lower_file)

            prev_rate_second_upper = stats.ecdf(filtered_df_upper['final_prev_rate'])
            prev_rate_second_lower = stats.ecdf(filtered_df_lower['final_prev_rate'])

            prev_rate_div_upper = stats.ecdf(filtered_df_upper['prev_rate_div'])
            prev_rate_div_lower = stats.ecdf(filtered_df_lower['prev_rate_div'])

            ax.plot(prev_rate_second_upper.cdf.quantiles, prev_rate_second_upper.cdf.probabilities,
                    label="CDF Final Prevalence Rate Upper")
            ax.plot(prev_rate_second_lower.cdf.quantiles, prev_rate_second_lower.cdf.probabilities,
                    label="CDF Final Prevalence Rate Lower")

            ax.plot(prev_rate_div_upper.cdf.quantiles, prev_rate_div_upper.cdf.probabilities,
                    label="CDF Prev Rate Div Upper")
            ax.plot(prev_rate_div_lower.cdf.quantiles, prev_rate_div_lower.cdf.probabilities,
                    label="CDF Prev Rate Div Lower")

            fig.suptitle(f"CDF Prevalence Rate \n Fix Rate: {fix_rate} Break Rate: {break_rate}")
            plt.legend()

    plt.show()

def plot_real_fix_rate(simulation_type, fix_rates, break_rates, upper_file, lower_file):
    fig, ax = plt.subplots(1, 1)

    for fix_rate in fix_rates:
        for break_rate in break_rates:
            filtered_df_upper = filtering(simulation_type, fix_rate, break_rate, upper_file)
            filtered_df_lower = filtering(simulation_type, fix_rate, break_rate, lower_file)

            fix_rate_upper = stats.ecdf(filtered_df_upper['real_fix_rate'])
            fix_rate_lower = stats.ecdf(filtered_df_lower['real_fix_rate'])

            ax.plot(fix_rate_upper.cdf.quantiles, fix_rate_upper.cdf.probabilities,
                    label="CDF Real Fix Rate upper")
            ax.plot(fix_rate_lower.cdf.quantiles, fix_rate_lower.cdf.probabilities,
                    label="CDF Real Fix Rate lower")

            fig.suptitle(f"CDF Real Fix Rate \n Fix Rate: {fix_rate} Break Rate: {break_rate}")
            plt.legend()

    plt.show()

def prevalence_rate(simulation_type, upper_file, lower_file):

    for fix_rate in fix_rate_values:
        for break_rate in break_rate_values[0:1]:
            print(f"\nFix rate: {fix_rate}, Break rate: {break_rate}")
            filtered_df_lower = filtering(simulation_type, fix_rate, break_rate, lower_file)
            filtered_df_upper = filtering(simulation_type, fix_rate, break_rate, upper_file)

            prev_rate_lower = filtered_df_lower['prev_rate_div'].min(axis=0)
            prev_rate_upper = filtered_df_upper['prev_rate_div'].max(axis=0)

            print(
                f"Div PR lower: {round(prev_rate_lower, 2)}",
                f" Real FR lower: {round(filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['real_fix_rate'].iloc[0], 2)}"
                f" First PR: {round(filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['first_prev_rate'].iloc[0], 2)}"
                f" Final PR lower: {round(filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['final_prev_rate'].iloc[0], 2)}")


            print(
                f"Div PR upper: {round(prev_rate_upper, 2)}",
                f" Real FR upper: {round(filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['real_fix_rate'].iloc[0], 2)}"
                f" First PR: {round(filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['first_prev_rate'].iloc[0], 2)}"
                f" Final PR upper: {round(filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['final_prev_rate'].iloc[0], 2)}")


def false_negative_rate(simulation_type, upper_file, lower_file):
    for fix_rate in fix_rate_values:
        for break_rate in break_rate_values[0:1]:
            print(f"\nFix rate: {fix_rate}, Break rate: {break_rate}")
            filtered_df_lower = filtering(simulation_type, fix_rate, break_rate, lower_file)
            filtered_df_upper = filtering(simulation_type, fix_rate, break_rate, upper_file)

            fn_rate_div_lower = filtered_df_lower['fn_div_rate'].min(axis=0)
            fn_rate_div_upper = filtered_df_upper['fn_div_rate'].max(axis=0)

            print(
                f"FN division lower: {filtered_df_lower[(filtered_df_lower['fn_div_rate'] == fn_rate_div_lower)]['fn_div'].iloc[0]}",
                f"FN division upper: {filtered_df_upper[(filtered_df_upper['fn_div_rate'] == fn_rate_div_upper)]['fn_div'].iloc[0]}")

               # f"FN division lower: {filtered_df_lower['fn_div'].min(axis=0)}",
               # f"FN division upper: {filtered_df_upper['fn_div'].max(axis=0)}")

            print(
                f"FN rate division lower: {fn_rate_div_lower}",
                f" First FN rate lower: {filtered_df_lower[(filtered_df_lower['fn_div_rate'] == fn_rate_div_lower)]['fn_rate_first'].iloc[0]}",
                f" Final FN rate lower: {filtered_df_lower[(filtered_df_lower['fn_div_rate'] == fn_rate_div_lower)]['fn_rate_final'].iloc[0]}")

            print(
                f"FN rate division upper: {fn_rate_div_upper}",
                f" First FN upper: {filtered_df_upper[(filtered_df_upper['fn_div_rate'] == fn_rate_div_upper)]['fn_rate_first'].iloc[0]}",
                f" Final FN upper: {filtered_df_upper[(filtered_df_upper['fn_div_rate'] == fn_rate_div_upper)]['fn_rate_final'].iloc[0]}"
            )


def p_box_simulation(simulation_type, file_upper, file_lower, rounds, first_prev_rate):

    with open('../EDA/binary_files/p_boxes/p_boxes_parameters_sens_1.pk', 'rb') as f:
        par_sens = pk.load(f)

    print("The parameters are: ", par_sens)

    with open('../EDA/binary_files/p_boxes/p_boxes_parameters_spec.pk', 'rb') as f:
        par_spec = pk.load(f)

    p_list = stats.uniform.rvs(loc=0, scale=1, size=25, random_state=1234)

    sensitivity_values_upper_bound = inverse_p_box_upper_a_b_loc(par_sens['data_min_sens'], par_sens['data_max_sens'], 
                                                                 par_sens['data_loc_sens'], p_list)
    sensitivity_values_lower_bound = inverse_p_box_lower_a_b_loc(par_sens['data_min_sens'],  par_sens['data_max_sens'], 
                                                                 par_sens['data_loc_sens'], p_list)

    specificity_values_upper_bound = list(np.zeros(25))
    specificity_values_lower_bound = list(np.zeros(25))

    """
    specificity_values_upper_bound = inverse_p_box_upper_a_b_loc(par_spec['data_min_spec'], par_spec['data_max_spec'],
                                                                 par_spec['data_loc_spec'], p_list)
    specificity_values_lower_bound = inverse_p_box_lower_a_b_loc(par_spec['data_min_spec'], par_spec['data_max_spec'],
                                                                 par_spec['data_loc_spec'], p_list)
    """

    simulation(simulation_type, file_upper, rounds, specificity_values_upper_bound, sensitivity_values_upper_bound,
               fix_rate_values, break_rate_values[0:1], first_prev_rate)
    simulation(simulation_type, file_lower, rounds, specificity_values_lower_bound, sensitivity_values_lower_bound,
               fix_rate_values, break_rate_values[0:1], first_prev_rate)

def see_results_p_box(simulation_type, upper_file, lower_file):


    print("\nLet's see the prevalence rate")
    prevalence_rate(simulation_type, upper_file, lower_file)

    print("\nLet's see the false negative rate")
    false_negative_rate(simulation_type, upper_file, lower_file)

    # Plotting

    """
    fix_rates = fix_rate_values[0:1]
    break_rates = break_rate_values[0:1]

    plot_prevalence_rate(simulation_type, fix_rates, break_rates, upper_file, lower_file)
    plot_real_fix_rate(simulation_type, fix_rates, break_rates, upper_file, lower_file)
    """