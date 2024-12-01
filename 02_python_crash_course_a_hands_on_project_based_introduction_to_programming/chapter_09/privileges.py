from users import User


class Privileges:
    """Store admins privileges"""
    def __init__(self):
        self.privileges = ['can add post', 'can delete post', 'can ban user']

    def show_privileges(self):
        print('Privileges list: ')
        for privilege in self.privileges:
            print(f'- {privilege}')


class Admin(User):
    def __init__(self, first_name, last_name, **info):
        super().__init__(first_name, last_name, **info)
        self.privileges = Privileges()


# admin = Admin('do', 'dat')
# admin.privileges.show_privileges()
