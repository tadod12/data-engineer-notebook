import csv
from datetime import datetime
from matplotlib import pyplot as plt

filename = 'data/sitka_weather_2018_simple.csv'
with open(filename) as f:
    reader = csv.reader(f)  # create reader object for csv file
    header_row = next(reader)
    print(header_row)

    dates, rainfalls = [], []
    for row in reader:
        dates.append(datetime.strptime(row[2], '%Y-%m-%d'))
        rainfalls.append(row[3])

plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(12, 10))
ax.plot(dates, rainfalls, color='blue', label='Rainfall')

# Format Plot
plt.title('Rainfall 2018', fontweight='bold')
plt.xlabel('Date', fontweight='bold')
plt.ylabel('Amount', fontweight='bold')
ax.get_yaxis().set_visible(False)

plt.show()
