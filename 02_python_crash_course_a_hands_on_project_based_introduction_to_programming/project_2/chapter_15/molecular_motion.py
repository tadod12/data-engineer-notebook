import matplotlib.pyplot as plt

from random_walk import RandomWalk

rw = RandomWalk()
rw.fill_walk()

plt.style.use('ggplot')
fig, ax = plt.subplots()
plt.plot(rw.x_values, rw.y_values, color='blue', linewidth=1)

ax.set_title('Molecular Motion')

plt.savefig('molecular_motion.png')
plt.show()
