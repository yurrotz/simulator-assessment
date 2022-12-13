import json
import random
import sys

# 0 NOT vulnerable/work | 1 vulnerable/work

vuln_rate, work_rate = sys.argv[1], sys.argv[2]

json_obj_list = []

with open('ground-truth.json', 'w') as ground_truth_file:
    r = random.randint(50,100)
    vuln = 1
    work = 1
    for i in range(r):
        random_vuln = random.random()
        random_work = random.random()
        
        if random_vuln > float(vuln_rate):
            vuln = 0
                  
        if random_work > float(work_rate):
            work = 0
        
        json_obj_list.append({"id": i, "vulnerable": vuln, "work": work})
    json.dump(json_obj_list, ground_truth_file, indent=4)