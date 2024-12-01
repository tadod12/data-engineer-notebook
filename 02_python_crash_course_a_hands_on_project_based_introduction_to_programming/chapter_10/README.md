# Chapter 10 Code Note
## Files
### Functions
1. open()
    ```
   # return an object representing the file
   file_object = open('name of the file')
   ```
   > Mode:
   > `'w'` - Write mode
   > `'r'` - Read mode
   > `'a'` - Append mode
   
2. read()
   ```
   contents = file_object.read()  # read the entire contents of the file and stores it as one long string in contents
   print(contents.rstrip())  # clear blank line
   ```
   > The only difference between this output and the original file is the extra blank line at the end of the output. The blank line appears because read() returns an empty string when it reaches the end of the file; this empty string shows up as a blank line.

3. readlines()
   ```
   lines = file_object.readlines()  # return a list (of lines)
   ```
   
4. write() - Write a string to a file
   ```
   with open(filename, 'w') as file_project:
      file_object.write('I love programming.')
   ```

### Syntax
1. Reading an Entire File
    ```
   with open('pi_digits.txt') as file_object:
      contents = file_object.read()
   print(contents)
   ```
   
2. Reading Line by Line
   ```
   with open(filename) as file_object:
      for line in file_project:
         print(line.rstrip())
   ```
   
3. Making a List of Lines from a File
   ```
   with open(filename) as file_object:
      lines = file_object.readlines()
   
   for line in lines:
      print(line.rstrip())
   ```
   
4. Writing to an Empty File
   ```
   filename = 'programming.txt'
   
   with open(filename, 'w') as file_project:
      file_object.write('I love programming.')
   ```
   
## Exceptions
### Syntax
1. Try-except block
   ```
   --snip--
   try:
      answer = int(first_number) / int(second_number)  # includes only the code that might cause an error
   except ZeroDivisionError:
      print('You can\'t divide by zero')  # not success
   else:
      print(answer)  # try successfully
   ```
   
   ```
   filename = 'alice.txt'
   
   try:
      with open(filename, encoding='utf-8') as f:
         contents = f.read()
   except FileNotFoundError:
      print(f'Sorry, the file {filename} does not exist')
   else:
      # words count
      words = contents.split()  # type: List (store words)
      num_words = len(words)
      print(f'The file {filename} has about {num_words} words')
   ```
   
2. Failing Silently
   ```
   try:
      --snip--
   except FileNotFoundError:
      pass
   else:
      --snip--
   ```
   
## JSON
### Functions
1. json.dump(data, file object)
   ```
   import json
   
   numbers = [2, 3, 5, 7, 11, 13]
   filename = 'numbers.json'
   
   with open(filename, 'w') as f:
      json.dump(numbers, f)  # 2 arguments: data and file object
   ```
   
2. json.load(file object)
   ```
   import json
   
   filename = 'numbers.json'
   with open(filename, 'r') as f:
      numbers = json.load(f)
   ```