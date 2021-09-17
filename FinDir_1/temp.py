import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from mpl_toolkits.mplot3d import Axes3D

options_1 = pd.read_csv('./New_option_prices_1.csv', header=None, names=["Maturity", "Strike", "Price"])
options_2 = pd.read_csv('./New_option_prices_2.csv', header=None, names=["Maturity", "Strike", "Price"])

#options_1['dt_backwards'] = options_1.groupby('Strike').apply(lambda x: x['Price'].diff(-1)/x['Maturity'].diff(-1)).reset_index(level=0)[0]
options_1['dt_forwards'] = options_1.groupby('Strike').apply(lambda x: x['Price'].diff(-1)/x['Maturity'].diff(-1)).reset_index(level=0)[0]
options_1['dK2'] = options_1[['Maturity', 'Strike','Price']].groupby('Maturity').apply(lambda x: (x['Price'].shift(1) - 2*x['Price'] + x['Price'].shift(-1))/100).reset_index(level=0)['Price']
options_1['iv'] = np.sqrt(2*options_1['dt_forwards']/(options_1['Strike']**2 *options_1['dK2']))

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Make data.
X = options_1['Maturity'].unique()
Y = options_1['Strike'].unique()
X, Y = np.meshgrid(X, Y)
Z = []
for i in range(5):
    Z.append(options_1['iv'].iloc[i*21:(i+1)*21].values)
Z = np.transpose(np.array(Z))

# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)

# Customize the z axis.
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()