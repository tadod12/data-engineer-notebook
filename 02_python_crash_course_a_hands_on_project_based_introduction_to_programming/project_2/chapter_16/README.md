# Data Visualization
## Downloading Data
### CSV File Format
1. Read CSV File
    ```
   import csv
   
   filename = 'data/sitka_weather_07-2018_simple.csv'
   with open(filename) as f:
      reader = csv.reader(f)
      header_row = next(reader)
   
      for index, column_header in enumerate(header_row):
         print(index, column_header)
      print(header_row)
   ```
   > `csv.reader(f)` create a reader object associated with file `f`
   > `next()` function return next line, first call - first line of the file (header row)
   > `enumerate()` function returns both the index of each item and the value of each item as you loop through a list
   
2. datetime.strptime()
    ```
   from datetime import datetime
   
   first_date = datetime.strptime('2018-07-01', '%Y-%m-%d')
   ```
   
    | Argument | Meaning                                  |
    |----------|------------------------------------------|
| \| %A       | Weekday name, such as Monday             |
| \| %B       | Month name, such as January              |
| \| %m       | Month, as a number (01 to 12)            |
| \| %d       | Day of the month, as a number (01 to 31) |
| \| %Y       | Four-digit year, such as 2019            |
| \| %y       | Two-digit year, such as 19               |
| \| %H       | Hour, in 24-hour format (00 to 23)       |
| \| %I       | Hour, in 12-hour format (01 to 12)       |
| \| %p       | am or pm                                 |
| \| %M       | Minutes (00 to 59)                       |
| \| %S       | Seconds (00 to 61)                       |

### JSON Format

   ```
   import json
   
   filename = 'data/eq_data_30_day_m1.json'
   with open(filename) as f:
      all_eq_data = json.load(f)
      
   # Save to readable file
   readable_file = 'data/readable_eq_data.json'
   with open(readable_file, 'w') as f:
      json.dump(all_eq_data, f, indent=4)
      
   all_eq_dicts = add_eq_data['features']
   
   # Extracting Magnitudes
   mags, lons, lats = [], [], []
   for eq_dict in all_eq_dicts:
      mag = eq_dict['properties']['mag']
      lon = eq_dict['geometry']['coordinates'][0]  # longitude
      lat = eq_dict['geometry']['coordinates'][1]  # latitude
            
      mags.append(mag)
      lons.append(lon)
      lats.append(lat)
   ```
