flag = True

while flag:
    age = int(input("Enter your age: "))
    if age < 0:
        flag = False
        print('Wrong age!!!')
        # break
    elif age < 3:
        print('The ticket is free')
    elif age <= 12:
        print('The ticket is $10')
    else:
        print('The ticket is $15')
