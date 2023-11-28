import matplotlib.pyplot as plt
import pickle as pk
import pandas as pd
import numpy as np

from EDA.functions import normalization

from scipy import stats
from functions import simulation, filtering
from variables import fix_rate_values, break_rate_values, colors1


def get_upper_lower_bound(dist_type):

    with open('../EDA/binary_files/p_boxes/levy_l_p_boxes.pk', 'rb') as f:
        p_boxes = pk.load(f)

    return p_boxes

def plot_roc(simulation_type, plot_title, case, fix_rate_values, break_rate_values, colors, file_upper, file_lower,
             dist_type):
    fig, ax = plt.subplots(1, 1)

    for i, fix_rate in enumerate(fix_rate_values):
        for j, break_rate in enumerate(break_rate_values):
            filtered_df_lower = filtering(simulation_type, fix_rate, break_rate, file_lower)
            filtered_df_upper = filtering(simulation_type, fix_rate, break_rate, file_upper)

            filtered_df_lower['fpr'] = (filtered_df_lower['FPout'] /
                                        (filtered_df_lower['TNout'] + filtered_df_lower['FPout']))
            filtered_df_lower['tpr'] = (filtered_df_lower['TPout'] /
                                        (filtered_df_lower['TPout'] + filtered_df_lower['FNout']))

            filtered_df_upper['fpr'] = (filtered_df_upper['FPout'] /
                                        (filtered_df_upper['TNout'] + filtered_df_upper['FPout']))
            filtered_df_upper['tpr'] = (filtered_df_upper['TPout'] /
                                        (filtered_df_upper['TPout'] + filtered_df_upper['FNout']))

            ax.scatter(filtered_df_lower['fpr'], filtered_df_lower['tpr'],
                       label=f'ROC Lower FR: {fix_rate} BR: {break_rate}',
                       color=colors[i][j])

            ax.scatter(filtered_df_upper['fpr'], filtered_df_upper['tpr'],
                       label=f'ROC Upper FR: {fix_rate} BR: {break_rate}',
                       color=colors[i][j])

    fig.suptitle(f'ROC Curve(s) Distribution: {dist_type}\n{plot_title}')
    plt.legend()
    plt.setp(ax, xlim=(0, 1), ylim=(0, 1))

    plt.savefig(f'figures/{simulation_type}/roc_{case}_{dist_type}.png')
    plt.show()


def plot_tp_cdf(simulation_type, plot_title, case, fix_rate_values, break_rate_values, file_upper, file_lower,
                dist_type, imp):

    fig, ax = plt.subplots()

    for i, fix_rate in enumerate(fix_rate_values):
        for j, break_rate in enumerate(break_rate_values):

            filtered_df_upper = filtering(simulation_type, fix_rate, break_rate, file_upper)
            filtered_df_lower = filtering(simulation_type, fix_rate, break_rate, file_lower)

            tp_upper = stats.ecdf(filtered_df_upper['TPout'])
            ax.plot(tp_upper.cdf.quantiles, tp_upper.cdf.probabilities, label=f'TPUpper_{fix_rate}_{break_rate}',
                          color=colors1[i][j])
            tp_lower = stats.ecdf(filtered_df_lower['TPout'])
            ax.plot(tp_lower.cdf.quantiles, tp_lower.cdf.probabilities, label=f'TPLower_{fix_rate}_{break_rate}',
                          color=colors1[i][j])
            fig.suptitle(f'TP CDFs Distribution: {dist_type}\n{plot_title}')
            plt.legend()

    plt.savefig(f'figures/{simulation_type}/cdf_{case}_{dist_type}_tp.png')
    plt.show()


def plot_fp_cdf(simulation_type, plot_title, case, fix_rate_values, break_rate_values, file_upper, file_lower,
                dist_type, imp):

    fig, ax = plt.subplots()

    for i, fix_rate in enumerate(fix_rate_values):
        for j, break_rate in enumerate(break_rate_values):
            filtered_df_upper = filtering(simulation_type, fix_rate, break_rate, file_upper)
            filtered_df_lower = filtering(simulation_type, fix_rate, break_rate, file_lower)

            fp_upper = stats.ecdf(filtered_df_upper['FPout'])
            ax.plot(fp_upper.cdf.quantiles, fp_upper.cdf.probabilities, label=f'FPUpper_{fix_rate}_{break_rate}',
                          color=colors1[i][j])
            fp_lower = stats.ecdf(filtered_df_lower['FPout'])
            ax.plot(fp_lower.cdf.quantiles, fp_lower.cdf.probabilities, label=f'FPLower_{fix_rate}_{break_rate}',
                          color=colors1[i][j])
            fig.suptitle(f'FP CDFs Distribution: {dist_type}\n{plot_title}')
            plt.legend()

    plt.savefig(f'figures/{simulation_type}/cdf_{case}_{dist_type}_fp.png')
    plt.show()


