import unittest
from city_functions import city_functions


class CityTests(unittest.TestCase):
    def test_city_country(self):
        function_result = city_functions('santiago', 'chile')
        self.assertEqual(function_result, 'Santiago, Chile')

    def test_city_country_population(self):
        function_result = city_functions('santiago', 'chile', population=5000000)
        self.assertEqual(function_result, 'Santiago, Chile - population 5000000')

if __name__ == '__main__':
    unittest.main()
