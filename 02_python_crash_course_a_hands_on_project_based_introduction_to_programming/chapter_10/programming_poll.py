filename = 'programming_poll.txt'

with open(filename, 'a') as file_object:
    while True:
        reason = input('Enter a reason why u like programming: ')
        file_object.write(reason + '\n')
        if input('Continue? [y/n]: ') == 'n':
            break
