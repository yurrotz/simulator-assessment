import json
import random
from collections import OrderedDict

# 0 NOT vulnerable/work | 1 vulnerable/work

#1st Analyzer
def first_analyzer(sensitivity, specificity):
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
            
            ground_truth_array.append([obj["id"],obj["vuln"],obj["work"]])

    global tp1, fp1, tn1, fn1
    tp1, fp1, tn1, fn1 = 0, 0, 0, 0
        
    for obj in ground_truth_array:
        sens = random.random()
        spec = random.random()
        
        id, vuln, work = obj[0], obj[1], obj[2]
        
        if vuln == 1: # vulnerable
            if sens <= sensitivity:
                tp1 = tp1 + 1
                first_analyzer_array.append([id, vuln, work, 1, "unknown", "unknown", "unknown", "unknown"]) #TP
            else:
                fn1 = fn1 + 1
                first_analyzer_array.append([id, vuln, work, 0, "unknown", "unknown", "unknown", "unknown"]) #FN
        elif vuln == 0: # NOT vulnerable
            if spec <= specificity:
                tn1 = tn1 + 1
                first_analyzer_array.append([id, vuln, work, 0, "unknown", "unknown", "unknown", "unknown"]) #TN
            else:
                fp1 = fp1 + 1
                first_analyzer_array.append([id, vuln, work, 1, "unknown", "unknown", "unknown", "unknown"]) #FP
                         
    json_obj_list = []
    with open('./first_analyzer/first_analyzer.json', 'w') as first_analyzer_file:
        for obj in first_analyzer_array:
            json_obj_list.append(OrderedDict((
                                            ("id", obj[0]), ("vuln", obj[1]), ("work", obj[2]), ("class", obj[3]), 
                                            ("fix", obj[4]), ("vuln_old", obj[5]), ("work_old", obj[6]), ("class_old", obj[7])
                                            )))
        json.dump(json_obj_list, first_analyzer_file, indent=4)
        
    return tot, p_init, n_init, pw_init, nw_init, tp1, fp1, tn1, fn1