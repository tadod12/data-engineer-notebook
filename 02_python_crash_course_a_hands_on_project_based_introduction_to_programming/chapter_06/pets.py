pet_0 = {
    'type': 'golden',
    'owner': 'dodat'
}

pet_1 = {
    'type': 'collie',
    'owner': 'gb'
}

pet_2 = {
    'type': 'pug',
    'owner': 'vanh'
}

pets = [pet_0, pet_1, pet_2]
for pet in pets:
    for key, value in pet.items():
        print(f'{key}: {value}')
    print('\n')
