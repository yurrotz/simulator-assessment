import pickle

import pba
import matplotlib.pyplot as plt
import random
import pickle as pk


def function():
    with open("first_pickle.pk", "wb") as file:
        p_box = pba.min_max_mean(0.50, 1.00, 0.90)
        x = p_box.get_x()[0]
        pickle.dump(x, file)

    with open("second_pickle.pk", "wb") as file:
        p_box = pba.min_max_mean(0.50, 1.00, 0.90)
        x = p_box.get_x()[1]
        pickle.dump(x, file)

    with open("first_pickle_1.pk", "wb") as file:
        p_box = pba.min_max_mean(0.50, 1.00, 0.90)
        x = p_box.get_x()[0]
        pickle.dump(x, file)

    with open("second_pickle_1.pk", "wb") as file:
        p_box = pba.min_max_mean(0.50, 1.00, 0.90)
        x = p_box.get_x()[1]
        pickle.dump(x, file)

    with open("first_pickle.pk", "rb") as file:
        x = pk.load(file)

    with open("second_pickle.pk", "rb") as file:
        y = pk.load(file)

    with open("first_pickle_1.pk", "rb") as file:
        x_1 = pk.load(file)

    with open("second_pickle_1.pk", "rb") as file:
        y_1 = pk.load(file)

    x_check = x == x_1
    y_check = y == y_1

    print(all(x_check))
    print(all(y_check))

if __name__ == '__main__':
    p_box_recall = pba.min_max_mean(0.50, 1.00, 0.75)

    sensitivity_values_upper_bound, sensitivity_values_lower_bound = p_box_recall.get_x()
    # print(sensitivity_values_upper_bound)
    # print(sensitivity_values_lower_bound)

    interval_sens = pba.Interval(0.50, 1.00)
    print(10 - interval_sens)
    interval_sens = interval_sens.__mul__(10000)
    print(interval_sens)

    interval_sens = pba.Interval(1, 2)
    interval_sens_1 = pba.Interval(1, 2)
    print(interval_sens.oadd(interval_sens_1))



