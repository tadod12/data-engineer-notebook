pizzas = ['pepperoni', 'funghi', 'calabrian', 'margherita', 'marinara']

print('1. The first three items in the list are: ')
for pizza in pizzas[:3]:
    print(pizza)

print('2. Three items from the middle of the list are:')
for pizza in pizzas[1:4]:
    print(pizza)

print('3. The last three items in the list are:')
for pizza in pizzas[-3:]:
    print(pizza)
