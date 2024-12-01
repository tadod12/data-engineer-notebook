favorite_places = {
    'dodat': ['birmingham', 'paris'],
    'john': ['new york'],
    'riot': ['las vegas', 'new york']
}

favorite_places['nick'] = ['san francisco', 'new york']

for key, value in favorite_places.items():
    print(f'{key.title()} wants to go to:')
    for place in value:
        print(f'{place.title()}')
    print('\n')
