import json
import random
from collections import OrderedDict

# 0 NOT vulnerable/work | 1 vulnerable/work

#1st Analyzer
def first_analyzer(sensitivity, specificity):
    #ground_truth_array is populated with the list in ground_truth.json. It contains the list of the objects with the grounf truth
    #first_analyzer_array is populated with the list of objects including their ground truth, and the classification made by the first analyzer
    global ground_truth_array, first_analyzer_array
    ground_truth_array, first_analyzer_array = [], []
    #tot -> number of total objects
    #p_init -> number of objects that are positive (e.g. objects with a vulnerability)
    #n_init -> number of objects that are negative (e.g. objects with no vulnerabilities)
    #pw_init -> number of objects that are positive and working (e.g. objects with a vulnerability and no bugs)
    #nw_init -> number of objects that are negative and working (e.g. objects with no vulnerabilities and no bugs)
    global tot, p_init, n_init, pw_init, nw_init
    tot, p_init, n_init, pw_init, nw_init = 0, 0, 0, 0, 0

    #open the ground_truth_file and read the objects to fill the ground_truth_array
    with open('../ground_truth_generator/ground_truth.json') as ground_truth_file:
        data = json.load(ground_truth_file)
        for obj in data:
            tot = tot + 1 #counting the total number of objects one by one
            if obj["vuln"] == 1: #the objects is vulnerable
                p_init = p_init + 1 #increase the number of positive objects
                if obj["work"] == 1: #the objects is working
                    pw_init = pw_init + 1 #increase the number of positive objects working
            else: #the objects is NOT vulnerable
                n_init = n_init + 1 #increase the number of negative objects
                if obj["work"] == 1:
                    nw_init = nw_init + 1 #increase the number of negative objects working
            
            ground_truth_array.append([obj["id"],obj["vuln"],obj["work"]]) #fill the array with the object

    #knowing the ground truth (number of positives and negatives) we count the number of TP, FP, TN, FN based on the classification
    #made by the first analyzer
    global tp1, fp1, tn1, fn1
    tp1, fp1, tn1, fn1 = 0, 0, 0, 0
        
    for obj in ground_truth_array:
        sens = random.random() #create random number for sensitivity 
        spec = random.random() #create random number for specificity
        
        id, vuln, work = obj[0], obj[1], obj[2] #read the gruound truth of the object
        
        #sensitivity is the true positive rate
        #specificity is the true negative rate
        
        if vuln == 1: # the object is vulnerable
            if sens <= sensitivity: #the object is correctly classified as vulnerable
                tp1 = tp1 + 1 #increase the number of TPs
                first_analyzer_array.append([id, vuln, work, 1, "unknown", "unknown", "unknown", "unknown"]) #TP
            else: #the object is missclassified as NOT vulnerable
                fn1 = fn1 + 1 #increase the number of FNs
                first_analyzer_array.append([id, vuln, work, 0, "unknown", "unknown", "unknown", "unknown"]) #FN
        elif vuln == 0: #the object is NOT vulnerable
            if spec <= specificity: #the object is correctly classifies as NOT vulnerable
                tn1 = tn1 + 1 #increate the number of TNs
                first_analyzer_array.append([id, vuln, work, 0, "unknown", "unknown", "unknown", "unknown"]) #TN
            else: #the objects is missclassified as vulnerable
                fp1 = fp1 + 1 #increase the number of FPs
                first_analyzer_array.append([id, vuln, work, 1, "unknown", "unknown", "unknown", "unknown"]) #FP
    
    #create a json list containing the objects with their ground truth and the classification made by the first analyzer                     
    json_obj_list = []
    with open('first_analyzer.json', 'w') as first_analyzer_file:
        for obj in first_analyzer_array:
            #id -> object identifier
            #vuln -> ground truth of the object vulnerable/not vulnerable
            #work -> grount truth of the object working/not working
            #class -> classification made by the first analyzer
            #the other parameters are set later in the simulation, for the moment we keep the value "unknown"
            json_obj_list.append(OrderedDict((
                                            ("id", obj[0]), ("vuln", obj[1]), ("work", obj[2]), ("class", obj[3]), 
                                            ("fix", obj[4]), ("vuln_old", obj[5]), ("work_old", obj[6]), ("class_old", obj[7])
                                            )))
        json.dump(json_obj_list, first_analyzer_file, indent=4)
        
    return tot, p_init, n_init, pw_init, nw_init, tp1, fp1, tn1, fn1