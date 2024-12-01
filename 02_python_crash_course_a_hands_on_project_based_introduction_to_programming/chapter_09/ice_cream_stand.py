from restaurant import Restaurant


class IceCreamStand(Restaurant):
    """Inherits from Restaurant in restaurant.py"""
    def __init__(self, restaurant_name, cuisine_type, *flavors):
        super().__init__(restaurant_name, cuisine_type)
        self.flavors = flavors

    def display_flavors(self):
        print('Flavors list: ')
        for flavor in self.flavors:
            print(f'- {flavor}')


ice = IceCreamStand('dodat', 'vietnamese', 'spicy', 'salty', 'sweet', 'bitter')
ice.display_flavors()
