import first_analyzer.first_analyzer as first_analyzer
import fixer.fixer as fixer
import second_analyzer.second_analyzer as second_analyzer

import csv
import pandas as pd

import random

def filtering(simulation_type, fix_rate, break_rate, file):

    print()

    pd_values = pd.read_csv(f'results/{simulation_type}/{file}')
    filtered_df = pd_values[(pd_values['fix_rate'] == fix_rate) & (pd_values['break_rate'] == break_rate)]

    return filtered_df


def calculate_epsilon(a, b, loc, variance):
    epsilon1 = loc - (variance / (b - loc))
    epsilon2 = loc + (variance / (loc - a))

    return {'epsilon1': epsilon1, 'epsilon2': epsilon2}

def exact_formulas(N, prev_rate, sensitivity, specificity, fix_rate):

    print(f"Fix rate: {fix_rate}, Break rate: 0\n"
          f"Sensitivity: {sensitivity}, Specificity: {specificity}\n")

    x = N * prev_rate
    y = N * (1 - prev_rate)

    print(f"vulnerable: {x}, not vulnerable: {y}")

    TP_start = x * sensitivity
    FN_start = x * (1 - sensitivity)

    TN_start = y * specificity
    FP_start = y * (1 - specificity)

    TP_end = (1 - fix_rate) * TP_start * sensitivity
    FN_end = FN_start + (1 - fix_rate) * TP_start * (1 - sensitivity)

    TN_end = (fix_rate * TP_start + FP_start) * specificity + TN_start
    FP_end = (fix_rate * TP_start + FP_start) * (1 - specificity)

    return TP_start, FN_start, TN_start, FP_start, TP_end, FN_end, TN_end, FP_end

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


def operation(n1, n2):

    if n1 == 0 and n2 == 0:
        return 0
    elif n1 == 0 or n2 == 0:
        return 200

    return round(abs((n1 - n2) / ((n1 + n2) / 2)) * 100, 0)


