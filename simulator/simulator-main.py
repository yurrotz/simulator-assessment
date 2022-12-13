import first_analyzer.first_analyzer as first_analyzer
import sys

sensitivity, specificity = float(sys.argv[1]), float(sys.argv[2])

first_analyzer.first_analyzer(sensitivity, specificity)