car = 'Subaru'
if car.lower() == 'subaru':
    print('car: subaru')

year_create = 2020
if year_create < 2010:
    print('model: old')
if year_create >= 2010:
    print('model: new')

items = ['hoods', 'mirrors', 'doors', 'fenders', 'bumpers']
if 'radiators' in items:
    print('missing: none')
if 'radiators' not in items:
    print('missing: radiators')
