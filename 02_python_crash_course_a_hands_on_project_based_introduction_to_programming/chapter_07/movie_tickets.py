age = int(input("Enter your age: "))

while age > 0:
    if age < 3:
        print('The ticket is free')
    elif age <= 12:
        print('The ticket is $10')
    else:
        print('The ticket is $15')
    age = int(input("Enter your age: "))
print('Wrong age!!!')
