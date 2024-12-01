from plotly.graph_objs import Bar, Layout
from plotly.offline import offline

from die import Die

die_1 = Die()
die_2 = Die()
die_3 = Die()

# Roll
results = []
for i in range(1000):
    results.append(die_1.roll() + die_2.roll() + die_3.roll())

# Analyze
frequencies = []
for value in range(3, 19):
    frequency = results.count(value)
    frequencies.append(frequency)

# Visualization
x_values = list(range(3, 19))
data = [Bar(x=x_values, y=frequencies)]

x_axis_config = {'title': 'Result', 'dtick': 1}
y_axis_config = {'title': 'Frequency of Result'}

my_layout = Layout(title='Rolling 3 dices 1000 times',
                   xaxis=x_axis_config, yaxis=y_axis_config)

offline.plot({'data': data, 'layout': my_layout}, filename="three_dice.html")
