from orup_errors import general_functions
import unittest


class TestCase(unittest.TestCase):
    def test_if_car_num_valid(self):
        car_number = 'В060ХА702'
        response = general_functions.is_car_num_valid(car_number)
        self.assertTrue(response)
        car_number = '9189МХ02'
        response = general_functions.is_car_num_valid(car_number)
        self.assertTrue(response)
        car_number = '{102ХА102'
        response = general_functions.is_car_num_valid(car_number)
        self.assertTrue(response)
        car_number = 'В060ХА02'
        response = general_functions.is_car_num_valid(car_number)
        self.assertTrue(response)
        car_number = 'D060ХА102'
        response = general_functions.is_car_num_valid(car_number)
        self.assertFalse(response)
        car_number = 'D060[A102'
        response = general_functions.is_car_num_valid(car_number)
        self.assertFalse(response)
        car_number = '[060ХА102'
        response = general_functions.is_car_num_valid(car_number)
        self.assertFalse(response)
        car_number = '[060ХА1022'
        response = general_functions.is_car_num_valid(car_number)
        self.assertFalse(response)


if __name__ == '__main__':
    unittest.main()

