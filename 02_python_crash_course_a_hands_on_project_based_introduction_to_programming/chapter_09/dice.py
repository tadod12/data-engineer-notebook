from random import randint


class Die:
    def __init__(self, sides=6):
        self.sides = sides

    def roll_die(self):
        print(randint(1, self.sides))


die_6 = Die(6)
print('Roll die 6 sides')
for i in range(10):
    die_6.roll_die()

die_10 = Die(10)
print('Roll die 10 sides')
for i in range(10):
    die_10.roll_die()
