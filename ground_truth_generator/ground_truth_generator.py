import json
import random
import sys
import getopt

# 0 NOT vulnerable/work | 1 vulnerable/work

#num_obj, vuln_rate, work_rate = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])

arg_num_obj= ""
arg_vuln_rate = ""
arg_work_rate = ""
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

json_obj_list = []

num_obj = int(arg_num_obj)
vuln_rate = float(arg_vuln_rate)
work_rate = float(arg_work_rate)

with open('ground-truth.json', 'w') as ground_truth_file:
    
    for i in range(num_obj):
        random_vuln = random.random()
        random_work = random.random()

        if random_vuln > vuln_rate:
            vuln = 0
        else:
            vuln = 1

        if random_work > work_rate:
            work = 0
        else:
            work = 1

        json_obj_list.append({"id": i, "vuln": vuln, "work": work})
    json.dump(json_obj_list, ground_truth_file, indent=4)