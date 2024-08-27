import pickle as pk

import matplotlib.pyplot as plt
import numpy as np

from functions import simulation, inverse_p_box_lower_a_b_loc, inverse_p_box_upper_a_b_loc, filtering
from variables import fix_rate_values, break_rate_values, colors
import pba

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

def prevalence_rate(simulation_type, upper_file, lower_file, not_const):

    for fix_rate in fix_rate_values:
        for break_rate in break_rate_values[0:1]:
            print(f"\nFIX RATE: {fix_rate}, BREAK RATE: {break_rate}")
            filtered_df_lower = filtering(simulation_type, fix_rate, break_rate, lower_file)
            filtered_df_upper = filtering(simulation_type, fix_rate, break_rate, upper_file)

            prev_rate_lower = filtered_df_lower['prev_rate_div'].min(axis=0)
            prev_rate_upper = filtered_df_upper['prev_rate_div'].max(axis=0)

            print(
                f"First PR: {round(filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['first_prev_rate'].iloc[0], 2)}"
                f" Final PR lower: {round(filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['final_prev_rate'].iloc[0], 2)}"
                f" Final PR lower adj: {round(filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['final_prev_rate_adj'].iloc[0], 2)}"
                f" Div PR lower: {prev_rate_lower}",
                f" Real FR lower: {round(filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['real_fix_rate'].iloc[0], 2)}"
                f" Fix rate adj: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['real_fix_rate_adj'].iloc[0]}\n"
                
                f"sensitivity: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['sensitivity'].iloc[0]}"
                f" specificity: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['specificity'].iloc[0]}\n"
                
                f"Sensitivity_out: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['Sensitivity'].iloc[0]}"
                f" Specificity_out: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['Specificity'].iloc[0]}\n"
                
                f"TP1: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['TP1'].iloc[0]}"
                f" FN1: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['FN1'].iloc[0]}"
                f" TN1: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['TN1'].iloc[0]}"
                f" FP1: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['FP1'].iloc[0]}\n"
                
                f"Poutfix: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['Poutfix'].iloc[0]}"
                f" Noutfix: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['Noutfix'].iloc[0]}"
                f" PWoutfix: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['PWoutfix'].iloc[0]}"
                f" NWoutfix: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['NWoutfix'].iloc[0]}\n"
                
                f"Magic number: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['num_magic'].iloc[0]}"
                f" Magic number fixed: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['not_vulnerable'].iloc[0]}"
                f" Magic number not fixed: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['still_vulnerable'].iloc[0]}"
                f" special case: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['num_magic_special'].iloc[0]}"
                f" special case 1: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['num_magic_special_1'].iloc[0]}"
                f" ignored: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['ignored'].iloc[0]}\n"
                
                f"Through fixer: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['through_fixer'].iloc[0]}"
                f" vulnerable: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['vulnerable'].iloc[0]}"
                f" not vuln: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['not_vuln'].iloc[0]}\n"
                
                f"TP2: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['TP2'].iloc[0]}"
                f" FN2: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['FN2'].iloc[0]}"
                f" TN2: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['TN2'].iloc[0]}"
                f" FP2: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['FP2'].iloc[0]}\n"
                
                f"TPout: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['TPout'].iloc[0]}"
                f" FNout: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['FNout'].iloc[0]}"
                f" TNout: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['TNout'].iloc[0]}"
                f" FPout: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['FPout'].iloc[0]}\n"
                
                f"ppv: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['ppv_value'].iloc[0]}"
                f" npv: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['npv_value'].iloc[0]}\n")

            if not not_const:
                print(
                    # f"ppv: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['ppv_value'].iloc[0]}"
                    # f" npv: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['npv_value'].iloc[0]}\n"
                    
                    f"TPoutadj: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['TPoutadj'].iloc[0]}"
                    f" FPoutadj: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['FPoutadj'].iloc[0]}"
                    f" TNoutadj: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['TNoutadj'].iloc[0]}"
                    f" FNoutadj: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['FNoutadj'].iloc[0]}\n")
                
                    # f"Fix rate adj: {filtered_df_lower[(filtered_df_lower['prev_rate_div'] == prev_rate_lower)]['real_fix_rate_adj'].iloc[0]}")

            print("\n")
            print(
                f"First PR: {round(filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['first_prev_rate'].iloc[0], 2)}"
                f" Final PR upper: {round(filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['final_prev_rate'].iloc[0], 2)}"
                f" Final PR upper adj: {round(filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['final_prev_rate_adj'].iloc[0], 2)}"
                f" Div PR upper: {prev_rate_upper}",
                f" Real FR upper: {round(filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['real_fix_rate'].iloc[0], 2)}"
                f" Fix rate adj: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['real_fix_rate_adj'].iloc[0]}\n"

                
                f"sensitivity: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['sensitivity'].iloc[0]}"
                f" specificity: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['specificity'].iloc[0]}\n"
                
                f"Sensitivity_out: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['Sensitivity'].iloc[0]}"
                f" Specificity_out: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['Specificity'].iloc[0]}\n"
                
                f"TP1: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['TP1'].iloc[0]}"
                f" FN1: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['FN1'].iloc[0]}"
                f" TN1: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['TN1'].iloc[0]}"
                f" FP1: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['FP1'].iloc[0]}\n"
                
                f"Poutfix: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['Poutfix'].iloc[0]}"
                f" Noutfix: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['Noutfix'].iloc[0]}"
                f" PWoutfix: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['PWoutfix'].iloc[0]}"
                f" NWoutfix: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['NWoutfix'].iloc[0]}\n"
                
                f"Magic number: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['num_magic'].iloc[0]}"
                f" Magic number fixed: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['not_vulnerable'].iloc[0]}"
                f" Magic number not fixed: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['still_vulnerable'].iloc[0]}"
                f" special case: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['num_magic_special'].iloc[0]}"
                f" special case 1: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['num_magic_special_1'].iloc[0]}"
                f" ignored: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['ignored'].iloc[0]}\n"
                
                f"Through fixer: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['through_fixer'].iloc[0]}"
                f" vulnerable: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['vulnerable'].iloc[0]}"
                f" not vuln: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['not_vuln'].iloc[0]}\n"
                
                f"TP2: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['TP2'].iloc[0]}"
                f" FN2: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['FN2'].iloc[0]}"
                f" TN2: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['TN2'].iloc[0]}"
                f" FP2: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['FP2'].iloc[0]}\n"
                
                f"TPout: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['TPout'].iloc[0]}"
                f" FNout: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['FNout'].iloc[0]}"
                f" TNout: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['TNout'].iloc[0]}"
                f" FPout: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['FPout'].iloc[0]}\n"
                
                f"ppv: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['ppv_value'].iloc[0]}"
                f" npv: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['npv_value'].iloc[0]}\n")

            if not not_const:
                print(
                    # f"ppv: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['ppv_value'].iloc[0]}"
                    # f" npv: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['npv_value'].iloc[0]}\n"
                    
                    f"TPoutadj: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['TPoutadj'].iloc[0]}"
                    f" FPoutadj: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['FPoutadj'].iloc[0]}"
                    f" TNoutadj: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['TNoutadj'].iloc[0]}"
                    f" FNoutadj: {filtered_df_upper[(filtered_df_upper['prev_rate_div'] == prev_rate_upper)]['FNoutadj'].iloc[0]}\n")

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

            print(
                f"FN rate division lower: {fn_rate_div_lower}",
                f" First FN rate lower: {filtered_df_lower[(filtered_df_lower['fn_div_rate'] == fn_rate_div_lower)]['fn_rate_first'].iloc[0]}",
                f" Final FN rate lower: {filtered_df_lower[(filtered_df_lower['fn_div_rate'] == fn_rate_div_lower)]['fn_rate_final'].iloc[0]}")

            print(
                f"FN rate division upper: {fn_rate_div_upper}",
                f" First FN upper: {filtered_df_upper[(filtered_df_upper['fn_div_rate'] == fn_rate_div_upper)]['fn_rate_first'].iloc[0]}",
                f" Final FN upper: {filtered_df_upper[(filtered_df_upper['fn_div_rate'] == fn_rate_div_upper)]['fn_rate_final'].iloc[0]}"
            )


