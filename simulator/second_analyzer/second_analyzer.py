import json
import random
from collections import OrderedDict
import fixer.fixer as fixer

# 0 NOT vulnerable/work | 1 vulnerable/work

second_analyzer_array = []

def second_analyzer(sensitivity, specificity):
    for obj in fixer.fixer_array:
        
        sens = random.random()
        spec = random.random()
        
        id, vuln, work, class_, fix, vuln_old, work_old, class_old = obj[0], obj[1], obj[2], obj[3], obj[4], obj[5], obj[6], obj[7]
        
        if fix == "yes":
            if vuln == 1:
                if sens <= sensitivity:
                    second_analyzer_array.append([id, vuln, work, 1, fix, vuln_old, work_old, class_old])
                else:
                    second_analyzer_array.append([id, vuln, work , 0, fix, vuln_old, work_old, class_old])
            elif obj[1] == 0:
                if spec <= specificity:
                    second_analyzer_array.append([id, vuln, work , 0, fix, vuln_old, work_old, class_old])
                else:
                    second_analyzer_array.append([id, vuln, work, 1, fix, vuln_old, work_old, class_old])
        elif fix == "no":
            second_analyzer_array.append([id, vuln, work , class_, fix, vuln_old, work_old, class_old])
    
    json_obj_list = []
    with open('./second_analyzer/second-analyzer.json', 'w') as fixer_file:
        for obj in second_analyzer_array:
            json_obj_list.append(OrderedDict((
                                            ("id", obj[0]), ("vuln", obj[1]), ("work", obj[2]), ("class", obj[3]), 
                                            ("fix", obj[4]), ("vuln_old", obj[5]), ("work_old", obj[6]), ("class_old", obj[7])
                                            )))
        json.dump(json_obj_list, fixer_file, indent=4) 