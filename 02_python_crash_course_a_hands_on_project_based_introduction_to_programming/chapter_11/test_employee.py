import unittest
from employee import Employee


class TestEmployee(unittest.TestCase):
    def setUp(self):
        self.employee = Employee('John', 'Smith', 100000)
        self.custom_raise = 10000

    def test_give_default_raise(self):
        new_salary = self.employee.annual_salary + 5000
        self.assertEqual(self.employee.give_raise(), new_salary)

    def test_give_custom_raise(self):
        new_salary = self.employee.annual_salary + self.custom_raise
        self.assertEqual(self.employee.give_raise(self.custom_raise), new_salary)


if __name__ == '__main__':
    unittest.main()
