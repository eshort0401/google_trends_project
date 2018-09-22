import logging
logging.basicConfig(level=logging.DEBUG)

import matplotlib.pyplot as plt
import numpy as np

plt.close("all")

plt.rc('text', usetex=True)

#plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
plt.rc('text', usetex=True)

x=np.arange(1,10)

plt.plot(x,x)

plt.xlabel("$\int_0^1 \sin(\\alpha)$")
plt.show()