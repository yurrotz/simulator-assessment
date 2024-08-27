import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Parameters
n = 30  # number of trials
p_true = 0.6  # true probability of success
np.random.seed(42)

# Simulate data
data = np.random.binomial(1, p_true, n)
k = np.sum(data)  # number of successes

# Construct beta distributions for the edges of the c-box
alpha1, beta1 = k, n - k + 1
alpha2, beta2 = k + 1, n - k

x = np.linspace(0, 1, 1000)
beta1_cdf = stats.beta.cdf(x, alpha1, beta1)
beta2_cdf = stats.beta.cdf(x, alpha2, beta2)

# Plot the confidence distribution (CDF)
plt.fill_between(x, beta1_cdf, beta2_cdf, color='skyblue', alpha=0.4, label='C-Box')
plt.plot(x, beta1_cdf, 'b-', label=f'Beta({alpha1}, {beta1}) CDF')
plt.plot(x, beta2_cdf, 'r-', label=f'Beta({alpha2}, {beta2}) CDF')
plt.axvline(x=p_true, color='black', linestyle='--', label='True p')
plt.xlabel('Probability of Success (p)')
plt.ylabel('Cumulative Probability')
plt.title('Confidence Distribution (CDF) for Binomial Probability')
plt.legend()
plt.show()
