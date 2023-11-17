import first_analyzer.first_analyzer as first_analyzer
import fixer.fixer as fixer
import second_analyzer.second_analyzer as second_analyzer
import sys
import getopt
import csv

arg_sensitivity= ""
arg_specificity = ""
arg_fix_rate = ""
arg_break_rate = ""
arg_run_times = ""
arg_new_csv = ""
write_mode = ""
arg_help = "{0} -r <sensitivity> -s <specificity> -f <fix_rate> -b <break_rate> -t <run_times> -n <new_csv>".format(sys.argv[0])

try:
    opts, args = getopt.getopt(sys.argv[1:], "h:r:s:f:b:t:n:", ["help", "sensitivity=", 
    "specificity=", "fix_rate=", "break_rate=", "run_times=", "new_csv="])
except:
    print(arg_help)
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-h", "--help"):
        print(arg_help)  # print the help message
        sys.exit(2)
    elif opt in ("-r", "--sensitivity"):
        arg_sensitivity = arg
    elif opt in ("-s", "--specificity"):
        arg_specificity = arg
    elif opt in ("-f", "--fix_rate"):
        arg_fix_rate = arg
    elif opt in ("-b", "--break_rate"):
        arg_break_rate = arg
    elif opt in ("-t", "--run_times"):
        arg_run_times = arg
    elif opt in ("-n", "--new_csv"):
        arg_new_csv = arg

sensitivity = float(arg_sensitivity)
specificity = float(arg_specificity)
fix_rate = float(arg_fix_rate)
break_rate = float(arg_break_rate)
run_times = int(arg_run_times)
new_csv = int(arg_new_csv)

json_obj_list = []

 
for time in range (run_times):
    
    if new_csv == 1 and time == 0:
        write_mode = 'w'
    else:
        write_mode = 'a'
    
    tot, p_init, n_init, pw_init, nw_init, tp1, fp1, tn1, fn1 = first_analyzer.first_analyzer(sensitivity, specificity)
    p_infix, n_infix, pw_infix, nw_infix, p_outfix, n_outfix, pw_outfix, nw_outfix = fixer.fixer(fix_rate, break_rate)
    p_out, n_out, pw_out, nw_out, tp2, fp2, tn2, fn2 = second_analyzer.second_analyzer(sensitivity, specificity)

    vuln_rate = round(p_init/tot, 1)
    work_rate = round((pw_init + nw_init)/tot, 1)
    tp_out = tp2
    fp_out = fp2
    tn_out = tn1 + tn2
    fn_out = fn1 + fn2

    accuracy_out = (tp_out + tn_out) / (tp_out + fp_out + tn_out + fn_out)

    if (tp_out + fp_out) != 0: 
        precision_out = tp_out / (tp_out + fp_out)
    else:
        precision_out = "err"
        
    if (tp_out + fn_out) != 0: 
        sensitivity_out = tp_out / (tp_out + fn_out)
    else:
        sensitivity_out = "err"

    with open('results.csv', write_mode, encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        if new_csv == 1 and time == 0:
            header = ["prevalence_rate","work_rate","sensitivity", "specificity", "fix_rate", "break_rate", 
                    "tot", "Pinit", "Ninit", "PWinit", "NWinit",
                    "TP1", "FP1", "TN1", "FN1",
                    "Pinfix", "Ninfix", "PWinfix", "NWinfix",
                    "Poutfix", "Noutfix", "PWoutfix", "NWoutfix",
                    "TP2", "FP2", "TN2", "FN2",
                    "Pout", "Nout", "PWout", "NWout",
                    "TPout", "FPout", "TNout", "FNout",
                    "Accuracy", "Precision", "Sensitivity"]
            
            writer.writerow(header)
        
        data = [vuln_rate, work_rate, sensitivity, specificity, fix_rate, break_rate, 
                tot, p_init, n_init, pw_init, nw_init,
                tp1, fp1, tn1, fn1,
                p_infix, n_infix, pw_infix, nw_infix,
                p_outfix, n_outfix, pw_outfix, nw_outfix,
                tp2, fp2, tn2, fn2,
                p_out, n_out, pw_out, nw_out,
                tp_out, fp_out, tn_out, fn_out,
                accuracy_out, precision_out, sensitivity_out]
        
        writer.writerow(data)