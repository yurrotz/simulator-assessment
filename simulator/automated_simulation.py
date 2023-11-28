from scipy import stats
import matplotlib.pyplot as plt

from functions import filtering, simulation
from variables import specificity_values, fix_rate_values, break_rate_values, colors


def plot_roc(simulation_type, plot_title, case, fix_rate_values, break_rate_values, colors, file):
    fig, ax = plt.subplots(1, 1)

    for i, fix_rate in enumerate(fix_rate_values):
        for j, break_rate in enumerate(break_rate_values):
            filtered_df = filtering(simulation_type, fix_rate, break_rate, file)

            filtered_df['fpr'] = filtered_df['FPout'] / (filtered_df['TNout'] + filtered_df['FPout'])
            filtered_df['tpr'] = filtered_df['TPout'] / (filtered_df['TPout'] + filtered_df['FNout'])

            ax.scatter(filtered_df['fpr'], filtered_df['tpr'], label=f'ROC FR: {fix_rate} BR: {break_rate}',
                    color=colors[i][j])

    fig.suptitle(f'ROC Curve(s)\n {plot_title}')
    plt.legend()
    plt.setp(ax, xlim=(0, 1), ylim=(0, 1))

    plt.savefig(f'figures/{simulation_type}/roc_{case}.png')
    plt.show()

def plot_cdf(simulation_type, plot_title, case, fix_rate_values, break_rate_values, colors, file):
    fig, ax = plt.subplots(2, 2)

    for i, fix_rate in enumerate(fix_rate_values):
        for j, break_rate in enumerate(break_rate_values):

            filtered_df = filtering(simulation_type, fix_rate, break_rate, file)

            """True Positives"""
            tp = stats.ecdf(filtered_df['TPout'])
            ax[0, 0].plot(tp.cdf.quantiles, tp.cdf.probabilities, label=f'TP_{fix_rate}_{break_rate}',
                          color=colors[i][j])
            ax[0, 0].legend()

            """False Positives"""
            fp = stats.ecdf(filtered_df['FPout'])
            ax[0, 1].plot(fp.cdf.quantiles, fp.cdf.probabilities, label=f'FP_{fix_rate}_{break_rate}',
                          color=colors[i][j])
            ax[0, 1].legend()

            """True Negatives"""
            tn = stats.ecdf(filtered_df['TNout'])
            ax[1, 0].plot(tn.cdf.quantiles, tn.cdf.probabilities, label=f'TN_{fix_rate}_{break_rate}',
                          color=colors[i][j])
            ax[1, 0].legend()

            """False Negatives"""
            fn = stats.ecdf(filtered_df['FNout'])
            ax[1, 1].plot(fn.cdf.quantiles, fn.cdf.probabilities, label=f'FN_{fix_rate}_{break_rate}',
                          color=colors[i][j])
            ax[1, 1].legend()

    fig.suptitle(f'CDFs\n{plot_title}')
    plt.setp(ax, xlim=(0, 10000), ylim=(0, 1))
    plt.legend()

    plt.savefig(f'figures/{simulation_type}/cdf_{case}.png')
    plt.show()

def plot_data(simulation_type, plot_title, case, fix_rate_values, break_rate_values, file):

    plot_roc(simulation_type, plot_title, case, fix_rate_values, break_rate_values, colors, file)
    plot_cdf(simulation_type, plot_title, case, fix_rate_values, break_rate_values, colors, file)

def det_simulation(simulation_type, file, rounds):
    simulation(simulation_type, file, rounds, specificity_values, fix_rate_values, break_rate_values)

def see_results_det(simulation_type, file):

    print("First deterministic case: Fix Rate = 1; Break Rate = 0")
    plot_data(simulation_type, "First deterministic case: Fix Rate = 1; Break Rate = 0", 1,
              fix_rate_values[-1:], break_rate_values[0:1], file)

    print("Second deterministic case: 0 <= Fix Rate < 1; Break Rate = 0")
    plot_data(simulation_type, "Second deterministic case: 0 <= Fix Rate < 1; Break Rate = 0", 2,
              fix_rate_values[0:-1], break_rate_values[0:1], file)

    print("Third deterministic Case: 0 <= Fix Rate < 1; 0 < Break Rate <= 1 (0.2, 0.3)")
    plot_data(simulation_type, "Third deterministic case: 0 <= Fix Rate < 1; 0 < Break Rate <= 1", 3,
              fix_rate_values[0:-1], break_rate_values[1:], file)