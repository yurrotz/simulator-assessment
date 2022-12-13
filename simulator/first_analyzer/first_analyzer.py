import json
import random

# 0 NOT vulnerable/work | 1 vulnerable/work

ground_truth_array = []

with open('../ground_truth_generator/ground-truth.json') as ground_truth_file:    
    data = json.load(ground_truth_file)
    for obj in data:
        ground_truth_array.append([obj["id"],obj["vulnerable"],obj["work"]])
ground_truth_file.close()

first_analyzer_array = []

#1st Analyzer
def first_analyzer(sensitivity, specificity):
    for obj in ground_truth_array:
        sens = random.random()
        spec = random.random()
        if obj[1] == 1: #positive
            if sens <= sensitivity:
                first_analyzer_array.append([obj[0],obj[1],1,obj[2]]) #true positive
            else:
                first_analyzer_array.append([obj[0],obj[1],0,obj[2]]) #false negative
        elif obj[1] == 0: #negative
            if spec <= specificity:
                first_analyzer_array.append([obj[0],obj[1],0,obj[2]]) #true negative
            else:
                first_analyzer_array.append([obj[0],obj[1],1,obj[2]]) #false positive
                
    json_obj_list = []
    with open('./first_analyzer/first-analyzer.json', 'w') as first_analyzer_file:
        for obj in first_analyzer_array:
            json_obj_list.append({"id": obj[0], "vulnerable": obj[1], "1a-vulnerable": obj[2], "work": obj[3]})
        json.dump(json_obj_list, first_analyzer_file, indent=4) 