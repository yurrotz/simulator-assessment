#%%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#%%
simulator_results_data = pd.read_csv('../simulator/results_automated.csv')

y_sens_before = []
x_spec_before  = []
y_sens_after = []
x_spec_after  = []
y_pout = [] #50% prevalence
x_fixrate = [] #50% prevalence
x_precision = [] #50% prevalence


for index, row in simulator_results_data.iterrows():
  y_pout.append((simulator_results_data.loc[index, 'Pout']/simulator_results_data.loc[index, 'Pinit']))
  x_fixrate.append(simulator_results_data.loc[index, 'fix_rate'])
  
  y_sens_before.append(simulator_results_data.loc[index, 'sensitivity'])
  x_spec_before.append(1 - simulator_results_data.loc[index, 'specificity'])
  
  
  
  tpout = simulator_results_data.loc[index, 'TPout']
  tnout = simulator_results_data.loc[index, 'TNout']
  fpout = simulator_results_data.loc[index, 'FPout']
  fnout = simulator_results_data.loc[index, 'FNout']
  
  y_sens_after.append(tpout/(tpout+fnout))
  x_spec_after.append(1 - (tnout/(tnout+fpout)))
  
  #fpout1 = simulator_results_data.loc[index, 'FPout']
  #precision1 = tpout1 / (tpout1 + fpout1)
  #x_precision.append(precision1)

  
# %%
#plt.scatter(x_fixrate, y_pout, marker='o', label = "Prevalence rate 50%")

plt.scatter(x_spec_before, y_sens_before, marker='o', label = "Prevalence rate 50%")
plt.xlabel("False Alert Rate = 1 - specificity")
plt.ylabel("sensitivity")
ticks = [round(x * 0.1, 1) for x in range(1, 11)]
ticks.insert(0,0)
plt.xticks(ticks)
plt.yticks(ticks)
plt.text(0.01, 1, "1 - spec^(1/5)")

#sns.stripplot(data = simulator_results_data, x="x", y="y", jitter=0.2, size=2)
#plt.show()

#%%
plt.scatter(x_spec_after, y_sens_after, marker='o', label = "Prevalence rate 50%")
plt.xlabel("False Alert Rate = 1 - specificity")
plt.ylabel("sensitivity")
ticks = [round(x * 0.1, 1) for x in range(1, 11)]
ticks.insert(0,0)
plt.xticks(ticks)
plt.yticks(ticks)
plt.text(0.01, 1, "1 - spec^(1/5)")

#%%
plt.scatter(x_precision, y_pout, marker='o', label = "Prevalence rate 50%")

#%%
plt.scatter(x_fixrate, y_pout, marker='o', label = "Prevalence rate 50%")

#%%
plt.scatter(y_sens_after, y_pout, marker='o', label = "Prevalence rate 50%")

# %%
plt.scatter(y_sens_before, y_pout, marker='o', label = "Prevalence rate 50%")

# %%
