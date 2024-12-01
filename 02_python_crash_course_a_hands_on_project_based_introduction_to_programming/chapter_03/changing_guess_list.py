guesses = ['vanh', 'lby', 'gb']

busy_guess = 'lby'
guesses.remove(busy_guess)
print(f'{busy_guess} can not make the dinner')

new_guess = 'ichbingt'
guesses.append(new_guess)
print(f'Final guess list: {guesses[0]}, {guesses[1]}, {guesses[2]}')
