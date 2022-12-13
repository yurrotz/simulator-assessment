import first_analyzer.first_analyzer as first_analyzer
import fixer.fixer as fixer
import second_analyzer.second_analyzer as second_analyzer
import sys
import json

sensitivity, specificity = float(sys.argv[1]), float(sys.argv[2])
fix_rate, break_rate = float(sys.argv[3]), float(sys.argv[4])

first_analyzer.first_analyzer(sensitivity, specificity)
fixer.fixer(fix_rate, break_rate)
second_analyzer.second_analyzer(sensitivity, specificity)

# id - GT - Vulnerable outcome - work

outcome_array = []

for obj in second_analyzer.second_analyzer_array:
    if obj[2] == 0: #the object did not go through the fixer and the second analyzer
        outcome_array.append([obj[0], obj[1], obj[2], obj[5]])
    
    elif obj[2] == 1:
        if obj[1] == 1:
            outcome_array.append([obj[0], obj[3], obj[4], obj[5]])
        elif obj[1] == 0:
            outcome_array.append([obj[0], obj[1], obj[4], obj[5]])
            
json_obj_list = []
with open('simulator-assessment.json', 'w') as simulator_assessment_file:
    for obj in outcome_array:
        json_obj_list.append({"id": obj[0], "gt*": obj[1], "vulnerable": obj[2], "work": obj[3]})
    json.dump(json_obj_list, simulator_assessment_file, indent=4) 
    
tp, fp, tn, fn = 0, 0, 0, 0

for obj in outcome_array:
    if obj[1] == 1 and obj[2] == 1: #true positive
        tp = tp + 1
    elif obj[1] == 0 and obj[2] == 1: #false positive
        fp = fp + 1
    elif obj[1] == 0 and obj[2] == 0: #true negative
        tn = tn + 1
    elif obj[1] == 1 and obj[2] == 0: #false negative
        fn = fn + 1
                
print('TP: ' + str(tp) + ' ' , 'FP: ' + str(fp) + ' ' + 'TN: ' + str(tn) + ' ' + 'FN: ' + str(fn) + ' ')