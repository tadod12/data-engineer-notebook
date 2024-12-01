sandwich_orders = ['pastrami', 'ham', 'blt', 'pastrami', 'bacon', 'meatball', 'pastrami']

print('the deli has run out of pastrami')
while 'pastrami' in sandwich_orders:
    sandwich_orders.remove('pastrami')

finished_sandwiches = []
for sandwich in sandwich_orders:
    finished_sandwiches.append(sandwich)

print(finished_sandwiches)
