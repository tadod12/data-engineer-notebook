# Chapter 08 Code Note
## Functions
### Syntax
1. Define
    ```
   def greet_user(username):
      """docstring - display what the function does"""
      print(f'Hello {username}')
   
   greet_user('dodat')
   ```
   
   > **Positional Arguments** - Need to be in the same order the parameters were written
   > **Keyword Arguments** - name-value pair passed to a function

2. Passing List
   Any changes made to the list inside the function's body are permanent
   Prevent a function from modifying a list
   ```
   function_name(list_name[:])  # Send a copy of a list to a function
   #  you should pass the original list to functions unless you have a specific reason to pass a copy
   ```
   
3. Passing an Arbitrary Number of Arguments
   ```
   def make_pizza(*toppings):
      print(toppings)
   
   make_pizza('pepperoni')
   make_pizza('mushrooms', 'green peppers', 'extra cheese')
   ```
   > `*toppings` - makes an empty tuple called toppings and pack whatever values it receives into this tuple 

4. Mixing
   ```
   def make_pizza(size, *toppings): 
      """Summarize the pizza we are about to make."""
      print(f"\nMaking a {size}-inch pizza with the following toppings:") 
      for topping in toppings: 
         print(f"- {topping}") 

   make_pizza(16, 'pepperoni') 
   make_pizza(12, 'mushrooms', 'green peppers', 'extra cheese')
   ```
   
5. Arbitrary Keyword Argument
   ```
   def build_profile(first, last, **user_info):
      """Build a dictionary containing everything we know about a user."""
      user_info['first_name'] = first
      user_info['last_name'] = last
   return user_info
 
   user_profile = build_profile('albert', 'einstein',
                             location='princeton',
                             field='physics')
   print(user_profile)
   ```
   > `**user_info` - makes an empty dictionary called user_info and pack whatever name-value pairs it receives into this dictionary

6. Module
   ```
   # Import an Entire Module
   import module_name
   module_name.function_name()  # call function
   
   # Import Specific Functions
   from module_name import function_0, function_1
   from module_name import *  # all functions
   
   # Using alias
   import module_name as m
   from module_name import function_0 as f0
   ```