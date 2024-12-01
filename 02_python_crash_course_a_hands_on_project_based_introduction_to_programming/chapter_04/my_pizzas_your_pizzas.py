pizzas = ['pepperoni', 'funghi', 'calabrian', 'margherita', 'marinara']

friend_pizzas = pizzas[:]

pizzas.append('bacon')
friend_pizzas.append('salami')

print('My favorite pizzas are:')
for pizza in pizzas:
    print(pizza)

print('\nMy friend\'s favorite pizzas are:')
for friend_pizza in friend_pizzas:
    print(friend_pizza)
