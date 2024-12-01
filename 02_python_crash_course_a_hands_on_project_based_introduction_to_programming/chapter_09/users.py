class User:
    def __init__(self, first_name, last_name, **info):
        """Save user's info, more information stored in 'info' dictionary"""
        self.first_name = first_name
        self.last_name = last_name
        self.info = info

    def describe_user(self):
        print(f'\nName: {self.first_name} {self.last_name}')
        for key, value in self.info.items():
            print(f'{key}: {value}')

    def greet_user(self):
        print(f'\nHello {self.first_name} {self.last_name}')


# me = User('Do', 'Dat', age=20, gender='Male')
# me.describe_user()
# me.greet_user()
