import pba

import json
import random
from collections import OrderedDict
import numpy as np


# 0 NOT vulnerable/work | 1 vulnerable/work

# 1st Analyzer
def first_analyzer(sensitivity, specificity, not_const, first_prev_rate):
    global ground_truth_array, first_analyzer_array
    ground_truth_array, first_analyzer_array = [], []
    global tot, p_init, n_init, pw_init, nw_init
    tot, p_init, n_init, pw_init, nw_init = 0, 0, 0, 0, 0

    with open('../ground_truth_generator/ground_truth.json') as ground_truth_file:
        data = json.load(ground_truth_file)
        for obj in data:
            tot = tot + 1
            if obj["vuln"] == 1:
                p_init = p_init + 1
                if obj["work"] == 1:
                    pw_init = pw_init + 1
            else:
                n_init = n_init + 1
                if obj["work"] == 1:
                    nw_init = nw_init + 1

            ground_truth_array.append([obj["id"], obj["vuln"], obj["work"]])

    global tp1, fp1, tn1, fn1
    tp1, fp1, tn1, fn1 = 0, 0, 0, 0

    for obj in ground_truth_array:
        sens = random.random()
        spec = random.random()

        id, vuln, work = obj[0], obj[1], obj[2]

        if vuln == 1:  # vulnerable
            if sens <= sensitivity:
                tp1 = tp1 + 1
                first_analyzer_array.append([id, vuln, work, 1, "unknown", "unknown", "unknown", "unknown"])  # TP
            else:
                fn1 = fn1 + 1
                first_analyzer_array.append([id, vuln, work, 0, "unknown", "unknown", "unknown", "unknown"])  # FN
        elif vuln == 0:  # NOT vulnerable
            if spec <= specificity:
                tn1 = tn1 + 1
                first_analyzer_array.append([id, vuln, work, 0, "unknown", "unknown", "unknown", "unknown"])  # TN
            else:
                fp1 = fp1 + 1
                first_analyzer_array.append([id, vuln, work, 1, "unknown", "unknown", "unknown", "unknown"])  # FP

    json_obj_list = []
    if not_const:
        ppv_value = (sensitivity * first_prev_rate) / (
                (sensitivity * first_prev_rate) + (1 - specificity) * (1 - first_prev_rate))

        npv_value = (specificity * (1 - first_prev_rate)) / ((
                specificity * (1 - first_prev_rate) + (1 - sensitivity) * first_prev_rate))

        tp1, fp1, tn1, fn1 = 0, 0, 0, 0
        with open('./first_analyzer/first_analyzer.json', 'w') as first_analyzer_file:
            for obj in first_analyzer_array:
                ppv = random.random()
                npv = random.random()

                if obj[3] == 1:
                    if ppv <= ppv_value:
                        tp1 += 1
                    else:
                        fp1 += 1
                elif obj[3] == 0:
                    if npv <= npv_value:
                        tn1 += 1
                    else:
                        fn1 += 1

                json_obj_list.append(OrderedDict((
                    ("id", obj[0]), ("vuln", obj[1]), ("work", obj[2]), ("class", obj[3]),
                    ("fix", obj[4]), ("vuln_old", obj[5]), ("work_old", obj[6]), ("class_old", obj[7]))))

            json.dump(json_obj_list, first_analyzer_file, indent=4)

    else:
        with open('./first_analyzer/first_analyzer.json', 'w') as first_analyzer_file:
            for obj in first_analyzer_array:
                json_obj_list.append(OrderedDict((
                    ("id", obj[0]), ("vuln", obj[1]), ("work", obj[2]), ("class", obj[3]),
                    ("fix", obj[4]), ("vuln_old", obj[5]), ("work_old", obj[6]), ("class_old", obj[7])
                )))
            json.dump(json_obj_list, first_analyzer_file, indent=4)

    return tot, p_init, n_init, pw_init, nw_init, tp1, fp1, tn1, fn1

def create_ground_truth(vuln_rate, work_rate, num_obj):
    print(f"New ground truth with: {vuln_rate}, {work_rate} e {num_obj}")

    random_vuln = np.random.random(num_obj)
    random_work = np.random.random(num_obj)

    vuln = (random_vuln <= vuln_rate).astype(int)
    work = (random_work <= work_rate).astype(int)

    vulnerable = np.sum(vuln)
    not_vulnerable = num_obj - vulnerable

    print(f"Vulnerable: {vulnerable}, Not vulnerable: {not_vulnerable}")

    json_obj_list = [{"id": i, "vuln": int(v), "work": int(w)} for i, (v, w) in enumerate(zip(vuln, work))]

    with (open('/Users/manu/Documents/GitHub/simulator-assessment/ground_truth_generator/ground_truth.json', 'w')
          as ground_truth_file):
        json.dump(json_obj_list, ground_truth_file, indent=4)

