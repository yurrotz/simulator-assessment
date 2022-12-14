import first_analyzer.first_analyzer as first_analyzer
import fixer.fixer as fixer
import second_analyzer.second_analyzer as second_analyzer
import sys

sensitivity, specificity = float(sys.argv[1]), float(sys.argv[2])
fix_rate, break_rate = float(sys.argv[3]), float(sys.argv[4])

first_analyzer.first_analyzer(sensitivity, specificity)
fixer.fixer(fix_rate, break_rate)
second_analyzer.second_analyzer(sensitivity, specificity)

# id - GT - Vulnerable outcome - work
    
tp, fp, tn, fn, num_vuln, num_not_vuln, num_work = 0, 0, 0, 0, 0, 0, 0

for obj in second_analyzer.second_analyzer_array:
    
    vuln, work, class_, fix, vuln_old, class_old  = obj[1], obj[2], obj[3], obj[4], obj[5], obj[7]
    
    if vuln:
        num_vuln = num_vuln + 1
    else:
        num_not_vuln = num_not_vuln + 1
    
    if work:
        num_work = num_work + 1
        
    if fix == "no":
        if vuln == 0 and class_ == 0:
            tn = tn + 1
            
        elif vuln == 1 and class_ == 0:
            fn = fn + 1
            
    elif fix == "yes":
        if ((vuln == 0 and class_ == 0 and vuln_old == 1 and class_old == 1) or
            (vuln == 0 and class_ == 0 and vuln_old == 0 and class_old == 1)):
            tn = tn + 1
        
        elif vuln == 1 and class_ == 0 and vuln_old == 1 and class_old == 1:
            fn = fn + 1  
            
        elif vuln == 1 and class_ == 1 and vuln_old == 1 and class_old == 1:
            tp = tp + 1 
            
        elif ((vuln == 0 and class_ == 1 and vuln_old == 1 and class_old == 1) or
              (vuln == 0 and class_ == 1 and vuln_old == 0 and class_old == 1)):
            fp = fp + 1
                
print('TP: ' + str(tp) + ' ' , 'FP: ' + str(fp) + ' ' + 'TN: ' + str(tn) + ' ' + 'FN: ' + str(fn))
print('P: ' + str(num_vuln) + ' ', 'N: ' + str(num_not_vuln) + ' ', 'W: ' + str(num_work))