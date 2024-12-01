from random import choice


def get_step():
    direction = choice([-1, 1])
    distance = choice([1, 2, 3, 4, 5])
    step = direction * distance
    return step


class RandomWalkRefactor():
    def __init__(self, num_points):
        self.num_points = num_points
        # init start
        self.x_values = [0]
        self.y_values = [0]

    def fill_walk(self):
        x_step = get_step()
        y_step = get_step()

        x = self.x_values[-1] + x_step
        y = self.y_values[-1] + y_step

        self.x_values.append(x)
        self.y_values.append(y)
