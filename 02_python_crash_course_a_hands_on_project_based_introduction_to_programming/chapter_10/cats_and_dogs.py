filenames = ['cats.txt', 'dogs.txt']

for filename in filenames:
    try:
        with open(filename, 'r') as f:
            contents = f.readlines()
    except FileNotFoundError:
        print(f'{filename} not found')
    else:
        for line in contents:
            print(line.strip())
