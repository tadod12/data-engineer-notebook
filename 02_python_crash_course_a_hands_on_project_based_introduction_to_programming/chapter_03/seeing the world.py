places = ['canada', 'france', 'vietnam', 'japan', 'england']

print(f'Origin: {places}')

print(f'Temporary sorted: {sorted(places)}')

print(f'Origin: {places}')

print(f'Temporary reverse sorted: {sorted(places, reverse=True)}')

print(f'Origin: {places}')

places.reverse()
print(f'Permanent reverse: {places}')

places.reverse()
print(f'Origin: {places}')

places.sort()
print(f'Permanent sorted: {places}')

places.sort(reverse=True)
print(f'Permanent reverse sorted: {places}')
