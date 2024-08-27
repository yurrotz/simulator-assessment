from automated_simulation import det_simulation, see_results_det
from automated_simulation_mc import mc_simulation, see_results_mc
from automated_simulation_mc_interval import mc_interval_simulation, see_results_mc_interval
from automated_simulation_p_boxes import p_box_simulation, p_box_simulation_2, see_results_p_box
from ground_truth_generator.ground_truth_generator import create_ground_truth
import random
import numpy as np

if __name__ == '__main__':
    sim_type = input('Insert det/mc/mc_interval/p_box/p_box_2: ')

    if sim_type == 'det':
        prev_rates = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        for prev_rate in prev_rates:
            create_ground_truth(prev_rate, 1, 10000)
            det_simulation('det_simulation', 'results_automated_det.csv', 10, prev_rate)
            # see_results_det('det_simulation', 'results_automated_det.csv')

    elif sim_type == 'mc':
        mc_simulation('mc_simulation', 'results_automated_mc.csv', 1)
        see_results_mc('mc_simulation', 'results_automated_mc.csv')

    elif sim_type == 'mc_interval':
        mc_interval_simulation('mc_int_simulation', 'results_automated_mc_interval_upper.csv',
                               'results_automated_mc_interval_lower.csv', 1)
        see_results_mc_interval('mc_int_simulation',
                                'results_automated_mc_interval_lower.csv',
                                'results_automated_mc_interval_upper.csv')

    elif sim_type == 'p_box':
        random.seed(1234)
        prev_rates = [0.10, 0.50, 1.00]
        n_objects = 10000
        for first_prev_rate in prev_rates:
            print(f"\nPrevalence rate: {first_prev_rate}")
            create_ground_truth(first_prev_rate, 1, n_objects)
            p_box_simulation('p_box_simulation', 'results_automated_p_box_upper.csv',
                             'results_automated_p_box_lower.csv', 1, False, first_prev_rate)
            see_results_p_box('p_box_simulation', 'results_automated_p_box_upper.csv',
                              'results_automated_p_box_lower.csv')

    elif sim_type == 'p_box_2':
        random.seed(1234)
        prev_rates = [0.10, 0.50, 1.00]
        n_objects = 20000
        max_sens, max_spec = 1.00, 0.90
        min_sens_array = [0.50, 0.60, 0.70, 0.80, 0.90]
        min_spec_array = [0.40, 0.50, 0.60, 0.70, 0.80]
        for first_prev_rate in prev_rates:
            next = input("New prevalence rate? ")
            if next == "yes":
                print(f"\nPrevalence rate: {first_prev_rate}")
                create_ground_truth(first_prev_rate, 1, n_objects)
                for (min_sens, min_spec) in list(zip(min_sens_array, min_spec_array)):
                    next = input("New min sens and spec? ")
                    if next == "yes":
                        print(f"Minimum sens and spec: {min_sens}, {min_spec}, Max sens and spec: {max_sens}, {max_spec}")

                        print("RESULTS WITH CONSTANT PR\n")
                        p_box_simulation_2('p_box_simulation', 'results_automated_p_box_upper.csv',
                                         'results_automated_p_box_lower.csv', 1, False,
                                           first_prev_rate, min_sens, min_spec, max_sens, max_spec)
                        see_results_p_box('p_box_simulation', 'results_automated_p_box_upper.csv',
                                          'results_automated_p_box_lower.csv', False)

                        """
                        print("\nRESULTS WITH VARYING PR\n")
                        p_box_simulation_2('p_box_simulation', 'results_automated_p_box_upper_.csv',
                                     'results_automated_p_box_lower_.csv', 1, True,
                                           first_prev_rate, min_sens, min_spec, max_sens, max_spec)

                        see_results_p_box('p_box_simulation', 'results_automated_p_box_upper_.csv',
                                      'results_automated_p_box_lower_.csv', True)
                        """