def simulation(simulation_type, file, rounds, specificity_values, sensitivity_values,
               fix_rate_values, break_rate_values, not_const, first_prev_rate):

    header = False
    write_mode = 'w'

    # Here we create the couples of sensitivity and specificity
    sensitivity_specificity_couples = list(zip(sensitivity_values, specificity_values))

    for round in range(rounds):
        for i, (sensitivity, specificity) in enumerate(sensitivity_specificity_couples):
            for fix_rate in fix_rate_values:
                for break_rate in break_rate_values:
                    tot, p_init, n_init, pw_init, nw_init, tp1, fp1, tn1, fn1 = first_analyzer.first_analyzer(
                        sensitivity, specificity, not_const, first_prev_rate)

                    (p_infix, n_infix, pw_infix, nw_infix, p_outfix, n_outfix, pw_outfix, nw_outfix, num_magic,
                     not_vulnerable, still_vulnerable, num_magic_special_case, num_magic_special_case_1, ignored) = (
                        fixer.fixer(fix_rate, break_rate))

                    p_out, n_out, pw_out, nw_out, tp2, fp2, tn2, fn2, through_fixer, vulnerable, not_vuln = (
                        second_analyzer.second_analyzer(sensitivity, specificity, not_const, first_prev_rate))

                    tp_out = tp2
                    fp_out = fp2
                    tn_out = tn1 + tn2
                    fn_out = fn1 + fn2

                    # Here we calculate the final accuracy, precision and sensitivity
                    accuracy_out = (tp_out + tn_out) / (tp_out + fp_out + tn_out + fn_out)
                    precision_out = tp_out / (tp_out + fp_out) if (tp_out + fp_out) != 0 else "err"
                    sensitivity_out = tp1 / (tp1 + fn1) if (tp1 + fn1) != 0 else "err"
                    specificity_out = tn1 / (tn1 + fp1) if (tn1 + fp1) != 0 else "err"

                    if sensitivity_out != "err" and specificity_out != "err":
                        ppv_value = (sensitivity_out * first_prev_rate) / ((sensitivity_out * first_prev_rate) + (1 - specificity_out) * (1 - first_prev_rate))
                        npv_value = (specificity_out * (1 - first_prev_rate)) / (specificity_out * (1 - first_prev_rate) + (1 - sensitivity_out) * first_prev_rate)
                    else:
                        ppv_value, npv_value = 0, 0

                    tp_out_adj = (tp_out + fp_out) * ppv_value
                    fp_out_adj = (tp_out + fp_out) * (1 - ppv_value)

                    tn_out_adj = (tn_out + fn_out) * npv_value
                    fn_out_adj = (tn_out + fn_out) * (1 - npv_value)

                    final_prev_rate_adj = (tp_out_adj + fn_out_adj) / (tp_out_adj + fn_out_adj + tn_out_adj + fp_out_adj)
                    prev_rate_div_adj = final_prev_rate_adj / first_prev_rate
                    real_fix_rate_adj = 1 - prev_rate_div_adj

                    fn_1_rate = fn1 / (tp1 + fn1) if (tp1 + fn1) != 0 else "err"
                    fn_out_rate = fn_out / (tp_out + fn_out) if (tp_out + fn_out) != 0 else "err"

                    # Here we calculate the division between the false negatives after the first analyzer
                    # and the false negatives after the second analyzer
                    fn_div = fn_out / fn1 if fn1 != 0 else "err"
                    fn_div_rate = fn_out_rate / fn_1_rate if fn_1_rate != 0 else "err"

                    # Here we calculate the final prevalence rate, and then we divide the final prevalence rate
                    # by the prevalence rate given at the beginning (vulnerable rate)
                    final_prev_rate = (tp_out + fn_out) / (tp_out + fn_out + tn_out + fp_out)
                    prev_rate_div = final_prev_rate / first_prev_rate

                    # Real fix rate
                    real_fix_rate = 1 - prev_rate_div

                    with open(f'results/{simulation_type}/{file}', write_mode,
                              encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)

                        if not header:
                            header = ["first_prev_rate", "final_prev_rate", "prev_rate_div",
                                      "fn_div", "fn_rate_first", "fn_rate_final", "fn_div_rate",
                                      "real_fix_rate", "work_rate", "sensitivity", "specificity", "fix_rate",
                                      "break_rate", "tot", "Pinit", "Ninit", "PWinit", "NWinit",
                                      "TP1", "FP1", "TN1", "FN1",
                                      "Pinfix", "Ninfix", "PWinfix", "NWinfix",
                                      "Poutfix", "Noutfix", "PWoutfix", "NWoutfix", "num_magic", "not_vulnerable", "still_vulnerable", "num_magic_special", "num_magic_special_1", "ignored",
                                      "TP2", "FP2", "TN2", "FN2", "through_fixer", "vulnerable", "not_vuln",
                                      "Pout", "Nout", "PWout", "NWout",
                                      "TPout", "FPout", "TNout", "FNout",
                                      "ppv_value", "npv_value",
                                      "TPoutadj", "FPoutadj", "TNoutadj", "FNoutadj",
                                      "final_prev_rate_adj", "prev_rate_div_adj", "real_fix_rate_adj",
                                      "Accuracy", "Precision", "Sensitivity", "Specificity"]

                            writer.writerow(header)
                            header = True
                            write_mode = 'a'

                        data = [first_prev_rate, final_prev_rate, prev_rate_div,
                                fn_div, fn_1_rate, fn_out_rate, fn_div_rate,
                                real_fix_rate, 1, sensitivity, specificity, fix_rate,
                                break_rate, tot, p_init, n_init, pw_init, nw_init,
                                tp1, fp1, tn1, fn1,
                                p_infix, n_infix, pw_infix, nw_infix,
                                p_outfix, n_outfix, pw_outfix, nw_outfix, num_magic, not_vulnerable, still_vulnerable, num_magic_special_case, num_magic_special_case_1, ignored,
                                tp2, fp2, tn2, fn2, through_fixer, vulnerable, not_vuln,
                                p_out, n_out, pw_out, nw_out,
                                tp_out, fp_out, tn_out, fn_out,
                                ppv_value, npv_value,
                                tp_out_adj, fp_out_adj, tn_out_adj, fn_out_adj,
                                final_prev_rate_adj, prev_rate_div_adj, real_fix_rate_adj,
                                accuracy_out, precision_out, sensitivity_out, specificity_out]

                        writer.writerow(data)