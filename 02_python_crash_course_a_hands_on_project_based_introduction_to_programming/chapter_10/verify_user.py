import json


def get_stored_username():
    filename = 'username.json'
    try:
        with open(filename, 'r') as f:
            username = json.load(f)
    except FileNotFoundError:
        return None
    else:
        return username


def get_new_username():
    username = input("Enter your username: ")
    filename = 'username.json'
    with open(filename, 'w') as f:
        json.dump(username, f)
    return username


def greet_user():
    username = get_stored_username()
    if username:
        flag = input(f'Are you {username}? (y/n) ')
        if flag == 'y':
            print(f'Welcome back, {username}!')
        else:
            username = get_new_username()
            print(f'We\'ll remember you when you come back, {username}!')
    else:
        username = get_new_username()
        print(f'We\'ll remember you when you come back, {username}!')


greet_user()
