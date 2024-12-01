import csv
from datetime import datetime
import matplotlib.pyplot as plt

filename = 'data/sitka_weather_2018_simple.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    # for index, column in enumerate(header_row):
    #     print(index, column)
    # HEADER ROW
    # 0 STATION
    # 1 NAME
    # 2 DATE - Date
    # 3 PRCP
    # 4 TAVG
    # 5 TMAX - Temperature Max
    # 6 TMIN - Temperature Min

    # Get DATE, TMAX, TMIN
    dates, highs, lows = [], [], []
    for row in reader:
        date = datetime.strptime(row[2], '%Y-%m-%d')
        dates.append(date)

        high = int(row[5])
        highs.append(high)

        low = int(row[6])
        lows.append(low)

# Plotting Data
plt.style.use('ggplot')
fig, ax = plt.subplots()

ax.plot(dates, highs, label='high', color='red')
ax.plot(dates, lows, label='low', color='blue')

# Format Plot
plt.title('Daily high and low temperatures 2018', fontweight='bold')
plt.xlabel('Date', fontweight='bold')
plt.ylabel('Temperature (F)', fontweight='bold')
plt.fill_between(dates, highs, lows, alpha=0.2, facecolor='blue', interpolate=True)

plt.savefig('sitka_highs_lows_2018.png')
plt.show()
