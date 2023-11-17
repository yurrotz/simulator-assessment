import json
import random
from collections import OrderedDict
import fixer.fixer as fixer

# 0 NOT vulnerable/work | 1 vulnerable/work

def second_analyzer(sensitivity, specificity):
    
    global second_analyzer_array
    second_analyzer_array = []
    global p_out, n_out, pw_out, nw_out, tp2, fp2, tn2, fn2
    p_out, n_out, pw_out, nw_out, tp2, fp2, tn2, fn2 = 0, 0, 0, 0, 0, 0, 0, 0
    
    for obj in fixer.fixer_array:
        
        sens = random.random()
        spec = random.random()
        
        id, vuln, work, class_, fix, vuln_old, work_old, class_old = obj[0], obj[1], obj[2], obj[3], obj[4], obj[5], obj[6], obj[7]
        
        if fix == "yes":
            if vuln == 1:
                if sens <= sensitivity:
                    tp2 = tp2 + 1
                    second_analyzer_array.append([id, vuln, work, 1, fix, vuln_old, work_old, class_old]) #TP
                else:
                    fn2 = fn2 + 1
                    second_analyzer_array.append([id, vuln, work , 0, fix, vuln_old, work_old, class_old]) #FN
            elif vuln == 0:
                if spec <= specificity:
                    tn2 = tn2 + 1
                    second_analyzer_array.append([id, vuln, work , 0, fix, vuln_old, work_old, class_old]) #TN
                else:
                    fp2 = fp2 + 1
                    second_analyzer_array.append([id, vuln, work, 1, fix, vuln_old, work_old, class_old]) #FP
        elif fix == "no":
            second_analyzer_array.append([id, vuln, work , class_, fix, vuln_old, work_old, class_old])
    
    json_obj_list = []
    with open('./second_analyzer/second_analyzer.json', 'w') as fixer_file:
        for obj in second_analyzer_array:
            if obj[1] == 1:
                p_out = p_out + 1
                if obj[2] == 1:
                    pw_out = pw_out + 1
            else:
                n_out = n_out + 1
                if obj[2] == 1:
                    nw_out = nw_out + 1           
            json_obj_list.append(OrderedDict((
                                            ("id", obj[0]), ("vuln", obj[1]), ("work", obj[2]), ("class", obj[3]), 
                                            ("fix", obj[4]), ("vuln_old", obj[5]), ("work_old", obj[6]), ("class_old", obj[7])
                                            )))
        json.dump(json_obj_list, fixer_file, indent=4) 
        
    return p_out, n_out, pw_out, nw_out, tp2, fp2, tn2, fn2