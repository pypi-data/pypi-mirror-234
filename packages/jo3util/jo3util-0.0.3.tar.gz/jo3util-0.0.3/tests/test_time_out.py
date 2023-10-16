#! /usr/bin/env python3
# vim:fenc=utf-8

import time
import unittest

from src.time_out import TimeoutException, time_limit


class TestTimeOut(unittest.TestCase):
    def test_exception(self):
        with self.assertRaises(TimeoutException):
            with time_limit(1):
                time.sleep(2)

    def test_no_exception(self):
        with time_limit(1):
            time.sleep(0.5)


if __name__ == "__main__":
    unittest.main()
