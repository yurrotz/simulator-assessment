import first_analyzer.first_analyzer as first_analyzer
import fixer.fixer as fixer
import second_analyzer.second_analyzer as second_analyzer

import csv
import pandas as pd
from variables import r

import random

def filtering(simulation_type, fix_rate, break_rate, file):

    pd_values = pd.read_csv(f'results/{simulation_type}/{file}')
    filtered_df = pd_values[(pd_values['fix_rate'] == fix_rate) & (pd_values['break_rate'] == break_rate)]

    return filtered_df


def calculate_epsilon(a, b, loc, variance):
    epsilon1 = loc - (variance / (b - loc))
    epsilon2 = loc + (variance / (loc - a))

    return {'epsilon1': epsilon1, 'epsilon2': epsilon2}


"""
def p_box_lower(a, b, loc, variance, x, epsilon1, epsilon2):
    if x < epsilon1:
        return 0
    elif epsilon1 <= x < epsilon2:
        return (variance + (b - loc) * (x - loc))/((b - a) * (x - a))
    elif epsilon2 <= x < b:
        return pow((x - loc), 2)/(pow((x - loc), 2) + variance)
    elif b <= x:
        return 1
"""

"""
def p_box_upper(a, b, loc, variance, x, epsilon1, epsilon2):
    if x < a:
        return 0
    elif a <= x < epsilon1:
        return variance / (pow((loc - x), 2) + variance)
    elif epsilon1 <= x < epsilon2:
        return ((b - loc) * (b - a + loc - x) - variance)/((b - a) * (b - x))
    elif epsilon2 <= x:
        return 1
"""

def inverse_p_box_lower_a_b_loc(a, b, loc, p_list):
    x_list = []

    for p in p_list:
        if p == 0:
            val = random.uniform(a, loc)
            x_list.append(val)
        elif 0 < p < ((b - loc)/(b - a)):
            val = (p * a - loc) / (p - 1)
            x_list.append(val)
        elif ((b - loc) / (b - a)) <= p <= 1:
            val = b
            x_list.append(val)

    return x_list

def inverse_p_box_upper_a_b_loc(a, b, loc, p_list):

    x_list = []

    for p in p_list:
        if 0 <= p <= ((b - loc)/(b - a)):
            val = a
            x_list.append(val)
        elif ((b - loc)/(b - a)) < p < 1:
            val = b - ((b - loc)/p)
            x_list.append(val)
        elif p == 1:
            val = random.uniform(loc, b)
            x_list.append(val)

    return x_list

def inverse_p_box_lower(a, b, loc, variance, p_list, epsilon1):

    x_list = []

    for p in p_list:
        if p == 0:
            val = random.uniform(a, epsilon1)
            x_list.append(val)
        elif 0 < p <= ((variance * (b - loc) * (variance / (loc - a)))/((b - a) * (loc - a + (variance / (loc - a))))):
            val = ((p * a * (b - a) - loc * (b - loc) + variance)/(p * (b - a) - (b - loc)))
            x_list.append(val)
        elif ((variance * (b - loc) * (variance / (loc - a)))/((b - a) * (loc - a + (variance / (loc - a))))) <= p < 1:
            val = loc + pow(((p * variance)/(1 - p)), 0.5)
            if val > 1:
                print(f"Val: {val}, p: {p}, limit: {(variance * (b - loc) * (variance / (loc - a)))/((b - a) * (loc - a + (variance / (loc - a))))}")
            x_list.append(val)
        elif p == 1:
            val = b
            x_list.append(val)

    return x_list

def inverse_p_box_upper(a, b, loc, variance, p_list, epsilon2):

    x_list = []

    for p in p_list:
        if p == 0:
           val = a
           x_list.append(val)
        elif 0 < p <= (variance / (pow((variance / (b - loc)), 2) + variance)):
            val = loc - pow(((variance * (1 - p))/p), 0.5)
            x_list.append(val)
        elif (variance / (pow((variance / (b - loc)), 2) + variance)) < p < 1:
            val = ((b - loc) * (b - a + loc) - variance - p * b * (b - a))/((b - loc) - p * (b - a))
            x_list.append(val)
        elif p == 1:
            val = random.uniform(epsilon2, b)
            x_list.append(val)

    return x_list

