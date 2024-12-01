while True:
    first_number = input("Enter first number: ")
    second_number = input("Enter second number: ")
    try:
        first_number = int(first_number)
        second_number = int(second_number)
    except ValueError:
        pass
    else:
        print(f'Result: {first_number + second_number}')
