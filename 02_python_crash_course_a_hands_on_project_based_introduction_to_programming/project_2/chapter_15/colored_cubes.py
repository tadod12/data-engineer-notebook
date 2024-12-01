from matplotlib import pyplot as plt

plt.style.use('ggplot')

x_values = [x for x in range(1, 5001)]
y_values = [x ** 3 for x in x_values]

fig, ax = plt.subplots()

# Set chart title and label axes
ax.set_title('First 5 Cube Numbers', fontsize=15)
ax.set_xlabel('value', fontsize=14)
ax.set_ylabel('cube of value', fontsize=14)

# ax.plot(x_values, y_values, 'o-', color='yellow')
ax.scatter(x_values, y_values, c=y_values, cmap=plt.cm.Blues, s=10)
plt.savefig('colored_cube5000.png', bbox_inches='tight')
plt.show()
