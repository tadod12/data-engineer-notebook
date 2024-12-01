from random import choice

letters = ('a', 1, 2, 'j', 'd', 'k', 3, 5, 8, 0)
lot = ''

for i in range(4):
    letter = choice(letters)
    if str(letter) not in lot:  # str() for convert
        lot += str(letter)

print(f'Ticket matching {lot} wins a prize')
