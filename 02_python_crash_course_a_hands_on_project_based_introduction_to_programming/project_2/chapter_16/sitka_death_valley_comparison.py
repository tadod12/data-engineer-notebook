import csv
from datetime import datetime
from matplotlib import pyplot as plt

# Sitka 2018
filename_1 = 'data/sitka_weather_2018_simple.csv'
with open(filename_1, 'r') as f:
    reader = csv.reader(f)
    header_row = next(reader)  # ['STATION', 'NAME', 'DATE', 'PRCP', 'TAVG', 'TMAX', 'TMIN']
    # print(header_row)
    sitka_dates, sitka_highs, sitka_lows = [], [], []
    for row in reader:
        sitka_dates.append(datetime.strptime(row[2], '%Y-%m-%d'))
        sitka_highs.append(int(row[5]))
        sitka_lows.append(int(row[6]))

# Death Valley 2018
filename_2 = 'data/death_valley_2018_simple.csv'
with open(filename_2, 'r') as f:
    reader = csv.reader(f)
    header_row = next(reader)  # ['STATION', 'NAME', 'DATE', 'PRCP', 'TMAX', 'TMIN', 'TOBS']
    # print(header_row)
    death_dates, death_highs, death_lows = [], [], []
    for row in reader:
        death_date = datetime.strptime(row[2], '%Y-%m-%d')
        try:
            high = int(row[4])
            low = int(row[5])
        except ValueError:
            print(f'Missing data on {death_date}')
        else:
            death_dates.append(death_date)
            death_highs.append(high)
            death_lows.append(low)

# Plotting
plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(12, 8))

ax.plot(sitka_dates, sitka_highs, label='sitka_high', color='red', linewidth=1)
ax.plot(sitka_dates, sitka_lows, label='sitka_low', color='blue', linewidth=1)
ax.plot(death_dates, death_highs, label='death_valley_high', color='green', linewidth=1)
ax.plot(death_dates, death_lows, label='death_valley_low', color='yellow', linewidth=1)

plt.fill_between(sitka_dates, sitka_highs, sitka_lows, alpha=0.2, color='blue')
plt.fill_between(death_dates, death_highs, death_lows, alpha=0.2, color='green')

plt.title('Daily Temperature Comparison 2018', fontweight='bold')
plt.xlabel('Date', fontweight='bold')
plt.ylabel('Temperature (F)', fontweight='bold')

ax.legend()  # Show line information
plt.savefig('sitka_death_valley_comparison.png')
plt.show()
