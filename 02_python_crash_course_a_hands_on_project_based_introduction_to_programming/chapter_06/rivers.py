rivers = {
    'Nile': 'Egypt',
    'Amazon': 'Brazil',
    'Yangtze': 'China'
}

for key, value in rivers.items():
    print(f'The {key.title()} runs through {value.title()}')

print('\nName list:')
for river in rivers.keys():
    print(f'{river}')

print('\nCountry list:')
for country in rivers.values():
    print(f'{country}')
