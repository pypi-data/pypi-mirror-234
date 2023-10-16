import unittest
import inspect
from jwtools.func import *
from jwtools.tests.test_base import BasicsTestCase
from jwtools.io_util import *
import os


class IOTestCase(BasicsTestCase):

    def test_get_parent_directory(self):
        print_line('不使用 NumPy 平铺列表')

        # cur_path = os.getcwd()
        cur_path = __file__
        print_vf(
            '__file__',
            __file__,
            'cur_path',
            cur_path,
            'level1',
            get_parent_directory(cur_path, 1),
            'level2',
            get_parent_directory(cur_path, 2),
            'level3',
            get_parent_directory(cur_path, 3),
        )


if __name__ == '__main__':
    unittest.main()
