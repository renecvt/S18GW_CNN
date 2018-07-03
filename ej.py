import pylab as plt

MINIMUM_MASS = 10
MAXIMUM_MASS = 50
STEP = 5

m = []

for x in range(MINIMUM_MASS, MAXIMUM_MASS + 1, STEP):
    for y in range(x, MINIMUM_MASS - 1, -STEP):
        m.append((x,y))

# plt.scatter(*zip(*m))
# plt.title('Masses')
# plt.xlabel('M1')
# plt.ylabel('M2')
# plt.show()

# MASA TOTAL
m1, m2 = zip(*m)
m_total = [sum(x) for x in zip(m1, m2)]

import numpy as np
duration = np.array([0.5, 1, 0.8, 2, 0.5, 1])
duration.resize(len(m_total))

# plt.scatter(m_total, duration)
# plt.xlabel('M-Total')
# plt.ylabel('Duration')
# plt.show()


