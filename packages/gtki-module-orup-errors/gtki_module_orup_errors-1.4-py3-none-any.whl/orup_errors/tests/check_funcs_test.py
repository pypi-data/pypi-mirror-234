from orup_errors import check_funcs
import unittest


class TestCase(unittest.TestCase):
    def test_check_valid(self):
        car_num = '{102ХА102'
        res = check_funcs.check_car_number(car_num)
        print(res)


if __name__ == '__unittest__':
    unittest.main()