def first_classifier(tpr_interval, tnr_interval):
    vulnerable = 2000
    not_vulnerable = 18000

    tp1_interval = tpr_interval.__mul__(vulnerable)
    fn1_interval = (pba.Interval(1, 1).__sub__(tpr_interval)).__mul__(vulnerable)

    tn1_interval = tnr_interval.__mul__(not_vulnerable)
    fp1_interval = (pba.Interval(1, 1).__sub__(tnr_interval)).__mul__(not_vulnerable)

    print(f"Vulnerable objects: {vulnerable}, Non vulnerable: {not_vulnerable}\n")
    print(f"""TP1 interval: {tp1_interval}, FN1 interval: {fn1_interval}\nTN1 interval: {tn1_interval}, FP1 interval: {fp1_interval}\n""")

    print("FIRST CHECK")
    print(f"""Check left: {tp1_interval.left + fn1_interval.right + tn1_interval.left + fp1_interval.right}""")
    print(f"""Check right: {tp1_interval.right + fn1_interval.left + tn1_interval.right + fp1_interval.left}""")

    return tp1_interval, fn1_interval, tn1_interval, fp1_interval

def fixer(fix_rate, tp1_interval, fp1_interval, tpr_interval, tnr_interval):

    to_be_fixed = tp1_interval.oadd(fp1_interval)
    print("To be fixed: ", to_be_fixed)

    tp1_interval_not_fixed = tp1_interval.__mul__(pba.Interval(1 - fix_rate, 1 - fix_rate))
    print("Still vulnerable: ", tp1_interval_not_fixed)

    def second_classifier_tp2_fn2(tpr_interval, tp1_interval_not_fixed):
        tp2_interval = tpr_interval.__mul__(tp1_interval_not_fixed)
        fn2_interval = (pba.Interval(1, 1).__sub__(tpr_interval)).omul(tp1_interval_not_fixed)

        return tp2_interval, fn2_interval

    def second_classifier_tn2_fp2(tnr_interval, tp2_interval, fn2_interval):

        print("To subtract: ", tp2_interval, fn2_interval, tp2_interval.oadd(fn2_interval))
        not_vulnerable = to_be_fixed.osub(tp2_interval.oadd(fn2_interval))
        print("Not vulnerable: ", not_vulnerable)

        print("TNR interval: ", tnr_interval)

        tn2_interval = tnr_interval.omul(not_vulnerable)
        fp2_interval = (pba.Interval(1, 1).__sub__(tnr_interval)).pmul(not_vulnerable)

        return tn2_interval, fp2_interval

    tp2_interval, fn2_interval = second_classifier_tp2_fn2(tpr_interval, tp1_interval_not_fixed)
    print(f"""TP2 interval: {tp2_interval}, FN2 interval: {fn2_interval}\n""")

    tn2_interval, fp2_interval = second_classifier_tn2_fp2(tnr_interval, tp2_interval, fn2_interval)
    print(f"""TN2 interval: {tn2_interval}, FP2 interval: {fp2_interval}\n""")

    return tp2_interval, fn2_interval, tn2_interval, fp2_interval


def second_classifier(tpr_interval, tnr_interval, tp1_interval_fixed, tp1_interval_not_fixed, fp1_interval_fixed, fp1_interval_not_fixed): # fixed, not_fixed):

    tn2_interval = tnr_interval.__mul__(fp1_interval_fixed)
    fp2_interval = (pba.Interval(1, 1).__sub__(tnr_interval)).omul(fp1_interval_fixed.oadd(tp1_interval_fixed))

    tp2_interval = tpr_interval.__mul__(tp1_interval_not_fixed)
    fn2_interval = (pba.Interval(1, 1).__sub__(tpr_interval)).omul(tp1_interval_not_fixed)

    print(f"""TPR interval: {tpr_interval}""")
    print(f"""TNR interval: {tnr_interval}\n""")
    print(f"""TP2 interval: {tp2_interval}, FN2 interval: {fn2_interval}\nTN2 interval: {tn2_interval}, FP2 interval: {fp2_interval}\n""")

    return tp2_interval, fn2_interval, tn2_interval, fp2_interval


