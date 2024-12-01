prompt = 'if you could visit one place in the world, where would you go? '
dream_vacation = {}

while True:
    name = input('input your name: ')
    dream_vacation[name] = input(prompt)
    more = input('Another? ')
    if more == 'no':
        break

print('lists:')
for key, value in dream_vacation.items():
    print(f'{key}:\t{value}')
