from automated_simulation_mc import mc
from automated_simulation_mc_interval import mc_interval

if __name__ == '__main__':
    sim_type = input('Insert the simulation type: ')

    if sim_type == 'deterministic':
        pass
    elif sim_type == 'mc':
        mc()
    elif sim_type == 'mc_interval':
        mc_interval()