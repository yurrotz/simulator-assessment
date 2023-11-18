import matplotlib.pyplot as plt
import pandas as pd

import first_analyzer.first_analyzer as first_analyzer
import fixer.fixer as fixer
import second_analyzer.second_analyzer as second_analyzer

import csv
from scipy.stats import *
import pickle as pk
import seaborn as sns

from EDA.functions import normalization

fixrate_values = [1]
break_rate = 0

def get_specificity_dist_par():
    with open('../EDA/binary_files/dist_par/spec_dist_par.pk', 'rb') as f:
        spec_dist_par = pk.load(f)

    return spec_dist_par

def plot_data():
    pd_values = pd.read_csv('results/mc_simulation/results_automated_mc.csv')

    print(pd_values)

    fix, ax = plt.subplots(2, 2)

    sns.histplot(pd_values['TPout'], kde=True, element='step', ax=ax[0, 0], label='TPout')
    #sns.move_legend(ax[0, 0], 'upper left')

    sns.histplot(pd_values['FPout'], kde=True, element='step', ax=ax[0, 1], label='FPout')
    #sns.move_legend(ax[0, 1], 'upper left')

    sns.histplot(pd_values['TNout'], kde=True, element='step', ax=ax[1, 0], label='TNout')
    #sns.move_legend(ax[1, 0], 'upper left')

    sns.histplot(pd_values['FNout'], kde=True, element='step', ax=ax[1, 1], label='FNout')
    #sns.move_legend(ax[1, 1], 'upper left')

    plt.show()


def mc():
    spec_dist_par = get_specificity_dist_par()
    specificity_values = normalization(levy_l.rvs(loc=spec_dist_par['levy_l']['loc'],
                                                  scale=spec_dist_par['levy_l']['scale'], size=10))

    rounds = 1
    header = False
    write_mode = 'w'

    for r in range(rounds):
        print("Round: " + str(r))

        for i, specificity in enumerate(specificity_values):
            print("Value: ", i)

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

    plot_data()