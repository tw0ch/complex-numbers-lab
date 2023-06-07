import numpy as np
import matplotlib.pyplot as plt

theta = np.arange(0, np.pi, 0.1)
z = 1.5 * np.exp(1j*theta)

fig, axs = plt.subplots(1, 2, sharex=True, sharey=True)
axs[0].plot(np.real(z), np.imag(z))
axs[0].set_aspect(1)
xi = z + 1.0 / z

axs[1].plot(np.real(xi), np.imag(xi))
axs[1].set_aspect(1)
plt.show()