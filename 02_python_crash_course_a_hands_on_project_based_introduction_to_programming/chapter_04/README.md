# Chapter 04 Code Note
## List
### Functions
1. range()
   ```
   for value in range(1, 5):  # print from 1 to 4
       print(value)
   # range(6) - from 0 to 5
   # range(1, 8, 2) - distance each = 2
   ```

2. list()
   ```
   numbers = list(range(1, 6))  # [1, 2, 3, 4, 5]
   ```

3. function for list of numbers
   ```
   digits = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
   min(digits)  # 0
   max(digits)  # 9
   sum(digits)  # 45
   ```
   
4. remove(string)
   ```
   pets = ['dog', 'cat', 'dog', 'goldfish', 'cat', 'rabbit', 'cat']
   pets.remove('cat')  # remove first 'cat' found in pets
   ```

### Syntax
1. List comprehensions
   ```
   squares = [value**2 for value in range(1, 11)]
   ```
   
2. List slicing
   ```
   players[0:3]     # from 0 to 2
   players[:4]      # from begin to 3
   players[2:]      # from 2 to end
   players[-3:]     # last 3 players
   players[1:10:2]  # 1 to 9, distance=3 (1, 3, 5, 7, 9)
   ```
   
3. Looping through slices
   ```
   for player in players[:3]:
       print(player.title())
   ```
   
4. Copying a list
   ```
   my_foods = ['pizza', 'falafel', 'carrot cake']
   friend_foods = my_foods[:]
   ```
   
## Tuples - An immutable list
### Functions

### Syntax
1. Define
   ```
   dimensions = (200, 50)
   print(dimensions[0])
   
   # Tuple with one element
   my_t = (3,)  # Must have ','
   ```

2. Writing over a tuple
   ```
   dimensions = (200, 50)
   print(f'Origin: {dimensions}')
   
   dimensions = (400, 100)
   print(f'Modified: {dimensions}')
   ```