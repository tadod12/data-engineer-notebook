class User:
    def __init__(self, first_name, last_name, **info):
        """Save user's info, more information stored in 'info' dictionary"""
        self.first_name = first_name
        self.last_name = last_name
        self.info = info
        self.login_attempts = 0

    def describe_user(self):
        print(f'\nName: {self.first_name} {self.last_name}')
        for key, value in self.info.items():
            print(f'{key}: {value}')

    def greet_user(self):
        print(f'\nHello {self.first_name} {self.last_name}')

    def increment_login_attempts(self):
        self.login_attempts += 1

    def reset_login_attempts(self):
        self.login_attempts = 0


dodat_12 = User('do', 'dat')
dodat_12.increment_login_attempts()
print(f'Number of login attempts: {dodat_12.login_attempts}')
dodat_12.reset_login_attempts()
print(f'Number of login attempts: {dodat_12.login_attempts}')