def p_box_simulation(simulation_type, file_upper, file_lower, rounds, not_const, first_prev_rate):

    with open('../EDA/binary_files/p_boxes/p_boxes_parameters_sens_1.pk', 'rb') as f:
        par_sens = pk.load(f)

    print("The parameters are: ", par_sens)

    p_list = stats.uniform.rvs(loc=0, scale=1, size=25, random_state=1234)

    """
    sensitivity_values_upper_bound = inverse_p_box_upper_a_b_loc(par_sens['data_min_sens'], par_sens['data_max_sens'], 
                                                                 par_sens['data_loc_sens'], p_list)
    sensitivity_values_lower_bound = inverse_p_box_lower_a_b_loc(par_sens['data_min_sens'],  par_sens['data_max_sens'], 
                                                                 par_sens['data_loc_sens'], p_list)

    specificity_values_upper_bound = inverse_p_box_upper_a_b_loc(par_sens['data_min_sens'], par_sens['data_max_sens'],
                                                                 par_sens['data_loc_sens'], p_list)
    specificity_values_lower_bound = inverse_p_box_lower_a_b_loc(par_sens['data_min_sens'], par_sens['data_max_sens'],
                                                                 par_sens['data_loc_sens'], p_list)
    """

    sensitivity_values_upper_bound = inverse_p_box_upper_a_b_loc(0.50, 1.00, 0.75, p_list)
    sensitivity_values_lower_bound = inverse_p_box_lower_a_b_loc(0.50, 1.00, 0.75, p_list)

    specificity_values_upper_bound = inverse_p_box_upper_a_b_loc(0.50, 1.00, 0.75, p_list)
    specificity_values_lower_bound = inverse_p_box_lower_a_b_loc(0.50, 1.00, 0.75, p_list)

    print("Sensitivity values upper bound: ", sensitivity_values_upper_bound)
    print("Specificity values upper bound: ", specificity_values_upper_bound)
    print("Sensitivity values lower bound: ", sensitivity_values_lower_bound)
    print("Specificity values lower bound: ", specificity_values_lower_bound)

    simulation(simulation_type, file_upper, rounds, specificity_values_upper_bound, sensitivity_values_upper_bound,
               fix_rate_values, break_rate_values[0:1], not_const, first_prev_rate)
    simulation(simulation_type, file_lower, rounds, specificity_values_lower_bound, sensitivity_values_lower_bound,
               fix_rate_values, break_rate_values[0:1], not_const, first_prev_rate)

