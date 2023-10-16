#
# Copyright (c) 2000, 2099, ducesoft and/or its affiliates. All rights reserved.
# DUCESOFT PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#
import unittest

from mesh.metrics.collector import Collector


class TestCollector(unittest.TestCase):

    def test_collect(self):
        Collector().collect()


if __name__ == '__main__':
    unittest.main()
