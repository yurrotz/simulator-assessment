import json
import random
import fixer.fixer as fixer

# 0 NOT vulnerable/work | 1 vulnerable/work

second_analyzer_array = []

def second_analyzer(sensitivity, specificity):
    for obj in fixer.fixer_array:
        sens = random.random()
        spec = random.random()
        
        if obj[3] != "no fixer":
            if obj[2] == 1:
                if sens <= sensitivity:
                    second_analyzer_array.append([obj[0],obj[1],obj[2],obj[3],1,obj[4]])
                else:
                    second_analyzer_array.append([obj[0],obj[1],obj[2],obj[3],0,obj[4]])
            elif obj[2] == 0:
                if spec <= specificity:
                    if sens <= sensitivity:
                        second_analyzer_array.append([obj[0],obj[1],obj[2],obj[3],0,obj[4]])
                    else:
                        second_analyzer_array.append([obj[0],obj[1],obj[2],obj[3],1,obj[4]])
        else:
            second_analyzer_array.append([obj[0],obj[1],obj[2],obj[3],"no second analyzer",obj[4]])
    
    json_obj_list = []
    with open('./second_analyzer/second_analyzer.json', 'w') as fixer_file:
        for obj in second_analyzer_array:
            json_obj_list.append({"id": obj[0], "vulnerable": obj[1], "1a-vulerable": obj[2], "fixer": obj[3], "2a-vulnerable": obj[4], "work": obj[5]})
        json.dump(json_obj_list, fixer_file, indent=4) 