# Chapter 02 Code Note
## Functions
### String
1. title()
    ```
    name = "ada lovelace"
    print(name.title())
    ```

2. upper()
    ```
    name = "Ada Lovelace"
    print(name.upper())
    ```

3. lower()
    ```
    name = "Ada Lovelace"
    print(name.lower())
    ```
4. format()
    ```
    message = f"Hello, {full_name.title()}!"
    message = "Hello, {}!".format(full_name.title())
    ```
5. strip()
    ```
    favorite_language = ' python '
    print(favorite_language.lstrip())
    print(favorite_language.rstrip())
    print(favorite_language.strip())    
    ```
### List
1. append()
    ```
    motorcycles.append('ducati')  # add to the end of the list
    ```
2. insert()
    ```
    motorcycles.insert(0, 'ducati')
    ```
3. del
    ```
    del motorcycles[1]
    ```
4. pop()
    ```
    popped_motorcycle = motorcycles.pop()  # remove and return the last element
    another_popped = motorcycles.pop(2)  # can use index
    ```
5. remove()
    ```
    motorcycles.remove('ducati')  # remove by value, only the first occurrence 
    ```

## Syntax
1. Underscored in number
   ```
   universe_age = 14_000_000_000  # 14000000000
   ```
2. Multiple assignment
   ```
   x, y, z = 0, 0, 0
   ```

> int / int = float
> int ** int = int