if __name__ == '__main__':

    random.seed(1234)
    prev_rates = [0.10]
    n_objects = 20000
    max_tpr, max_tnr = 1.00, 0.90
    min_tpr_array = [0.90]
    min_tnr_array = [0.80]
    mean_tpr_tnr_array = [0.75, 0.80, 0.85, 0.90, 0.95]

    fix_rates = [1.00]
    for first_prev_rate in prev_rates:
        print(f"\nPrevalence rate: {first_prev_rate}")
        # create_ground_truth(first_prev_rate, 1, n_objects)
        next = input("Iterate? ")

        if next == "yes":
            for (min_tpr, min_tnr) in list(zip(min_tpr_array, min_tnr_array)):
                print(f"Minimum tpr and tnr: {min_tpr}, {min_tnr}")
                next = input("Iterate? ")
                if next == "yes":
                    for fix_rate in fix_rates:
                        next = input("Show fix rate result? ")
                        if next == "yes":
                            print("Fix rate: ", fix_rate)
                            p_box_tpr = pba.min_max_mean(min_tpr, max_tpr, (min_tpr + max_tpr) / 2)
                            p_box_tnr = pba.min_max_mean(min_tnr, max_tnr, (min_tnr + max_tnr) / 2)

                            values_tpr = p_box_tpr.get_x()
                            values_tnr = p_box_tnr.get_x()

                            # Let's generate the intervals for recall and specificity
                            tpr_intervals = [pba.Interval(tpr_upper, tpr_lower) for (tpr_upper, tpr_lower) in zip(values_tpr[0], values_tpr[1])]
                            tnr_intervals = [pba.Interval(tnr_upper, tnr_lower) for (tnr_upper, tnr_lower) in zip(values_tnr[0], values_tnr[1])]

                            tp1_intervals, fn1_intervals, tn1_intervals, fp1_intervals = [], [], [], []
                            for i, (tpr_interval, tnr_interval) in enumerate(zip(tpr_intervals, tnr_intervals)):

                                print("Interval: ", i)
                                print(tpr_interval, tnr_interval)

                                tp1_interval, fn1_interval, tn1_interval, fp1_interval = first_classifier(tpr_interval, tnr_interval)
                                tp2_interval, fn2_interval, tn2_interval, fp2_interval = fixer(fix_rate, tp1_interval, fp1_interval, tpr_interval, tnr_interval)

                                tp_out_interval = tp2_interval
                                fp_out_interval = fp2_interval

                                fn_out_interval = (fn1_interval.padd(fn2_interval))
                                tn_out_interval = (tn1_interval.oadd(tn2_interval))

                                print(f"TP out interval: {tp_out_interval} FN out interval: {fn_out_interval}\nTN out interval: {tn_out_interval} FP out interval: {fp_out_interval}\n")
                                print("FINAL CHECK")
                                print(f"Check left: {tp_out_interval.left + fn_out_interval.right + tn_out_interval.left + fp_out_interval.right}")
                                print(f"Check right: {tp_out_interval.right + fn_out_interval.left + tn_out_interval.right + fp_out_interval.left}")

                                pr_interval_left = (tp_out_interval.left + fn_out_interval.right) / (tp_out_interval.left + fn_out_interval.right + tn_out_interval.left + fp_out_interval.right)
                                pr_interval_right = (tp_out_interval.right + fn_out_interval.left) / (tp_out_interval.right + fn_out_interval.left + tn_out_interval.right + fp_out_interval.left)

                                pr_interval = pba.Interval(pr_interval_left, pr_interval_right)
                                print("Final PR: ", pr_interval)

                                pr_interval_div = pr_interval.pdiv(pba.Interval(first_prev_rate, first_prev_rate))
                                print("Interval div: ", pr_interval_div)

                                fix_rate_interval = 1 - pr_interval_div
                                print("Fix rate interval: ", fix_rate_interval)


                                ppv_interval_num = tpr_interval.__mul__(first_prev_rate)
                                ppv_interval = ppv_interval_num.odiv(tpr_interval.__mul__(pba.Interval(first_prev_rate, first_prev_rate)).oadd(pba.Interval(1, 1).psub(tnr_interval).pmul(pba.Interval(1, 1).psub(pba.Interval(first_prev_rate, first_prev_rate)))))

                                """
                                print("Interval ppv num: ", ppv_interval_num)
                                print("Interval ppv den first: ", tpr_interval.__mul__(pba.Interval(first_prev_rate, first_prev_rate)))
                                print("Interval ppv den second: ", pba.Interval(1, 1).psub(tnr_interval))
                                print("Interval ppv den third: ", pba.Interval(1, 1).psub(pba.Interval(first_prev_rate, first_prev_rate)))
                                print("Interval ppv second product: ", pba.Interval(1, 1).psub(tnr_interval).pmul(pba.Interval(1, 1).psub(pba.Interval(first_prev_rate, first_prev_rate))))
                                print("Sum denominator: ", tpr_interval.__mul__(pba.Interval(first_prev_rate, first_prev_rate)).oadd(pba.Interval(1, 1).psub(tnr_interval).pmul(pba.Interval(1, 1).psub(pba.Interval(first_prev_rate, first_prev_rate)))))
                                print("Final result: ", ppv_interval_num.odiv(tpr_interval.__mul__(pba.Interval(first_prev_rate, first_prev_rate)).oadd(pba.Interval(1, 1).psub(tnr_interval).pmul(pba.Interval(1, 1).psub(pba.Interval(first_prev_rate, first_prev_rate))))))
                                """

                                npv_interval_num = tnr_interval.__mul__(pba.Interval(1, 1).psub(pba.Interval(first_prev_rate, first_prev_rate)))
                                npv_interval = npv_interval_num.pdiv((tnr_interval.pmul(pba.Interval(1, 1).psub(pba.Interval(first_prev_rate, first_prev_rate)))).oadd((pba.Interval(1, 1).psub(tpr_interval)).pmul(pba.Interval(first_prev_rate))))

                                print("\n")
                                """
                                print("Interval npv num: ", npv_interval_num)
                                print("Interval npv den first: ", tnr_interval.pmul(pba.Interval(1, 1).psub(pba.Interval(first_prev_rate, first_prev_rate))))
                                print("Interval npv den second: ", (pba.Interval(1, 1).psub(tpr_interval)).pmul(pba.Interval(first_prev_rate)))
                                print("Sum denominator: ", (tnr_interval.pmul(pba.Interval(1, 1).psub(pba.Interval(first_prev_rate, first_prev_rate)))).oadd((pba.Interval(1, 1).psub(tpr_interval)).pmul(pba.Interval(first_prev_rate))))
                                print("NPV interval: ", npv_interval)
                                """

                                positive_calls = tp_out_interval.oadd(fp_out_interval)
                                tp_out_adjusted = ppv_interval.omul(positive_calls)
                                new = pba.Interval(1, 1).psub(ppv_interval)
                                fp_out_adjusted = (pba.Interval(1, 1).psub(ppv_interval)).pmul(positive_calls)

                                print("Positive calls: ", positive_calls)
                                print("TP adjusted: ", tp_out_adjusted)
                                print("FP adjusted: ", fp_out_adjusted)

                                negative_calls = tn_out_interval.oadd(fn_out_interval)
                                tn_out_adjusted = npv_interval.pmul(negative_calls)
                                fn_out_adjusted = (pba.Interval(1, 1).psub(npv_interval)).omul(negative_calls)

                                print("Negative calls: ", negative_calls)
                                print("TN adjusted: ", tn_out_adjusted)
                                print("FN adjusted: ", fn_out_adjusted)

                                # pr_interval_left = (tp_out_interval.left + fn_out_interval.right) / (tp_out_interval.left + fn_out_interval.right + tn_out_interval.left + fp_out_interval.right)
                                # pr_interval_right = (tp_out_interval.right + fn_out_interval.left) / (tp_out_interval.right + fn_out_interval.left + tn_out_interval.right + fp_out_interval.left)

                                pr_interval_left_adj = (tp_out_adjusted.left + fn_out_adjusted.left) / (tp_out_adjusted.left + fn_out_adjusted.left + tn_out_adjusted.right + fp_out_adjusted.left)
                                pr_interval_right_adj = (tp_out_adjusted.right + fn_out_adjusted.right) / (tp_out_adjusted.right + fn_out_adjusted.right + tn_out_adjusted.left + fp_out_adjusted.right)

                                pr_interval_adj = pba.Interval(pr_interval_left_adj, pr_interval_right_adj)

                                print("Pr interval: ", pr_interval_adj)

                                pr_interval_div_adj = pr_interval_adj.pdiv(pba.Interval(first_prev_rate, first_prev_rate))

                                print("Pr div interval: ", pr_interval_div_adj)

                                fix_rate_adj = 1 - pr_interval_div_adj

                                print("Fix rate adjusted: " ,fix_rate_adj)












