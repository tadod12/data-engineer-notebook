while True:
    first_number = input("Enter first number: ")
    try:
        first_number = int(first_number)
    except ValueError:
        print("Please enter an integer")
    else:
        break

while True:
    second_number = input("Enter second number: ")
    try:
        second_number = int(second_number)
    except ValueError:
        print("Please enter an integer")
    else:
        break

print(f'Result: {first_number + second_number}')
