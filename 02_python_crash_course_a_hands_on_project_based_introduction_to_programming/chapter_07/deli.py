sandwich_orders = ['ham', 'blt', 'bacon', 'meatball']
finished_sandwich = []

while sandwich_orders:
    sandwich = sandwich_orders.pop()
    print(f'I made your {sandwich} sandwich')
    finished_sandwich.append(sandwich)

print('Sandwich lists:')
for sandwich in finished_sandwich:
    print(sandwich)
