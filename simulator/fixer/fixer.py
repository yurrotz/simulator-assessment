import json
import random
import first_analyzer.first_analyzer as first_analyzer

# 0 NOT vulnerable/work | 1 vulnerable/work

fixer_array = []

def fixer(fix_rate, break_rate):
    for obj in first_analyzer.first_analyzer_array:
        
        random_fix = random.random() #fix
        random_break = random.random() #break
        
        if obj[2] == 1:
            if random_fix <= fix_rate and random_break <= break_rate: #not vulnerable and broken
                fixer_array.append([obj[0],obj[1],obj[2],0,0])
            elif random_fix <= fix_rate and random_break > break_rate: #not vulnerable and work
                fixer_array.append([obj[0],obj[1],obj[2],0,1])
            elif random_fix > fix_rate and random_break > break_rate: #vulnerable and work
                fixer_array.append([obj[0],obj[1],obj[2],1,1])
            elif random_fix > fix_rate and random_break <= break_rate: #vulnerable and broken
                fixer_array.append([obj[0],obj[1],obj[2],1,0])   
        else:
            fixer_array.append([obj[0],obj[1],obj[2],"no fixer",obj[3]])          
         
    json_obj_list = []
    with open('./fixer/fixer.json', 'w') as fixer_file:
        for obj in fixer_array:
            json_obj_list.append({"id": obj[0], "vulnerable": obj[1], "1a-vulerable": obj[2], "fixer": obj[3], "work": obj[4]})
        json.dump(json_obj_list, fixer_file, indent=4) 
        
    