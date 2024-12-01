filename = 'a_book_of_bridges.txt'

try:
    with open(filename, 'r') as f:
        content = f.readlines()
except FileNotFoundError:
    print('File not found')
else:
    counter = 0
    for line in content:
        counter += line.lower().count('the ')

    print(f'Number of the word "the": {counter}')
