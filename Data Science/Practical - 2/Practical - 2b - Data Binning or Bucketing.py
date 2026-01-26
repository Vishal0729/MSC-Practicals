import numpy as np
import matplotlib.pyplot as plt
from math import exp, sqrt, pi

np.random.seed(0)

# example data
mu = 90
sigma = 25
x = mu + sigma * np.random.randn(5000)

num_bins = 25
fig, ax = plt.subplots()

# histogram
n, bins, patches = ax.hist(x, num_bins, density=True, alpha=0.6)

# normal distribution fit (no SciPy needed)
def normal_pdf(x, mu, sigma):
    return (1 / (sigma * sqrt(2 * pi))) * exp(-0.5 * ((x - mu) / sigma)**2)

y = [normal_pdf(b, mu, sigma) for b in bins]
ax.plot(bins, y, '--')
ax.set_xlabel('Example Data')
ax.set_ylabel('Probability density')

sTitle = (
    fr'Histogram {len(x)} entries into {num_bins} Bins: '
    fr'$\mu={mu}$, $\sigma={sigma}$'
)
ax.set_title(sTitle)
fig.tight_layout()

sPathFig = 'D:/MSC Practicals/Data Science/Practical - 2/Outputs/DU-Histogram.png'
fig.savefig(sPathFig)

plt.show()

