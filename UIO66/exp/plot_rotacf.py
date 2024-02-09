import matplotlib.pyplot as plt

x = [0, 1, 2, 3]
y_removed = [0.21, 0.82, 1.44, 1.90]
y_removed_cl = [0.21, 1.05, 1.65, 2.36]
y_replaced = [0.21, 10.0, 30.0, 40.0]

plt.plot(x, y_removed, color='black')
plt.plot(x, y_removed_cl, color='red')
plt.plot(x, y_replaced, color='blue')
plt.scatter(x, y_removed, color='black')
plt.scatter(x, y_removed_cl, color='red')
plt.scatter(x, y_replaced, color='blue')

plt.grid(color='black', linestyle='--', linewidth=0.25)
plt.xticks([0, 1, 2, 3], ['0', '1', '2', '3'])
plt.xlabel('Removed linkers count')
plt.ylabel('$T_{cor}, ns$')
plt.yscale('log')
plt.savefig('/home/sc_enigma/Projects/MD_UIO66/analysis/rotacf/rotacf.png', dpi=500)