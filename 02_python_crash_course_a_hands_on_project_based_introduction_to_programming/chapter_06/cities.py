cities = {
    'ha noi': {
        'country': 'viet nam',
        'population': 50000,
        'fact': 'capital'
    },
    'new york': {
        'country': 'us',
        'population': 50000,
        'fact': 'none'
    }
}

for city, info in cities.items():
    print(f'{city.title()}')
    for key, value in info.items():
        if str == type(value):
            print(f'\t{key}: {value.title()}')
        else:
            print(f'\t{key}: {value}')
    print('\n')
