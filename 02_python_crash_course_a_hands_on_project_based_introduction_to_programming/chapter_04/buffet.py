foods = ('rice', 'beef', 'coca', 'chicken', 'soda')
print('OLD:')
for food in foods:
    print(food)

# Tuples don't support item assignment
# foods[2] = 'pepsi'

foods = ('rice', 'beef', 'pepsi', 'chicken', 'water')
print('NEW:')
for food in foods:
    print(food)
