filename = 'guest_book.txt'

with open(filename, 'a') as file_object:
    while True:
        name = input('Enter your name: ')
        print(f'Hello {name}, welcome to tadod!')
        file_object.write(f'{name}\n')
        flag = input('Would you like to add another name? (y/n): ')
        if flag.lower() == 'n':
            break
