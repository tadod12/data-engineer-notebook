import json

filename = 'favorite_number.json'
try:
    with open(filename, 'r') as f:
        favorite_number = json.load(f)
except FileNotFoundError:
    number = input('Enter your favorite number: ')
    with open(filename, 'w') as f:
        json.dump(number, f)
else:
    print(f'I know your favorite number is {favorite_number}')
# This also is Favorite Number Remembered exercise
