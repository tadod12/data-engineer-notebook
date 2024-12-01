person_0 = {
    'first_name': 'John',
    'last_name': 'Doe',
    'age': 25,
    'city': 'New York'
}

person_1 = {
    'first_name': 'John',
    'last_name': 'Week',
    'age': 21,
    'city': 'Ha Noi'
}

person_2 = {
    'first_name': 'Justin',
    'last_name': 'Sagan',
    'age': 27,
    'city': 'San Francisco'
}

people = [person_0, person_1, person_2]

for person in people:
    for k, v in person.items():
        print(f'{k}: {v}')
    print('\n')
