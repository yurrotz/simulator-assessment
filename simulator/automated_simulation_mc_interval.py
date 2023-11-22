import matplotlib.pyplot as plt
import pickle as pk
import pandas as pd
import numpy as np
import csv

from EDA.functions import normalization

import first_analyzer.first_analyzer as first_analyzer
import fixer.fixer as fixer
import second_analyzer.second_analyzer as second_analyzer

from scipy import stats


fixrate_values = [1]
break_rate = 0


def get_upper_lower_bound(dist_type):

    with open('../EDA/binary_files/p_boxes/levy_l_p_boxes.pk', 'rb') as f:
        p_boxes = pk.load(f)

    return p_boxes

def plot_data():
    pd_values_lower = pd.read_csv('results/mc_int_simulation/results_automated_mc_interval_lower.csv')
    pd_values_upper = pd.read_csv('results/mc_int_simulation/results_automated_mc_interval_upper.csv')

    fig, ax = plt.subplots(2, 2)

    fig.suptitle('Automated Simulation MC Interval')

    """True Negatives"""
    tn_lower = stats.ecdf(pd_values_lower['TNout'])
    ax[0, 0].plot(tn_lower.cdf.quantiles, tn_lower.cdf.probabilities, label='TNLower', color='green')

    tn_upper = stats.ecdf(pd_values_upper['TNout'])
    ax[0, 0].plot(tn_upper.cdf.quantiles, tn_upper.cdf.probabilities, label='TNUpper', color='red')

    ax[0, 0].legend()

    """False Positives"""
    fp_lower = stats.ecdf(pd_values_lower['FPout'])
    ax[0, 1].plot(fp_lower.cdf.quantiles, fp_lower.cdf.probabilities, label='FPLower', color='green')

    fp_upper = stats.ecdf(pd_values_upper['FPout'])
    ax[0, 1].plot(fp_upper.cdf.quantiles, fp_upper.cdf.probabilities, label='FPUpper', color='red')

    ax[0, 1].legend()

    """True Positives"""
    tp_lower = stats.ecdf(pd_values_lower['TPout'])
    ax[1, 0].plot(tp_lower.cdf.quantiles, tp_lower.cdf.probabilities, label='TPLower', color='blue')

    tp_upper = stats.ecdf(pd_values_upper['TPout'])
    ax[1, 0].plot(tp_upper.cdf.quantiles, tp_upper.cdf.probabilities, label='TPUpper', color='yellow')

    ax[1, 0].legend()

    """False Negatives"""
    fn_lower = stats.ecdf(pd_values_lower['FNout'])
    ax[1, 1].plot(fn_lower.cdf.quantiles, fn_lower.cdf.probabilities, label='FNLower', color='blue')

    fn_upper = stats.ecdf(pd_values_upper['FNout'])
    ax[1, 1].plot(fn_upper.cdf.quantiles, fn_upper.cdf.probabilities, label='FNUpper', color='yellow')

    ax[1, 1].legend()

    plt.savefig('figures/tp_tn_fp_fn_mc_interval.png')
    plt.show()

def simulation(specificity_values_bound, bound):

    write_mode = 'w'
    header = False

    for i, specificity in enumerate(specificity_values_bound):

        r = 0.5
        sensitivity = pow(1 - specificity, 1 - r)

        for fix_rate in fixrate_values:
            tot, p_init, n_init, pw_init, nw_init, tp1, fp1, tn1, fn1 = first_analyzer.first_analyzer(sensitivity,
                                                                                                      specificity)
            p_infix, n_infix, pw_infix, nw_infix, p_outfix, n_outfix, pw_outfix, nw_outfix = fixer.fixer(fix_rate,
                                                                                                         break_rate)
            p_out, n_out, pw_out, nw_out, tp2, fp2, tn2, fn2 = second_analyzer.second_analyzer(sensitivity,
                                                                                               specificity)

            tp_out = tp2
            fp_out = fp2
            tn_out = tn1 + tn2
            fn_out = fn1 + fn2

            accuracy_out = (tp_out + tn_out) / (tp_out + fp_out + tn_out + fn_out)

            precision_out = tp_out / (tp_out + fp_out) if (tp_out + fp_out) != 0 else "err"
            sensitivity_out = tp_out / (tp_out + fn_out) if (tp_out + fn_out) != 0 else "err"

            with open('results/mc_int_simulation/results_automated_mc_interval_{}.csv'.format(bound), write_mode,
                      encoding='UTF8', newline='') as f:
                writer = csv.writer(f)

                if not header:
                    header = ["prevalence_rate", "work_rate", "sensitivity", "specificity", "fix_rate",
                              "break_rate",
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

                data = [0.5, 0, sensitivity, specificity, fix_rate, break_rate,
                        tot, p_init, n_init, pw_init, nw_init,
                        tp1, fp1, tn1, fn1,
                        p_infix, n_infix, pw_infix, nw_infix,
                        p_outfix, n_outfix, pw_outfix, nw_outfix,
                        tp2, fp2, tn2, fn2,
                        p_out, n_out, pw_out, nw_out,
                        tp_out, fp_out, tn_out, fn_out,
                        accuracy_out, precision_out, sensitivity_out]

                writer.writerow(data)



def mc_interval():
    p_boxes = get_upper_lower_bound('levy_l')

    np.random.seed(42)

    specificity_values_upper_bound = normalization(stats.levy_l.rvs(loc=p_boxes['lower_loc'],
                                                              scale=p_boxes['lower_scale'], size=100))
    specificity_values_lower_bound = normalization(stats.levy_l.rvs(loc=p_boxes['upper_loc'],
                                                              scale=p_boxes['upper_scale'], size=100))

    rounds = 1

    for r in range(rounds):
        print("Round: " + str(r))

        simulation(specificity_values_lower_bound, 'lower')
        simulation(specificity_values_upper_bound, 'upper')

    plot_data()

    lower = pd.read_csv('results/mc_int_simulation/results_automated_mc_interval_lower.csv')
    upper = pd.read_csv('results/mc_int_simulation/results_automated_mc_interval_upper.csv')

    resultTN = lower['TNout'] >= upper['TNout']
    resultFP = lower['FPout'] <= upper['FPout']

    resultTP = lower['TPout'] <= upper['TPout']
    resultFN = lower['FNout'] >= upper['FNout']

    print("TN: ", np.count_nonzero(np.array(resultTN) == True))
    print("FP: ", np.count_nonzero(np.array(resultFP) == True))

    print("TP: ", np.count_nonzero(np.array(resultTP) == True))
    print("FN: ", np.count_nonzero(np.array(resultFN) == True))