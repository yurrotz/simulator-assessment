import json
import random
from collections import OrderedDict
import fixer.fixer as fixer

# 0 NOT vulnerable/work | 1 vulnerable/work

def second_analyzer(sensitivity, specificity):
    
    #second_analyzer_array is filled with the list of objects including ground truth vulnerable/not vulnerable,
    #ground truth working/not working, classification from the second analyzer, touched by the fixed, and old status of the object
    global second_analyzer_array
    second_analyzer_array = []
    global p_out, n_out, pw_out, nw_out, tp2, fp2, tn2, fn2
    #p_out -> number of objects that are positive at the end (e.g. objects with a vulnerability)
    #n_out -> number of objects that are negative at the end (e.g. objects with no vulnerabilities)
    #pw_out -> number of objects that are positive at the end and working (e.g. objects with a vulnerability and no bugs)
    #nw_out -> number of objects that are negative at the end and working (e.g. objects with no vulnerabilities and no bugs)
    p_out, n_out, pw_out, nw_out, tp2, fp2, tn2, fn2 = 0, 0, 0, 0, 0, 0, 0, 0
    
    for obj in fixer.fixer_array:
        
        sens = random.random() #random number for sensitivity 
        spec = random.random() #random number for specificity
        
        id, vuln, work, class_, fix, vuln_old, work_old, class_old = obj[0], obj[1], obj[2], obj[3], obj[4], obj[5], obj[6], obj[7]
        #knowing the ground truth (number of positives and negatives) we count the number of TP, FP, TN, FN based on the classification
        #made by the second analyzer
        if fix == "yes": #we classify only the objects that have been touched by the fixer
            if vuln == 1: #the object is vulnerable
                if sens <= sensitivity: #the object is correctly classified as vulnerable
                    tp2 = tp2 + 1 #increase the number of TPs
                    second_analyzer_array.append([id, vuln, work, 1, fix, vuln_old, work_old, class_old]) #TP
                else: #the object is missclassified as NOT vulnerable
                    fn2 = fn2 + 1 #increase the number of FNs
                    second_analyzer_array.append([id, vuln, work , 0, fix, vuln_old, work_old, class_old]) #FN
            elif vuln == 0: #the object is NOT vulnerable
                if spec <= specificity: #the object is correctly classifies as NOT vulnerable
                    tn2 = tn2 + 1 #increate the number of TNs
                    second_analyzer_array.append([id, vuln, work , 0, fix, vuln_old, work_old, class_old]) #TN
                else: #the objects is missclassified as vulnerable
                    fp2 = fp2 + 1 #increase the number of FPs
                    second_analyzer_array.append([id, vuln, work, 1, fix, vuln_old, work_old, class_old]) #FP
        elif fix == "no":
            second_analyzer_array.append([id, vuln, work , class_, fix, vuln_old, work_old, class_old])
    
    #create a json list containing the objects with their ground truth and the classification made by the second analyzer  
    json_obj_list = []
    with open('./second_analyzer/second-analyzer.json', 'w') as fixer_file:
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