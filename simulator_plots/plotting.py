import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd


min_sens_spec = [0.50, 0.60, 0.70, 0.80, 0.90]

y_50_train = [0.25, 0.30, 0.35, 0.40, 0.45]
y_50_test = [0.00, 0.16, 0.34, 0.50, 0.60]

y_70_train = [0.35, 0.42, 0.48, 0.55, 0.62]
y_70_test = [0.00, 0.15, 0.35, 0.53, 0.67]

y_90_train = [0.45, 0.54, 0.62, 0.72, 0.81]
y_90_test = [0.00, 0.18, 0.34, 0.55, 0.74]

y_100_train = [0.50, 0.60, 0.69, 0.80, 0.90]
y_100_test = [0.00, 0.17, 0.38, 0.58, 0.78]

fig, axs = plt.subplots(2, 2)

patch_test = mpatches.Patch(color='C0', label='train')
patch_train = mpatches.Patch(color='C1', label='test')

axs[0, 0].plot(min_sens_spec, y_50_train)
axs[0, 0].plot(min_sens_spec, y_50_test)
axs[0, 0].title.set_text("Theoretical Fr = 0.50")
axs[0, 0].legend(loc='lower right', labelspacing=0.70, handleheight=1.0, handlelength=1.0, borderpad=0.40,
              handles=[patch_train, patch_test])

axs[0, 1].plot(min_sens_spec, y_70_train)
axs[0, 1].plot(min_sens_spec, y_70_test)
axs[0, 1].title.set_text("Theoretical Fr = 0.70")
axs[0, 1].legend(loc='lower right', labelspacing=0.70, handleheight=1.0, handlelength=1.0, borderpad=0.40,
              handles=[patch_train, patch_test])

axs[1, 0].plot(min_sens_spec, y_90_train)
axs[1, 0].plot(min_sens_spec, y_90_test)
axs[1, 0].title.set_text("Theoretical Fr = 0.90")
axs[1, 0].legend(loc='lower right', labelspacing=0.70, handleheight=1.0, handlelength=1.0, borderpad=0.40,
              handles=[patch_train, patch_test])

axs[1, 1].plot(min_sens_spec, y_90_train)
axs[1, 1].plot(min_sens_spec, y_90_test)
axs[1, 1].title.set_text("Theoretical Fr = 1.00")
axs[1, 1].legend(loc='lower right', labelspacing=0.70, handleheight=1.0, handlelength=1.0, borderpad=0.40,
              handles=[patch_train, patch_test])

fig.supxlabel('Minimum Recall/Specificity')
fig.supylabel('Minimum Fr(aias)')

fig.tight_layout()
plt.savefig('train_test.png')

plt.show()
