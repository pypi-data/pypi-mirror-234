import time
import unittest
import inspect
from jwtools.func import *
from jwtools.tests.test_base import BasicsTestCase
from jwtools.dt import *
import os


class IOTestCase(BasicsTestCase):

    def test_time_ms(self):
        print_line('test_time_ms')

        print_vf(
            'time_s',
            time_s(),
            'time_ms',
            time_ms(),
        )

        print_line('sleep(0.1)')
        time.sleep(0.1)

        print_vf(
            'time_s',
            time_s(),
            'time_ms',
            time_ms(),
        )

        print_line('sleep(3)')
        time.sleep(3)

        print_vf(
            'time_s',
            time_s(),
            'time_ms',
            time_ms(),
        )

        self.assertTrue(True, 'test_time_ms')

    def test_time_ms(self):
        print_line('test_time_ms')
        print_vf(
            time_s(),
            time_s(1),
            time_s(2),
            time_s(3)
        )

        self.assertTrue(True, 'test_time_ms')

    def test_time_work(self):
        print_line('test_time_ms')
        start = time.time()
        time.sleep(2)
        print_vf(
            time_work(start),
        )

        self.assertTrue(True, 'test_time_ms')



    def test_work_times(self):
        print_line('test_time_ms')
        times = []
        time1 = time.time()
        times.append((time1, 'time1'))
        time.sleep(2)
        time2 = time.time()
        times.append((time2, 'time2'))
        time.sleep(3)
        time3 = time.time()
        times.append((time3, 'time3'))
        result = work_times(times)
        print_vf(
            result,
        )

        self.assertTrue(True, 'test_time_ms')


if __name__ == '__main__':
    unittest.main()
