import first_analyzer.first_analyzer as first_analyzer
import fixer.fixer as fixer
import second_analyzer.second_analyzer as second_analyzer
from scipy.stats import *
import sys
import getopt

# specificity_values = [round(x * 0.1, 1) for x in range(1, 11)]
specificity_values = [x / 100 for x in range(1, 101, 1)]
specificity_values.insert(0, 0)
print(specificity_values)
fixrate_values = [round(x * 0.1, 1) for x in range(0, 11)]
break_rate = 0

header = False
write_mode = 'w'

arg_rounds = ""
arg_help = "{0} -r <rounds_number>".format(sys.argv[0])

try:
    opts, args = getopt.getopt(sys.argv[1:], "h:r:", ["help", "rounds="])
except:
    print(arg_help)
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-h", "--help"):
        print(arg_help)  # print the help message
        sys.exit(2)
    elif opt in ("-r", "--rounds_number"):
        arg_rounds = arg

rounds = int(arg_rounds)

for r in range(rounds):
    print("Round: " + str(r))

    for specificity in specificity_values:

        r = 0.5
        sensitivity = pow(1 - specificity, 1 - r)

        # (1 - pow(math.e, -(1 - specificity)))/(1 - pow(math.e, -1))

        for fix_rate in fixrate_values:
            tot, p_init, n_init, pw_init, nw_init, tp1, fp1, tn1, fn1 = first_analyzer.first_analyzer(sensitivity,
                                                                                                      specificity)
            p_infix, n_infix, pw_infix, nw_infix, p_outfix, n_outfix, pw_outfix, nw_outfix = fixer.fixer(fix_rate,
                                                                                                         break_rate)
            p_out, n_out, pw_out, nw_out, tp2, fp2, tn2, fn2 = second_analyzer.second_analyzer(sensitivity, specificity)

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

            with open('results_automated.csv', write_mode, encoding='UTF8', newline='') as f:
                writer = csv.writer(f)

                if not header:
                    header = ["prevalence_rate", "work_rate", "sensitivity", "specificity", "fix_rate", "break_rate",
                              "tot", "Pinit", "Ninit", "PWinit", "NWinit",
                              "TP1", "FP1", "TN1", "FN1",
                              "Pinfix", "Ninfix", "PWinfix", "NWinfix",
                              "Poutfix", "Noutfix", "PWoutfix", "NWoutfix",
                              "TP2", "FP2", "TN2", "FN2",
                              "Pout", "Nout", "PWout", "NWout",
                              "TPout", "FPout", "TNout", "FNout",
                              "Accuracy", "Precision", "Sensitivity"]

                    writer.writerow(header)
                    header = True
                    write_mode = 'a'

                data = [0.5, 0, sensitivity, specificity, fix_rate, break_rate,
                        tot, p_init, n_init, pw_init, nw_init,
                        tp1, fp1, tn1, fn1,
                        p_infix, n_infix, pw_infix, nw_infix,
                        p_outfix, n_outfix, pw_outfix, nw_outfix,
                        tp2, fp2, tn2, fn2,
                        p_out, n_out, pw_out, nw_out,
                        tp_out, fp_out, tn_out, fn_out,
                        accuracy_out, precision_out, sensitivity_out]

                # print(data)

                writer.writerow(data)