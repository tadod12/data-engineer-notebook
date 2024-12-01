class Restaurant:
    def __init__(self, restaurant_name, cuisine_type):
        self.restaurant_name = restaurant_name
        self.cuisine_type = cuisine_type
        self.number_served = 0

    def describe_restaurant(self):
        print(f'\nThe restaurant name is {self.restaurant_name}')
        print(f'The cuisine type is {self.cuisine_type}')

    def open_restaurant(self):
        print(f'{self.restaurant_name} has been opened')

    def set_number_served(self, number_served):
        self.number_served = number_served

    def increment_number_served(self, number):
        if number < 0:
            print('Invalid number!')
        else:
            self.number_served += number


restaurant = Restaurant('tadod', 'Ford')

restaurant.number_served = 10
print(f'\nRestaurant\'s number served: {restaurant.number_served}')

restaurant.set_number_served(20)
print(f'\nRestaurant\'s number served: {restaurant.number_served}')

restaurant.increment_number_served(2)
print(f'\nRestaurant\'s number served: {restaurant.number_served}')
