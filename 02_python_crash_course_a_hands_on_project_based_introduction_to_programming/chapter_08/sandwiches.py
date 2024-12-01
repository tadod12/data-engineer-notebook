def sandwich(*ingredients):
    print('lists: ')
    for ingredient in ingredients:
        print(f'- {ingredient}')


sandwich('cheese', 'cheese', 'cheese')
sandwich('cheese')
sandwich()
