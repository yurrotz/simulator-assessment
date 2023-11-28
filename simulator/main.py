from automated_simulation import det_simulation, see_results_det
from automated_simulation_mc import mc_simulation, see_results_mc
from automated_simulation_mc_interval import mc_interval_simulation, see_results_mc_interval
from automated_simulation_p_boxes import p_box_simulation, see_results_p_box

if __name__ == '__main__':
    sim_type = input('Insert det/mc/mc_interval/p_box: ')

    if sim_type == 'det':
        # det_simulation('det_simulation', 'results_automated_det.csv', 1)
        see_results_det('det_simulation', 'results_automated_det.csv')

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
        p_box_simulation('p_box_simulation', 'results_automated_p_box_upper.csv', 'results_automated_p_box_lower.csv', 1)
        see_results_p_box('p_box_simulation', 'results_automated_p_box_upper.csv',
                          'results_automated_p_box_lower.csv')
