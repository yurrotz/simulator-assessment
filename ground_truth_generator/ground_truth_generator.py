import json
import random
import sys
import getopt

# 0 NOT vulnerable/work | 1 vulnerable/work

#num_obj, vuln_rate, work_rate = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])

"""
arg_num_obj= ""
arg_vuln_rate = ""
arg_work_rate = ""

# The Ground Truth generator takes as input:
# <num_obj> total number of objects
# <vuln_rate> rate of vulnerable objects -> how many objects are vulnerable
# <vuln_rate> rate of working objects -> how many objects work
arg_help = "{0} -n <num_obj> -v <vuln_rate> -w <work_rate>".format(sys.argv[0])

try:
    opts, args = getopt.getopt(sys.argv[1:], "hn:v:w:", ["help", "num_obj=", 
    "vuln_rate=", "work_rate="])
except:
    print(arg_help)
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-h", "--help"):
        print(arg_help)  # print the help message
        sys.exit(2)
    elif opt in ("-n", "--num_obj"):
        arg_num_obj = arg
    elif opt in ("-v", "--vuln_rate"):
        arg_vuln_rate = arg
    elif opt in ("-w", "--work_rate"):
        arg_work_rate = arg
"""


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