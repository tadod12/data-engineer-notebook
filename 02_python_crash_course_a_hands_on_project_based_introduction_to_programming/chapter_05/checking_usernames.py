current_users = ['joHn', 'josh', 'Tim', 'David', 'chris']
new_users = ['josh', 'dodat', 'tom', 'DaViD', 'bale']

current_users_normalize = []
for user in current_users:
    current_users_normalize.append(user.lower())

for new_user in new_users:
    if new_user.lower() in current_users_normalize:
        print(f'{new_user} is already taken, enter a different username!')
    else:
        print(f'{new_user} is available')
