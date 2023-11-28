import pickle as pk
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from EDA.functions import normalization
from scipy.stats import levy_l, beta, norm

from functions import filtering, simulation
from variables import fix_rate_values, break_rate_values, colors


def get_specificity_dist_par():
    with open('../EDA/binary_files/dist_par/spec_dist_par.pk', 'rb') as f:
        spec_dist_par = pk.load(f)

    return spec_dist_par


def plot_roc(simulation_type, plot_title, case, fix_rate_values, break_rate_values, colors, file, distr_type):
    fig, ax = plt.subplots(1, 1)

    for i, fix_rate in enumerate(fix_rate_values):
        for j, break_rate in enumerate(break_rate_values):
            filtered_df = filtering(simulation_type, fix_rate, break_rate, file)

            filtered_df['fpr'] = filtered_df['FPout'] / (filtered_df['TNout'] + filtered_df['FPout'])
            filtered_df['tpr'] = filtered_df['TPout'] / (filtered_df['TPout'] + filtered_df['FNout'])

            ax.scatter(filtered_df['fpr'], filtered_df['tpr'], label=f'ROC FR: {fix_rate} BR: {break_rate}',
                       color=colors[i][j])

    fig.suptitle(f'ROC Curve(s) Distribution: {distr_type}\n{plot_title}')
    plt.legend()
    plt.setp(ax, xlim=(0, 1), ylim=(0, 1))

    plt.savefig(f'figures/{simulation_type}/roc_{case}_{distr_type}.png')
    plt.show()

def plot_cdf(simulation_type, plot_title, case, fix_rate_values, break_rate_values, colors, file, dist_type, imp):
    fig, ax = plt.subplots(2, 2)

    for i, fix_rate in enumerate(fix_rate_values):
        for j, break_rate in enumerate(break_rate_values):

            filtered_df = filtering(simulation_type, fix_rate, break_rate, file)

            """True Positives"""
            tp = stats.ecdf(filtered_df['TPout'])
            ax[0, 0].plot(tp.cdf.quantiles, tp.cdf.probabilities, label=f'TP_{fix_rate}_{break_rate}',
                          color=colors[i][j])
            if imp:
                ax[0, 0].set_xlim(0, 10000)
                ax[0, 0].set_ylim(0, 1)

            ax[0, 0].legend()

            """False Positives"""
            fp = stats.ecdf(filtered_df['FPout'])
            ax[0, 1].plot(fp.cdf.quantiles, fp.cdf.probabilities, label=f'FP_{fix_rate}_{break_rate}',
                          color=colors[i][j])
            ax[0, 1].set_xlim(0, 10000)
            ax[0, 1].legend()

            """True Negatives"""
            tn = stats.ecdf(filtered_df['TNout'])
            ax[1, 0].plot(tn.cdf.quantiles, tn.cdf.probabilities, label=f'TN_{fix_rate}_{break_rate}',
                          color=colors[i][j])
            ax[1, 0].set_xlim(0, 10000)
            ax[1, 0].set_ylim(0, 1)
            ax[1, 0].legend()

            """False Negatives"""
            fn = stats.ecdf(filtered_df['FNout'])
            ax[1, 1].plot(fn.cdf.quantiles, fn.cdf.probabilities, label=f'FN_{fix_rate}_{break_rate}',
                          color=colors[i][j])
            ax[1, 1].set_xlim(0, 10000)
            ax[1, 1].set_ylim(0, 1)
            ax[1, 1].legend()

    fig.suptitle(f'CDFs Distribution: {dist_type}\n{plot_title}')
    plt.legend()

    plt.savefig(f'figures/{simulation_type}/cdf_{case}_{dist_type}.png')
    plt.show()

def plot_data(simulation_type, plot_title, case, fix_rate_values, break_rate_values, file, dist_type, imp):

    plot_roc(simulation_type, plot_title, case, fix_rate_values, break_rate_values, colors, file, dist_type)
    plot_cdf(simulation_type, plot_title, case, fix_rate_values, break_rate_values, colors, file, dist_type, imp)


def mc_simulation(simulation_type, file, rounds):
    spec_dist_par = get_specificity_dist_par()
    specificity_values = normalization(levy_l.rvs(loc=spec_dist_par['levy_l']['loc'],
                                                scale=spec_dist_par['levy_l']['scale'], size=10))
    simulation(simulation_type, file, rounds, specificity_values, fix_rate_values, break_rate_values)


def see_results_mc(simulation_type, file):
    pd_values = pd.read_csv(f'results/{simulation_type}/{file}')
    print("Pd_values: ", pd_values)

    print("First uncertain case with MC: Fix Rate = 1; Break Rate = 0")
    plot_data(simulation_type, "First MC: Fix Rate = 1; Break Rate = 0", 1,
              fix_rate_values[-1:], break_rate_values[0:1], file, 'levy_l', True)

    print("Second uncertain Case with MC: 0 <= Fix Rate < 1; 0 < Break Rate <= 1")
    plot_data(simulation_type, "Second MC: 0 <= Fix Rate < 1; 0 < Break Rate <= 1", 3,
              fix_rate_values[0:-1], break_rate_values[1:], file, 'levy_l', True)


"""
def comparison():
    colors = ['brown', 'orangered', 'sienna', 'darkgoldenrod',
              'black', 'olive', 'yellow', 'lawngreen',
              'forestgreen', 'turquoise', 'deepskyblue', 'slategray',
              'midnightblue', 'blue', 'darkviolet', 'fuchsia']

    fig, ax = plt.subplots(1, 2)

    for i, fix_rate in enumerate(fix_rate_values[0:1]):
        for j, break_rate in enumerate(break_rate_values[1:2]):
            filtered_df_det = filtering('det_simulation', fix_rate, break_rate, 'results_automated_det.csv')
            filtered_df_mc = filtering('mc_simulation', fix_rate, break_rate, 'results_automated_mc.csv')

            filtered_df_mc['fpr'] = filtered_df_mc['FPout'] / (filtered_df_mc['TNout'] + filtered_df_mc['FPout'])
            filtered_df_mc['tpr'] = filtered_df_mc['TPout'] / (filtered_df_mc['TPout'] + filtered_df_mc['FNout'])

            print(filtered_df_det[['fix_rate', 'break_rate', 'specificity', 'fpr', 'tpr', 'Precision']])
            print(filtered_df_mc[['fix_rate', 'break_rate', 'specificity', 'fpr', 'tpr', 'Precision']])

            ax[0].scatter(filtered_df_det['fpr'], filtered_df_det['tpr'], label=f'ROC FR: {fix_rate} BR: {break_rate}',
                    color=colors[i + j])
            ax[1].scatter(filtered_df_mc['fpr'], filtered_df_mc['tpr'], label=f'ROC FR: {fix_rate} BR: {break_rate}',
                    color=colors[i + j])

    fig.suptitle(f'ROC Curve(s) Comparison')
    plt.legend()
    plt.setp(ax, xlim=(0, 1), ylim=(0, 1))

    #plt.savefig(f'figures/{simulation_type}/roc_{case}.png')
    plt.show()
"""
