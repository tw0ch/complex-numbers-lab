import numpy as np
import math
from matplotlib import pyplot as plt

# Joukowski transform parameters
lam = 1.0  # transform parameter
x0, y0 = -0.15, 0.1  # center of circle in z plane
R = 1.15  # circle radius

# curve in z plane
n = 2000

x = np.linspace(-R + x0, R + x0, n)
print(x)
yu = np.sqrt(R ** 2 - (x - x0) ** 2) + y0  # upper semi-circle
yl = -np.sqrt(R ** 2 - (x - x0) ** 2) + y0  # lower semi-circle

zu = x + 1j * yu  # upper curve
zl = x + 1j * yl  # lower curve

# zeta plane curve
zeta_u = zu + lam ** 2 / zu
zeta_l = zl + lam ** 2 / zl

print(type(zeta_l.real))
plt.figure(figsize=(10, 2))
plt.plot(zeta_u.real, zeta_u.imag)
plt.plot(zeta_l.real, zeta_l.imag)
plt.show()