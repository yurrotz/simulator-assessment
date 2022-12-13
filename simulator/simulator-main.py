import first_analyzer.first_analyzer as first_analyzer
import fixer.fixer as fixer
import sys

sensitivity, specificity = float(sys.argv[1]), float(sys.argv[2])
fix_rate, break_rate = float(sys.argv[3]), float(sys.argv[4])

first_analyzer.first_analyzer(sensitivity, specificity)
fixer.fixer(fix_rate, break_rate)