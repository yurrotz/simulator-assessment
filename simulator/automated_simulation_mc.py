import matplotlib.pyplot as plt
import pandas as pd

import first_analyzer.first_analyzer as first_analyzer
import fixer.fixer as fixer
import second_analyzer.second_analyzer as second_analyzer

import csv
from scipy import stats
import pickle as pk
import numpy as np

from scipy.stats import levy_l

from EDA.functions import normalization

"""Parameters"""
specificity_values = [x / 10 for x in range(0, 11, 1)]
fix_rate_values = [0.5, 0.7, 0.9, 1]
break_rate_values = [0, 0.2, 0.3]


def get_specificity_dist_par():
    with open('../EDA/binary_files/dist_par/spec_dist_par.pk', 'rb') as f:
        spec_dist_par = pk.load(f)

    return spec_dist_par


def filtering(simulation_type, fix_rate, break_rate):
    pd_values = pd.read_csv(f'results/{simulation_type}/results_automated_mc.csv')
    filtered_df = pd_values[(pd_values['fix_rate'] == fix_rate) & (pd_values['break_rate'] == break_rate)]

    return filtered_df


def plot_ROC(simulation_type, plot_title, case, fix_rate_values, break_rate_values, colors):
    fig, ax = plt.subplots(1, 1)

    for i, fix_rate in enumerate(fix_rate_values):
        for j, break_rate in enumerate(break_rate_values):
            filtered_df = filtering(simulation_type, fix_rate, break_rate)

            filtered_df['fpr'] = np.ones(len(filtered_df)) - (filtered_df['TNout'] / (filtered_df['TNout'] + filtered_df['FPout']))
            filtered_df['tpr'] = filtered_df['TPout'] / (filtered_df['TPout'] + filtered_df['FNout'])

            ax.plot(filtered_df['fpr'], filtered_df['tpr'], label=f'ROC FR: {fix_rate} BR: {break_rate}', color=colors[i + j])

    fig.suptitle(f'ROC Curve(s)\n {plot_title}')
    plt.legend()
    plt.setp(ax, xlim=(0, 1), ylim=(0, 1))

    plt.savefig(f'figures/{simulation_type}/roc_{case}.png')
    plt.show()

def plot_CDF(simulation_type, plot_title, case, fix_rate_values, break_rate_values, colors):
    fig, ax = plt.subplots(2, 2)

    for i, fix_rate in enumerate(fix_rate_values):
        for j, break_rate in enumerate(break_rate_values):

            filtered_df = filtering(simulation_type, fix_rate, break_rate)

            """True Positives"""
            tp = stats.ecdf(filtered_df['TPout'])
            ax[0, 0].plot(tp.cdf.quantiles, tp.cdf.probabilities, label=f'TP_{fix_rate}_{break_rate}', color=colors[i + j])
            ax[0, 0].set_xlim(0, 5000)
            ax[0, 0].set_ylim(0, 1)
            ax[0, 0].legend()

            """False Positives"""
            fp = stats.ecdf(filtered_df['FPout'])
            ax[0, 1].plot(fp.cdf.quantiles, fp.cdf.probabilities, label=f'FP_{fix_rate}_{break_rate}', color=colors[i + j])
            ax[0, 1].legend()

            """True Negatives"""
            tn = stats.ecdf(filtered_df['TNout'])
            ax[1, 0].plot(tn.cdf.quantiles, tn.cdf.probabilities, label=f'TN_{fix_rate}_{break_rate}', color=colors[i + j])
            ax[1, 0].set_ylim(0, 1)
            ax[1, 0].legend()

            """False Negatives"""
            fn = stats.ecdf(filtered_df['FNout'])
            ax[1, 1].plot(fn.cdf.quantiles, fn.cdf.probabilities, label=f'FN_{fix_rate}_{break_rate}', color=colors[i + j])
            ax[1, 1].set_ylim(0, 1)
            ax[1, 1].legend()

    fig.suptitle(f'CDFs\n{plot_title}')
    plt.legend()

    plt.savefig(f'figures/{simulation_type}/cdf_{case}.png')
    plt.show()

def plot_data(simulation_type, plot_title, case, fix_rate_values, break_rate_values):

    colors = ['rosybrown', 'goldenrod', 'black', 'mediumpurple',
              'lightcoral', 'gold', 'lightcyan', 'blueviolet',
              'firebrick', 'khaki', 'darkslategray', 'darkviolet',
              'tomato', 'olive', 'cadetblue', 'darkmagenta']

    plot_CDF(simulation_type, plot_title, case, fix_rate_values, break_rate_values, colors)
    plot_ROC(simulation_type, plot_title, case, fix_rate_values, break_rate_values, colors)

"""
def plot_data():
    pd_values = pd.read_csv('results/mc_simulation/results_automated_mc.csv')

    fig, ax = plt.subplots(2, 2)

    fig.suptitle('Automated Simulation MC')

    tp = stats.ecdf(pd_values['TPout'])
    ax[0, 0].plot(tp.cdf.quantiles, tp.cdf.probabilities, label='TP', color='red')
    ax[0, 0].legend()

    fp = stats.ecdf(pd_values['FPout'])
    ax[0, 1].plot(fp.cdf.quantiles, fp.cdf.probabilities, label='FP', color='green')
    ax[0, 1].legend()

    tn = stats.ecdf(pd_values['TNout'])
    ax[1, 0].plot(tn.cdf.quantiles, tn.cdf.probabilities, label='TN', color='yellow')
    ax[1, 0].legend()

    fn = stats.ecdf(pd_values['FNout'])
    ax[1, 1].plot(fn.cdf.quantiles, fn.cdf.probabilities, label='FN', color='blue')
    ax[1, 1].legend()

    plt.savefig('figures/tp_tn_fp_fn_mc.png')
    plt.show()
"""


def mc():
    spec_dist_par = get_specificity_dist_par()
    specificity_values = normalization(levy_l.rvs(loc=spec_dist_par['levy_l']['loc'],
                                                  scale=spec_dist_par['levy_l']['scale'], size=10))

    header = False
    write_mode = 'w'
    rounds = 1
    simulation_type = 'mc_simulation'

    for r in range(rounds):
        print("Round: " + str(r))

        for i, specificity in enumerate(specificity_values):
            print("\nSpecificity: ", specificity)

            r = 0.5
            sensitivity = pow(1 - specificity, 1 - r)

            for fix_rate in fix_rate_values:
                print("Fix rate: ", fix_rate)
                for break_rate in break_rate_values:
                    print("Break rate: ", break_rate)

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

                    if (tp_out + fp_out) != 0:
                        precision_out = tp_out / (tp_out + fp_out)
                    else:
                        precision_out = "err"

                    if (tp_out + fn_out) != 0:
                        sensitivity_out = tp_out / (tp_out + fn_out)
                    else:
                        sensitivity_out = "err"

                    with open('results/mc_simulation/results_automated_mc.csv', write_mode, encoding='UTF8', newline='') as f:
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

    pd_values = pd.read_csv(f'results/{simulation_type}/results_automated_mc.csv')
    print("Pd_values: ", pd_values)

    print("First uncertain case with MC: Fix Rate = 1; Break Rate = 0")
    plot_data(simulation_type, "First uncertain case: Fix Rate = 1; Break Rate = 0", 1,
              fix_rate_values[-1:], break_rate_values[0:1])

    print("Second uncertain Case: 0 <= Fix Rate < 1; 0 < Break Rate <= 1")
    plot_data(simulation_type, "Second uncertain case: 0 <= Fix Rate < 1; 0 < Break Rate <= 1", 3,
              fix_rate_values[0:-1], break_rate_values[1:])