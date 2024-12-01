from random import choice

letters = ('a', 1, 2, 'j', 'd', 'k', 3, 5, 8, 0)
lot = ''

for i in range(4):
    letter = choice(letters)
    while str(letter) in lot:  # str() for convert
        letter = choice(letters)
    lot += str(letter)

print(f'Ticket matching {lot} wins a prize')

ticket = ''
counter = 0
while ticket != lot:
    counter += 1
    ticket = ''
    for i in range(4):
        letter = choice(letters)
        while str(letter) in ticket:  # str() for convert
            letter = choice(letters)
        ticket += str(letter)

print(f'Total number of tickets: {counter}')
