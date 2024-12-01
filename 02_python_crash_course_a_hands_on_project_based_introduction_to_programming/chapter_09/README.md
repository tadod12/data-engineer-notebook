# Chapter 09 Code Note
## Classes
### Functions
### Syntax
1. Define class from scratch
    ```
   class Dog:
      """A simple attempt to model a dog"""
      def __init__(self, name, age):
         """Initialize name and age attributes"""
         self.name = name
         self.age = age
   
      def sit(self):
         """Simulate a dog sitting in response to a command"""
         print(f'{self.name} is now sitting')
   
   my_dog = Dog('Willie', 6)
   print(f'My dog's name is {my_dog.name}')  # access attributes
   my_dog.sit()  # calling methods
   ```
   > The `self` parameter is required in the method definition, must come first before the other parameters

2. Inheritance
   ```
   class Golden(Dog):
      """Represent aspects of a dog, specific to golden retriever"""
   
      def __init__(self, name, age):
         """Initialize attributes of the parent class"""
         super().__init__(name, age)
   ```
   > `super()` allows you to call the `__init__` method from the parent class

3. Instances as Attributes
   ```
   class Battery:
      def __init__(self, battery_size=75):
         self.battery_size = battery_size
      def describe_battery(self):
         print(f'This car has a {self.battery_size}-kWh battery.')
   
   class ElectricCar(Car):
      def __init__(self, make, model, year):
         super().__init__(make, model, year)
         self.battery = Battery()  # Instance as Attribute
   
   my_tesla = ElectricCar('tesla', 'model_s', 2019)
   my_tesla.battery.Battery()
   ```

4. Import Classes
   ```
   from car import Car  # from module car (car.py) import class Car()
   my_new_car = Car('audi', 'a4', 2019)
   
   import car  # import entire module
   my_bettle = car.Car('volkswagen', 'beetle', 2019)
   
   # Using Aliaes
   from electric_car import ElectricCar as EC
   ```
   
5. The Python Standard Library
   ```
   from random import randint
   print(randint(1, 6))  # random from 1 to 6
   
   from random import choice
   players = ['charles', 'martina', 'michael', 'florence', 'eli']
   first_up = choice(players)  # random in list, tuple...
   ```