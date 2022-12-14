import json
import random
from collections import OrderedDict
import first_analyzer.first_analyzer as first_analyzer

# 0 NOT vulnerable/work | 1 vulnerable/work

fixer_array = []

def fixer(fix_rate, break_rate):
    for obj in first_analyzer.first_analyzer_array:
        
        random_fix = random.random() #fix
        random_break = random.random() #break
        
        if obj[3] == 1: #class = 1
            if random_fix <= fix_rate and random_break <= break_rate: #not vulnerable and broken
                fixer_array.append([obj[0],0,0,"unknown","yes",obj[1],obj[2],obj[3]])
                
            elif random_fix <= fix_rate and random_break > break_rate: #not vulnerable and work
                fixer_array.append([obj[0],0,obj[2],"unknown","yes",obj[1],obj[2],obj[3]])
                
            elif random_fix > fix_rate and random_break > break_rate: #vulnerable and work
                fixer_array.append([obj[0],obj[1],obj[2],"unknown","yes",obj[1],obj[2],obj[3]])
                
            elif random_fix > fix_rate and random_break <= break_rate: #vulnerable and broken
                fixer_array.append([obj[0],obj[1],0,"unknown","yes",obj[1],obj[2],obj[3]]) 
                
        elif obj[3] == 0: #class = 0
            fixer_array.append([obj[0],obj[1],obj[2],obj[3],"no","unknown","unknown","unknown"])          
         
    json_obj_list = []
    with open('./fixer/fixer.json', 'w') as fixer_file:
        for obj in fixer_array:
            json_obj_list.append(OrderedDict((
                                            ("id", obj[0]), ("vuln", obj[1]), ("work", obj[2]), ("class", obj[3]), 
                                            ("fix", obj[4]), ("vuln_old", obj[5]), ("work_old", obj[6]), ("class_old", obj[7])
                                            )))
        json.dump(json_obj_list, fixer_file, indent=4) 
        
    