import json
import random
from collections import OrderedDict
import first_analyzer.first_analyzer as first_analyzer

# 0 NOT vulnerable/work | 1 vulnerable/work

def fixer(fix_rate, break_rate):  
    global fixer_array
    fixer_array = []
    global p_infix, n_infix, pw_infix, nw_infix
    p_infix, n_infix, pw_infix, nw_infix = 0, 0, 0, 0
    global p_outfix, n_outfix, pw_outfix, nw_outfix
    p_outfix, n_outfix, pw_outfix, nw_outfix = 0, 0, 0, 0
    
    for obj in first_analyzer.first_analyzer_array:
        random_fix = random.random() #fix
        random_break = random.random() #break
        
        id, vuln, work, class_ = obj[0], obj[1], obj[2], obj[3]
        if vuln == 1 and class_ == 1:
            p_infix = p_infix + 1
            if work == 1:
                pw_infix = pw_infix + 1
        elif vuln == 0 and class_ == 1:
            n_infix = n_infix + 1
            if work == 1:
                nw_infix = nw_infix + 1
        
        
        if class_ == 1:
            if random_fix <= fix_rate and random_break <= break_rate: #fixed & broken
                fixer_array.append([id, 0, 0, "unknown", "yes", vuln, work, class_])
                
            elif random_fix <= fix_rate and random_break > break_rate: #fixed & NOT broken
                fixer_array.append([id, 0, work, "unknown", "yes", vuln, work, class_])
                
            elif random_fix > fix_rate and random_break > break_rate: #NOT fixed & NOT broken
                fixer_array.append([id, vuln, work, "unknown", "yes", vuln, work, class_])
                
            elif random_fix > fix_rate and random_break <= break_rate: #NOT fixed & broken
                fixer_array.append([id, vuln, 0, "unknown", "yes", vuln, work, class_]) 
                
        elif class_ == 0:
            fixer_array.append([id, vuln, work, class_, "no", "unknown", "unknown", "unknown"])          
         
    json_obj_list = []
    with open('./fixer/fixer.json', 'w') as fixer_file:
        for obj in fixer_array:
            
            if obj[1] == 1:
                p_outfix = p_outfix + 1
                if obj[2] == 1:
                    pw_outfix = pw_outfix + 1
            else:
                n_outfix = n_outfix + 1
                if obj[2] == 1:
                    nw_outfix = nw_outfix + 1
                    
            json_obj_list.append(OrderedDict((
                                            ("id", obj[0]), ("vuln", obj[1]), ("work", obj[2]), ("class", obj[3]), 
                                            ("fix", obj[4]), ("vuln_old", obj[5]), ("work_old", obj[6]), ("class_old", obj[7])
                                            )))
        json.dump(json_obj_list, fixer_file, indent=4) 
        
    return p_infix, n_infix, pw_infix, nw_infix, p_outfix, n_outfix, pw_outfix, nw_outfix
        
    