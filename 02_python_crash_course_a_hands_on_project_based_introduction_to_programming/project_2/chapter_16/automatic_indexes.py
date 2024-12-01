import csv
from datetime import datetime
from matplotlib import pyplot as plt


def extract_data(csv_filename):
    with open(csv_filename, 'r') as f:
        reader = csv.reader(f)
        header_row = next(reader)
        date_index, tmax_index, tmin_index = 0, 0, 0
        for index, column in enumerate(header_row):
            if column == 'DATE':
                date_index = index
            elif column == 'TMAX':
                tmax_index = index
            elif column == 'TMIN':
                tmin_index = index

        dates, highs, lows = [], [], []
        for row in reader:
            date = datetime.strptime(row[date_index], '%Y-%m-%d')
            try:
                high = int(row[tmax_index])
                low = int(row[tmin_index])
            except ValueError:
                print(f'Missing data on {date}')
            else:
                dates.append(date)
                highs.append(high)
                lows.append(low)
        return dates, highs, lows


def generate_graph(csv_filename):
    dates, highs, lows = extract_data(csv_filename)
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(12, 8))

    ax.plot(dates, highs, label='MaxTemp', color='red')
    ax.plot(dates, lows, label='MinTemp', color='blue')
    ax.legend()

    plt.title('Daily Temperature 2018', fontweight='bold')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Temperature', fontweight='bold')
    plt.fill_between(dates, highs, lows, alpha=0.2, color='yellow')
    plt.show()


generate_graph('data/sitka_weather_2018_simple.csv')
