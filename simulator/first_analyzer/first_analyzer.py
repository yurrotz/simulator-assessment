import json
import random
from collections import OrderedDict

# 0 NOT vulnerable/work | 1 vulnerable/work

ground_truth_array = []

with open('../ground_truth_generator/ground-truth.json') as ground_truth_file:    
    data = json.load(ground_truth_file)
    for obj in data:
        ground_truth_array.append([obj["id"],obj["vuln"],obj["work"]])
ground_truth_file.close()

first_analyzer_array = [] # id - vuln - work - class - fix - vuln_old - work_old - class_old

#1st Analyzer
def first_analyzer(sensitivity, specificity):
    for obj in ground_truth_array:
        sens = random.random()
        spec = random.random()
        if obj[1] == 1: # vulnerable
            if sens <= sensitivity:
                first_analyzer_array.append([obj[0],obj[1],obj[2],1,"unknown","unknown","unknown","unknown"]) #true positive
            else:
                first_analyzer_array.append([obj[0],obj[1],obj[2],0,"unknown","unknown","unknown","unknown"]) #false negative
        elif obj[1] == 0: # NOT vulnerable
            if spec <= specificity:
                first_analyzer_array.append([obj[0],obj[1],obj[2],0,"unknown","unknown","unknown","unknown"]) #true negative
            else:
                first_analyzer_array.append([obj[0],obj[1],obj[2],1,"unknown","unknown","unknown","unknown"]) #false positive
    #print(first_analyzer_array)         
    json_obj_list = []
    with open('./first_analyzer/first-analyzer.json', 'w') as first_analyzer_file:
        for obj in first_analyzer_array:
            json_obj_list.append(OrderedDict((
                                            ("id", obj[0]), ("vuln", obj[1]), ("work", obj[2]), ("class", obj[3]), 
                                            ("fix", obj[4]), ("vuln_old", obj[5]), ("work_old", obj[6]), ("class_old", obj[7])
                                            )))
        json.dump(json_obj_list, first_analyzer_file, indent=4) 