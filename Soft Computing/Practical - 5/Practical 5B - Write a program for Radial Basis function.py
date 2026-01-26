import numpy as np
from scipy.linalg import pinv
import matplotlib.pyplot as plt

# Step 1: Define Gaussian basis function
def rbf(x, c, beta=8):
    return np.exp(-beta * np.linalg.norm(x - c)**2)


# Step 2: Generate training data
x = np.linspace(-1, 1, 100).reshape(-1, 1)
y = np.sin(3 * (x + 0.5)**3 - 1)

# Step 3: Choose RBF centers
centers = np.linspace(-1, 1, 10).reshape(-1, 1)


# Step 4: Build activation matrix
G = np.zeros((x.shape[0], centers.shape[0]))
for i, xi in enumerate(x):
    for j, cj in enumerate(centers): 
        G[i, j] = rbf(xi, cj)

# Step 5: Solve for weights 
W = pinv(G) @ y

# Step 6: Predict
y_pred = G @ W 

# Step 7: Plot
plt.plot(x, y, label='True')
plt.plot(x, y_pred, label='RBF Approximation')
plt.legend()
plt.show() 