def plot_tn_cdf(simulation_type, plot_title, case, fix_rate_values, break_rate_values, file_upper, file_lower,
                dist_type, imp):

    fig, ax = plt.subplots()

    for i, fix_rate in enumerate(fix_rate_values):
        for j, break_rate in enumerate(break_rate_values):
            filtered_df_upper = filtering(simulation_type, fix_rate, break_rate, file_upper)
            filtered_df_lower = filtering(simulation_type, fix_rate, break_rate, file_lower)

            tn_upper = stats.ecdf(filtered_df_upper['TNout'])
            ax.plot(tn_upper.cdf.quantiles, tn_upper.cdf.probabilities, label=f'TNUpper_{fix_rate}_{break_rate}',
                          color=colors1[i][j])
            tn_lower = stats.ecdf(filtered_df_lower['TNout'])
            ax.plot(tn_lower.cdf.quantiles, tn_lower.cdf.probabilities, label=f'TNLower_{fix_rate}_{break_rate}',
                          color=colors1[i][j])
            fig.suptitle(f'TN CDFs Distribution: {dist_type}\n{plot_title}')
            plt.legend()

    plt.savefig(f'figures/{simulation_type}/cdf_{case}_{dist_type}_tn.png')
    plt.show()


def plot_fn_cdf(simulation_type, plot_title, case, fix_rate_values, break_rate_values, file_upper, file_lower,
                dist_type, imp):

    fig, ax = plt.subplots()

    for i, fix_rate in enumerate(fix_rate_values):
        for j, break_rate in enumerate(break_rate_values):
            filtered_df_upper = filtering(simulation_type, fix_rate, break_rate, file_upper)
            filtered_df_lower = filtering(simulation_type, fix_rate, break_rate, file_lower)

            fn_upper = stats.ecdf(filtered_df_upper['FNout'])
            ax.plot(fn_upper.cdf.quantiles, fn_upper.cdf.probabilities, label=f'FNUpper_{fix_rate}_{break_rate}',
                          color=colors1[i][j])
            fn_lower = stats.ecdf(filtered_df_lower['FNout'])
            ax.plot(fn_lower.cdf.quantiles, fn_lower.cdf.probabilities, label=f'FNLower_{fix_rate}_{break_rate}',
                          color=colors1[i][j])
            ax.legend()

            fig.suptitle(f'FN CDFs Distribution: {dist_type}\n{plot_title}')
            plt.legend()

    plt.savefig(f'figures/{simulation_type}/cdf_{case}_{dist_type}_fn.png')
    plt.show()

def plot_cdf(simulation_type, plot_title, case, fix_rate_values, break_rate_values, file_upper, file_lower,
             dist_type, imp):

    if case == 1:
        fig, ax = plt.subplots(2, 2)

        for fix_rate in fix_rate_values:
            for break_rate in break_rate_values:

                filtered_df_upper = filtering(simulation_type, fix_rate, break_rate, file_upper)
                filtered_df_lower = filtering(simulation_type, fix_rate, break_rate, file_lower)

                """True Positives"""
                tp_upper = stats.ecdf(filtered_df_upper['TPout'])
                ax[0, 0].plot(tp_upper.cdf.quantiles, tp_upper.cdf.probabilities, label=f'TPUpper_{fix_rate}_{break_rate}',
                              color='yellow')
                tp_lower = stats.ecdf(filtered_df_lower['TPout'])
                ax[0, 0].plot(tp_lower.cdf.quantiles, tp_lower.cdf.probabilities, label=f'TPLower_{fix_rate}_{break_rate}',
                              color='blue')

                if imp:
                    ax[0, 0].set_xlim(0, 10000)
                    ax[0, 0].set_ylim(0, 1)
                ax[0, 0].legend()

                """False Positives"""
                fp_upper = stats.ecdf(filtered_df_upper['FPout'])
                ax[0, 1].plot(fp_upper.cdf.quantiles, fp_upper.cdf.probabilities, label=f'FPUpper_{fix_rate}_{break_rate}',
                              color='red')
                fp_lower = stats.ecdf(filtered_df_lower['FPout'])
                ax[0, 1].plot(fp_lower.cdf.quantiles, fp_lower.cdf.probabilities, label=f'FPLower_{fix_rate}_{break_rate}',
                              color='green')
                ax[0, 1].legend()

                """True Negatives"""
                tn_upper = stats.ecdf(filtered_df_upper['TNout'])
                ax[1, 0].plot(tn_upper.cdf.quantiles, tn_upper.cdf.probabilities, label=f'TNUpper_{fix_rate}_{break_rate}',
                              color='red')
                tn_lower = stats.ecdf(filtered_df_lower['TNout'])
                ax[1, 0].plot(tn_lower.cdf.quantiles, tn_lower.cdf.probabilities, label=f'TNLower_{fix_rate}_{break_rate}',
                              color='green')
                ax[1, 0].legend()


                """False Negatives"""
                fn_upper = stats.ecdf(filtered_df_upper['FNout'])
                ax[1, 1].plot(fn_upper.cdf.quantiles, fn_upper.cdf.probabilities, label=f'FNUpper_{fix_rate}_{break_rate}',
                              color='yellow')
                fn_lower = stats.ecdf(filtered_df_lower['FNout'])
                ax[1, 1].plot(fn_lower.cdf.quantiles, fn_lower.cdf.probabilities, label=f'FNLower_{fix_rate}_{break_rate}',
                              color='blue')
                ax[1, 1].legend()

                fig.suptitle(f'CDFs Distribution: {dist_type}\n{plot_title}')
                plt.legend()

        plt.savefig(f'figures/{simulation_type}/cdf_{case}_{dist_type}.png')
        plt.show()

    elif case == 3:
        # plot_tp_cdf(simulation_type, plot_title, case, fix_rate_values, break_rate_values, file_upper, file_lower, dist_type, imp)
        # plot_fp_cdf(simulation_type, plot_title, case, fix_rate_values, break_rate_values, file_upper, file_lower, dist_type, imp)
        # plot_tn_cdf(simulation_type, plot_title, case, fix_rate_values, break_rate_values, file_upper, file_lower, dist_type, imp)
        plot_fn_cdf(simulation_type, plot_title, case, fix_rate_values, break_rate_values, file_upper, file_lower, dist_type, imp)


