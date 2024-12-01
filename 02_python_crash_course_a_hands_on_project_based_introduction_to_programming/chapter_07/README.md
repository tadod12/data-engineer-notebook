# Chapter 07 Code Note
## Input
### Functions
1. input()
    ```
   message = input("Tell me something, and I will repeat it back to you: ")
   print(message)
   
   prompt = "If you tell us who you are, we can personalize the messages you see."
   prompt += "\nWhat is your first name? "
   name = input(prompt)
   ```
   
   > message's type is string

## While Loop
### Syntax
   ```
   current_number = 1
   while current_number <= 5:
      print(current_number)
      current_number += 1
   
   # list
   unconfirmed_users = ['alice', 'brian', 'candace']
   while unconfirmed_users:
      ...
     
   pets = ['dog', 'cat', 'dog', 'goldfish', 'cat', 'rabbit', 'cat']
   while 'cat' in pets:
      pets.remove('cat')
   ```
