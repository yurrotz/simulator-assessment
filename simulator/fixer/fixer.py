import json
import random
from collections import OrderedDict
import first_analyzer.first_analyzer as first_analyzer

# 0 NOT vulnerable/work | 1 vulnerable/work

def fixer(fix_rate, break_rate):
    #fixer_array is populated with the list of objects including ground truth vulnerable/not vulnerable, working/not working
    #and the classification made by the first analyzer. In this part we consider only the objects that has been classified as
    #positive from the first analyzer. The objects that were classified as negative do not pass through the fixer.  
    global fixer_array
    fixer_array = []
    global p_infix, n_infix, pw_infix, nw_infix
    #p_infix -> input for the fixer, number of positive objects 
    #n_infix -> input for the fixer, number of negative objects
    #pw_infix -> input for the fixer, number of positive objects and working objects
    #nw_infix -> input for the fixer, number of negative objects and working objects
    p_infix, n_infix, pw_infix, nw_infix = 0, 0, 0, 0
    global p_outfix, n_outfix, pw_outfix, nw_outfix
    #p_outfix -> output from the fixer, number of positive objects 
    #n_outfix -> output from the fixer, number of negative objects
    #pw_outfix -> output from the fixer, number of positive objects and working objects
    #nw_outfix -> output from the fixer, number of negative objects and working objects
    p_outfix, n_outfix, pw_outfix, nw_outfix = 0, 0, 0, 0
    
    for obj in first_analyzer.first_analyzer_array:
        random_fix = random.random() #random number for fix
        random_break = random.random() #randon number for break
        
        id, vuln, work, class_ = obj[0], obj[1], obj[2], obj[3]
        if vuln == 1 and class_ == 1: #positive objects classified as positive
            p_infix = p_infix + 1 #increase the number of positive objects
            if work == 1:
                pw_infix = pw_infix + 1 #increase the number of positive working objects
        elif vuln == 0 and class_ == 1: #negative objects classified as negative
            n_infix = n_infix + 1 #increase the number of negative objects
            if work == 1:
                nw_infix = nw_infix + 1 #increase the number of negative working objects
        
        
        if class_ == 1: #we consider only the objects classified as vulnerable
            if random_fix <= fix_rate and random_break <= break_rate: #the object is fixed & broken
                fixer_array.append([id, 0, 0, "unknown", "yes", vuln, work, class_])
                
            elif random_fix <= fix_rate and random_break > break_rate: #the object is fixed & NOT broken
                fixer_array.append([id, 0, work, "unknown", "yes", vuln, work, class_])
                
            elif random_fix > fix_rate and random_break > break_rate: #the object is NOT fixed & NOT broken
                fixer_array.append([id, vuln, work, "unknown", "yes", vuln, work, class_])
                
            elif random_fix > fix_rate and random_break <= break_rate: #the object is NOT fixed & broken
                fixer_array.append([id, vuln, 0, "unknown", "yes", vuln, work, class_]) 
                
        elif class_ == 0: #the objects classfied as NOT vulnerable
            fixer_array.append([id, vuln, work, class_, "no", "unknown", "unknown", "unknown"])          
         
    json_obj_list = []
    with open('fixer.json', 'w') as fixer_file:
        for obj in fixer_array:
            
            if obj[1] == 1: #the object is not fixed, therefore is positive 
                p_outfix = p_outfix + 1 #increase the number of positive objects
                if obj[2] == 1: #the object is NOT broken 
                    pw_outfix = pw_outfix + 1 #increase the number of positive working objects
            else: #the object is fixed, therefore is negative 
                n_outfix = n_outfix + 1 #increase the number of negative objects
                if obj[2] == 1: #the object is NOT broken 
                    nw_outfix = nw_outfix + 1 #increase the number of negative working objects
            
            #create the list of objects after the fixer         
            json_obj_list.append(OrderedDict((
                                            ("id", obj[0]), ("vuln", obj[1]), ("work", obj[2]), ("class", obj[3]), 
                                            ("fix", obj[4]), ("vuln_old", obj[5]), ("work_old", obj[6]), ("class_old", obj[7])
                                            )))
            #id -> object identifier
            #vuln -> vulnerable/not vulnerable, this parameter is changed by the fixer. It's the new ground truth
            #work -> working/not working, this parameter is changed by the fixer. It's the new ground truth
            #class -> after the fixer is "unknown". This parameter will be changed by the second analyzer
            #fix -> the object has been touched by the fixer
            #vuln_old -> previous status of the object before the fixer: vulnerable/not vulnerable
            #work_old -> previous status of the object before the fixer: working/not working
            #class_old -> the classification made by the first analyzer: positive/negative
        json.dump(json_obj_list, fixer_file, indent=4) 
        
    return p_infix, n_infix, pw_infix, nw_infix, p_outfix, n_outfix, pw_outfix, nw_outfix
        
    