# entire file
with open('learning_python.txt') as file_object:
    contents = file_object.read()
    print(contents.rstrip())

# looping over file object
with open('learning_python.txt') as file_object:
    for line in file_object:
        print(line.rstrip())

# storing lines in a list
with open('learning_python.txt') as file_object:
    contents = file_object.readlines()  # contents type: List

for line in contents:
    print(line.strip())