def plot_data(simulation_type, plot_title, case, fix_rate_values, break_rate_values, file_upper,
              file_lower, dist_type, imp):

    plot_cdf(simulation_type, plot_title, case, fix_rate_values, break_rate_values, file_upper,
             file_lower, dist_type, imp)
    plot_roc(simulation_type, plot_title, case, fix_rate_values, break_rate_values, colors1, file_upper,
             file_lower, dist_type)


def mc_interval_simulation(simulation_type, file_upper, file_lower, rounds):
    p_boxes = get_upper_lower_bound('levy_l')

    np.random.seed(42)

    specificity_values_upper_bound = normalization(stats.levy_l.rvs(loc=p_boxes['upper_loc'],
                                                                    scale=p_boxes['upper_scale'], size=10))
    specificity_values_lower_bound = normalization(stats.levy_l.rvs(loc=p_boxes['lower_loc'],
                                                                    scale=p_boxes['lower_scale'], size=10))

    print(len(specificity_values_upper_bound), len(specificity_values_lower_bound))

    simulation(simulation_type, file_upper, rounds, specificity_values_upper_bound, fix_rate_values, break_rate_values)
    simulation(simulation_type, file_lower, rounds, specificity_values_lower_bound, fix_rate_values, break_rate_values)

def see_results_mc_interval(simulation_type, file_upper, file_lower):

    print("First uncertain case with MC Interval: Fix Rate = 1; Break Rate = 0")
    plot_data(simulation_type, "First Interval MC: Fix Rate = 1; Break Rate = 0", 1,
              fix_rate_values[-1:], break_rate_values[0:1], file_upper, file_lower, 'levy_l',
              True)

    print("Second uncertain case with MC Interval: 0 <= Fix Rate < 1; 0 < Break Rate <= 1")
    plot_data(simulation_type, "Second Interval MC: 0 <= Fix Rate <= 1; 0 < Break Rate <= 1", 3,
              fix_rate_values[0:-1], break_rate_values[1:], file_upper, file_lower, 'levy_l',
              False)

    lower = pd.read_csv('results/mc_int_simulation/results_automated_mc_interval_lower.csv')
    upper = pd.read_csv('results/mc_int_simulation/results_automated_mc_interval_upper.csv')

    resultTP = lower['TPout'] <= upper['TPout']
    resultFP = lower['FPout'] <= upper['FPout']

    resultTN = lower['TNout'] >= upper['TNout']
    resultFN = lower['FNout'] >= upper['FNout']

    print(lower['FNout'], upper['FNout'])

    print("TP: ", np.count_nonzero(np.array(resultTP) == True))
    print("FP: ", np.count_nonzero(np.array(resultFP) == True))

    print("TN: ", np.count_nonzero(np.array(resultTN) == True))
    print("FN: ", np.count_nonzero(np.array(resultFN) == True))