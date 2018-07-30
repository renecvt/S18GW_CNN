from numpy import genfromtxt
data = genfromtxt('/Users/karenggv/Desktop/Projects/Delfin/S18GW_CNN/run_summary_log_pruebas-tag-auc_1.csv', delimiter=',', names=True)


import pylab as plt
plt.plot(data)
plt.show()