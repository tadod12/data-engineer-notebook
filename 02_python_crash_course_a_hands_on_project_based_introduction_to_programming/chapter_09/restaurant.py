class Restaurant:
    def __init__(self, restaurant_name, cuisine_type):
        self.restaurant_name = restaurant_name
        self.cuisine_type = cuisine_type

    def describe_restaurant(self):
        print(f'\nThe restaurant name is {self.restaurant_name}')
        print(f'The cuisine type is {self.cuisine_type}')

    def open_restaurant(self):
        print(f'{self.restaurant_name} has been opened')


# my_restaurant = Restaurant('tadod', 'Vietnamese')
# print(my_restaurant.restaurant_name)
# print(my_restaurant.cuisine_type)
# my_restaurant.describe_restaurant()
# my_restaurant.open_restaurant()
