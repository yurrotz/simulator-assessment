from scipy import stats
import matplotlib.pyplot as plt
import pickle as pk

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

def det_simulation(simulation_type, file, rounds, prev_rate):

    with open('../EDA/binary_files/p_boxes/p_boxes_parameters_sens.pk', 'rb') as f:
        par_sens = pk.load(f)

    with open('../EDA/binary_files/p_boxes/p_boxes_parameters_spec.pk', 'rb') as f:
        par_spec = pk.load(f)

    spec_val = [par_spec['data_loc_spec']]
    sens_val = [par_sens['data_loc_sens']]

    simulation(simulation_type, file, rounds, spec_val, sens_val, fix_rate_values, break_rate_values[0:1], prev_rate)

def prevalence_rate(simulation_type, upper_file, lower_file, file):

    if upper_file is None and lower_file is None:
        for fix_rate in fix_rate_values:
            for break_rate in break_rate_values[0:1]:
                print(f"\nFix rate: {fix_rate}, Break rate: {break_rate}")
                filtered_df = filtering(simulation_type, fix_rate, break_rate, file)

                print(f"Prevalence rate min: {filtered_df['final_prevalence_rate'].min(axis=0)}")
                print(f"Prevalence rate max: {filtered_df['final_prevalence_rate'].max(axis=0)}")

def false_negative_rate(simulation_type, upper_file, lower_file, file):

    if upper_file is None and lower_file is None:
        for fix_rate in fix_rate_values:
            for break_rate in break_rate_values[0:1]:
                print(f"\nFix rate: {fix_rate}, Break rate: {break_rate}")
                filtered_df = filtering(simulation_type, fix_rate, break_rate, file)

                print(f"False negative rate min: {filtered_df['false_negative_rate'].min(axis=0)}")
                print(f"False negative rate max: {filtered_df['false_negative_rate'].max(axis=0)}")


def see_results_det(simulation_type, file):

    """
    print("First deterministic case: Fix Rate = 1; Break Rate = 0")
    plot_data(simulation_type, "First deterministic case: Fix Rate = 1; Break Rate = 0", 1,
              fix_rate_values[-1:], break_rate_values[0:1], file)
    """

    prevalence_rate(simulation_type, None, None, file)
    false_negative_rate(simulation_type, None, None, file)

    """
    print("Second deterministic case: 0 <= Fix Rate < 1; Break Rate = 0")
    plot_data(simulation_type, "Second deterministic case: 0 <= Fix Rate < 1; Break Rate = 0", 2,
              fix_rate_values[0:-1], break_rate_values[0:1], file)
    """

    """
    print("Third deterministic Case: 0 <= Fix Rate < 1; 0 < Break Rate <= 1 (0.2, 0.3)")
    plot_data(simulation_type, "Third deterministic case: 0 <= Fix Rate < 1; 0 < Break Rate <= 1", 3,
              fix_rate_values[0:-1], break_rate_values[1:], file)
    """