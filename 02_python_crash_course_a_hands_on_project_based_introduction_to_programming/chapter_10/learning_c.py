with open('learning_python.txt') as file_object:
    contents = file_object.readlines()

for line in contents:
    line = line.replace('Python', 'C')  # return modified line
    print(line.strip())
