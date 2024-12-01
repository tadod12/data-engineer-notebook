favorite_numbers = {
    'dodat': [12, 20],
    'jack': [1, 10],
    'john': [20],
    'nick': [3, 100, 5]
}

for key, value in favorite_numbers.items():
    print(f'{key.title()}\'s favorite number is:')
    for num in value:
        print(num)
