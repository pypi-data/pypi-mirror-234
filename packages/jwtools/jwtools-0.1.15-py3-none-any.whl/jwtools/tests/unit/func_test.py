import unittest
import inspect
from jwtools.func import *
from jwtools.tests.test_base import BasicsTestCase


class FuncTestCase(BasicsTestCase):
    def test_flatten_list(self):
        print_line('不使用 NumPy 平铺列表')

        # 示例列表
        my_list = [[1, 2, 3], [4, [5, 6]], [7, 8, [9, 10]]]

        # 不使用 NumPy 平铺列表
        flattened_list = flatten_list(my_list)
        print(flattened_list)  # 输出 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        assert_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertListEqual(flattened_list, assert_list)

        # 示例列表
        my_list = [[1, 2, 3], [4, [5, 6]], [7, 8, [9, 10]], [11, [12, [13, 14, [15, 16]]]]]
        flattened_list = flatten_list(my_list)
        print(flattened_list)  # 输出 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        assert_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        self.assertListEqual(flattened_list, assert_list)

    def test_get_max_dimension(self):
        print_line('test_get_max_dimension')
        lst = [
            [1, 2, 3],
            [1, [2, 3]],
            [1, [2, [3, 4]]],
            [1, [2, [3, 4, [5, 6]]]],
            [1, [2, [3, 4, [5, [6]]]]],
        ]
        result = [get_max_dimension(item) for item in lst]
        print_vf('input:', lst, 'output:', result)
        self.assertListEqual(result, [1, 2, 3, 4, 5])

    def test_dict_filter_sort(self):
        data = {
            'k1': {'weight': 0},
            'k2': {'weight': 3},
            'k3': {'weight': 1},
            'z1': {'weight': 2},
            'z2': {'weight': 2}
        }

        result = dict_filter_sort(
            data=data,
            filter_func=lambda x: x[0].startswith('k') and x[1].get('weight') >= 0,
            sort_func=lambda item: item[1].get('weight'),
            top=2
        )
        print([(k, v) for k, v in result.items()])

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
