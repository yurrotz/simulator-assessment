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
    
tp, fp, tn, fn = 0, 0, 0, 0

for obj in second_analyzer.second_analyzer_array:
    if obj[4] == "no": # I can obtain only TN or FN
        if obj[1] == 0 and obj[3] == 0:
            tn = tn + 1
        elif obj[1] == 1 and obj[3] == 0:
            fn = fn + 1
            
    elif obj[4] == "yes":
        if obj[1] == 0 and obj[3] == 0 and obj[5] == 1 and obj[7] == 1:
            tn = tn + 1
        
        elif obj[1] == 0 and obj[3] == 1 and obj[5] == 1 and obj[7] == 1:
            fp = fp + 1
        
        elif obj[1] == 1 and obj[3] == 0 and obj[5] == 1 and obj[7] == 1:
            fn = fn + 1  
            
        elif obj[1] == 1 and obj[3] == 1 and obj[5] == 1 and obj[7] == 1:
            tp = tp + 1 
            
        elif obj[1] == 0 and obj[3] == 0 and obj[5] == 0 and obj[7] == 1:
            fp = fp + 1 
            
        elif obj[1] == 0 and obj[3] == 1 and obj[5] == 0 and obj[7] == 1:
            fp = fp + 1 
            
        elif obj[1] == 1 and obj[3] == 0 and obj[5] == 0 and obj[7] == 1:
            fp = fp + 1 
            
        elif obj[1] == 1 and obj[3] == 1 and obj[5] == 0 and obj[7] == 1:
            fp = fp + 1
        
                
print('TP: ' + str(tp) + ' ' , 'FP: ' + str(fp) + ' ' + 'TN: ' + str(tn) + ' ' + 'FN: ' + str(fn) + ' ')