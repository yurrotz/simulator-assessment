import json
import random

# 0 NOT vulnerable/work | 1 vulnerable/work

def create_ground_truth(vuln_rate, work_rate, num_obj):
    json_obj_list = []

    with (open('/Users/manu/Documents/GitHub/simulator-assessment/ground_truth_generator/ground_truth.json', 'w')
          as ground_truth_file):

        print(f"New ground truth with: {vuln_rate}, {work_rate} e {num_obj}")

        vulnerable = 0
        not_vulnerable = 0

        for i in range(num_obj):
            random_vuln = random.random() #generate random number for the vuln rate
            random_work = random.random() #generate random number for the work rate

            if random_vuln > vuln_rate: #if random_vuln is bigger than vuln_rate then the object is NOT vulnerable
                vuln = 0
                not_vulnerable += 1
            else: #the object is vulnerable
                vuln = 1
                vulnerable += 1

            if random_work > work_rate: #if random_work is bigger than work_rate then the object is NOT # working (e.g. a bug is present)
                work = 0
            else: #the object is working
                work = 1
            #create the json list containing the list of objects and their vuln and work ground truth
            json_obj_list.append({"id": i, "vuln": vuln, "work": work})

        print(f"Vulnerable: {vulnerable}, Not vulnerable: {not_vulnerable}")
        json.dump(json_obj_list, ground_truth_file, indent=4) #copy the json list in json file