"""
def inverse_p_box_lower(a, b, loc, variance, p_list, epsilon1):

    x_list = []
    for p in p_list:
        if p == 0:
            x_list.append(random.uniform(a, epsilon1))

        elif 0 < p <= (variance * (b - loc) * variance / (loc - a))/((b - a) * (loc - a + variance/(loc - a))):
            x_list.append((p * a * (b - a) - loc * (b - loc) + variance)/(p * (b - a) - (b - loc)))

        elif (variance * (b - loc) * variance / (loc - a))/((b - a) * (loc - a + variance / (loc - a))) < p < 1:
            if loc + pow((p * variance) / (1 - p), 0.5) > 1:
                print("Hey lower")
                print(pow((p * variance) / (1 - p), 0.5))
                print(loc + pow((p * variance) / (1 - p), 0.5))
                print(p)
                print((variance * (b - loc) * variance / (loc - a)) / ((b - a) * (loc - a + variance / (loc - a))))

            x_list.append(loc + pow((p * variance) / (1 - p), 0.5))

        elif p == 1:
            x_list.append(b)

    return x_list


def inverse_p_box_upper(a, b, loc, variance, p_list, epsilon2):

    x_list = []
    for p in p_list:
        if p == 0:
            x_list.append(a)

        elif 0 < p <= (variance / ((pow(variance, 2)/pow((b - loc), 2)) + variance)):
            if loc - pow(variance * (1 - p)/p, 0.5) < 0:
                print("Hey upper")
                print(pow(variance * (1 - p)/p, 0.5))
                print(loc - pow(variance * (1 - p)/p, 0.5))
                print(p)
                print(variance / ((pow(variance, 2)/pow((b - loc), 2)) + variance))

            x_list.append(loc - pow(variance * (1 - p)/p, 0.5))

        elif (variance / (pow(variance / (b - loc), 2) + variance)) < p < 1:
            x_list.append(((b - loc) * (b - a + loc) - variance - p * b * (b - a))/((b - loc) - p * (b  - a)))

        elif p == 1:
            x_list.append(random.uniform(epsilon2, b))

    return x_list
"""

def simulation(simulation_type, file, rounds, specificity_values, fix_rate_values, break_rate_values):

    header = False
    write_mode = 'w'

    for round in range(rounds):
        print("Round: " + str(round))

        for i, specificity in enumerate(specificity_values):
            print(f"\nSpecificity: {specificity}, {i} ")
            sensitivity = pow(1 - specificity, 1 - r)
            print(f"\nSensitivity: {sensitivity}, {i}")

            for fix_rate in fix_rate_values:
                print("Fix rate: ", fix_rate)

                for break_rate in break_rate_values:
                    print("Break rate: ", break_rate)

                    tot, p_init, n_init, pw_init, nw_init, tp1, fp1, tn1, fn1 = first_analyzer.first_analyzer(
                        sensitivity, specificity)

                    prevalence_rate_first_analyzer = tp1 / (tp1 + fp1 + tn1 + fn1)

                    p_infix, n_infix, pw_infix, nw_infix, p_outfix, n_outfix, pw_outfix, nw_outfix = fixer.fixer(
                        fix_rate, break_rate)

                    p_out, n_out, pw_out, nw_out, tp2, fp2, tn2, fn2 = second_analyzer.second_analyzer(
                        sensitivity, specificity)

                    tp_out = tp2
                    fp_out = fp2
                    tn_out = tn1 + tn2
                    fn_out = fn1 + fn2

                    accuracy_out = (tp_out + tn_out) / (tp_out + fp_out + tn_out + fn_out)

                    if (tp_out + fp_out) != 0:
                        precision_out = tp_out / (tp_out + fp_out)
                    else:
                        precision_out = "err"

                    if (tp_out + fn_out) != 0:
                        sensitivity_out = tp_out / (tp_out + fn_out)
                    else:
                        sensitivity_out = "err"

                    prevalence_rate_second_analyzer = tp_out / (tp_out + fn_out + tn_out + fp_out)

                    with open(f'results/{simulation_type}/{file}', write_mode,
                              encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)

                        if not header:
                            header = ["prevalence_rate_first_analyzer", "prevalence_rate_second_analyzer", "work_rate",
                                      "sensitivity", "specificity", "fix_rate", "break_rate",
                                      "tot", "Pinit", "Ninit", "PWinit", "NWinit",
                                      "TP1", "FP1", "TN1", "FN1",
                                      "Pinfix", "Ninfix", "PWinfix", "NWinfix",
                                      "Poutfix", "Noutfix", "PWoutfix", "NWoutfix",
                                      "TP2", "FP2", "TN2", "FN2",
                                      "Pout", "Nout", "PWout", "NWout",
                                      "TPout", "FPout", "TNout", "FNout",
                                      "Accuracy", "Precision", "Sensitivity"]

                            writer.writerow(header)
                            header = True
                            write_mode = 'a'

                        data = [prevalence_rate_first_analyzer, prevalence_rate_second_analyzer, 0, sensitivity,
                                specificity, fix_rate, break_rate, tot, p_init, n_init, pw_init, nw_init, tp1, fp1, tn1,
                                fn1, p_infix, n_infix, pw_infix, nw_infix, p_outfix, n_outfix, pw_outfix, nw_outfix,
                                tp2, fp2, tn2, fn2, p_out, n_out, pw_out, nw_out, tp_out, fp_out, tn_out, fn_out,
                                accuracy_out, precision_out, sensitivity_out]

                        writer.writerow(data)