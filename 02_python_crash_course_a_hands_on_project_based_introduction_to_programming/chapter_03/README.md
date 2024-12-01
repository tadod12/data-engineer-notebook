# Chapter 03 Code Note
## Functions
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

6. sort() - Permanently
   ```
   cars = ['bmw', 'audi', 'toyota', 'subaru']
   cars.sort()  # or cars.sort(reverse=True)
   print(cars)
   ```

7. sorted() - Temporary
   ```
   print(sorted(cars))
   ```

8. reverse()
   ```
   cars.reverse()
   print(cars)
   ```

9. len()
   ```
   print(len(cars))
   ```

## Syntax
