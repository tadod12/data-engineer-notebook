from users import User


class Admin(User):
    def __init__(self, first_name, last_name, **info):
        super().__init__(first_name, last_name, **info)
        self.privileges = ['can add post', 'can delete post', 'can ban user']

    def show_privileges(self):
        print('Admin\'s set of privileges: ')
        for privilege in self.privileges:
            print(f'- {privilege}')


# admin = Admin('do', 'dat', age=21, height=175, weight=71)
# admin.show_privileges()
# admin.describe_user()
