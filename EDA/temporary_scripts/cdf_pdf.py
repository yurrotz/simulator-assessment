import numpy as np
from scipy.stats import beta, levy_l
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(1, 1)

a = 43.13
b = 0.70

numbers = beta.rvs(a=20, b=3, loc=0.87, scale=0.016, size=100)

x = np.linspace(0, 1, 100000)

plt.plot(x, beta.pdf(x, a=2, b=5, loc=0, scale=1))
plt.plot(x, beta.cdf(x, a=2, b=5, loc=0, scale=1))
plt.plot(x, levy_l.cdf(x, loc=0, scale=1))

#sns.histplot(numbers, kde=True, element='step', ax=ax)

plt.show()