def p_box_simulation_2(simulation_type, file_upper, file_lower, rounds, not_const, first_prev_rate, min_sens, min_spec,
                       max_sens, max_spec):

    p_list = stats.uniform.rvs(loc=0, scale=1, size=25, random_state=1234)
    sensitivity_values_upper_bound = inverse_p_box_upper_a_b_loc(min_sens, max_sens, (min_sens + max_sens) / 2, p_list)
    sensitivity_values_lower_bound = inverse_p_box_lower_a_b_loc(min_sens, max_sens, (min_sens + max_sens) / 2, p_list)

    specificity_values_upper_bound = inverse_p_box_upper_a_b_loc(min_spec, max_spec, (min_spec + max_spec) / 2, p_list)
    specificity_values_lower_bound = inverse_p_box_lower_a_b_loc(min_spec, max_spec, (min_spec + max_spec) / 2, p_list)

    """
    # Version with the pba library, without the monte carlo simulation.
    p_box_sens_spec = pba.min_max_mean(min, max, (min + max) / 2)
    values = p_box_sens_spec.get_x()

    sensitivity_values_upper_bound, sensitivity_values_lower_bound = list(values[0]), list(values[1])
    specificity_values_upper_bound, specificity_values_lower_bound = list(values[0]), list(values[1])
    """

    print("\nSampled sensitivity and specificity values")
    print("Sensitivity values upper bound: ", sensitivity_values_upper_bound)
    print("Specificity values upper bound: ", specificity_values_upper_bound)

    print("Sensitivity values lower bound: ", sensitivity_values_lower_bound)
    print("Specificity values lower bound: ", specificity_values_lower_bound)

    simulation(simulation_type, file_upper, rounds, specificity_values_upper_bound, sensitivity_values_upper_bound,
               fix_rate_values, break_rate_values[0:1], not_const, first_prev_rate)
    simulation(simulation_type, file_lower, rounds, specificity_values_lower_bound, sensitivity_values_lower_bound,
               fix_rate_values, break_rate_values[0:1], not_const, first_prev_rate)

def see_results_p_box(simulation_type, upper_file, lower_file, not_const):


    print("\nLet's see the prevalence rate")
    prevalence_rate(simulation_type, upper_file, lower_file, not_const)

    # print("\nLet's see the false negative rate")
    # false_negative_rate(simulation_type, upper_file, lower_file)

    # Plotting

    """
    fix_rates = fix_rate_values[0:1]
    break_rates = break_rate_values[0:1]

    plot_prevalence_rate(simulation_type, fix_rates, break_rates, upper_file, lower_file)
    plot_real_fix_rate(simulation_type, fix_rates, break_rates, upper_file, lower_file)
    """