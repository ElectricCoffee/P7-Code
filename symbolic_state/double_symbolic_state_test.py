import unittest
from double_symbolic_state import *
import sys
sys.path.insert(0, '../test/')
from udbm import *

class double_symbolic_state_test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.c = Context(clock_names=['x', 'y', 'z', 'w'], name='c')
        cls.zone1 = (cls.c.x < 3) & (cls.c.x > 2) & (cls.c.y < 5) & (cls.c.y > 1)
        cls.zone2 = (cls.c.x < 3) & (cls.c.x > 2) & (cls.c.y < 5) & (cls.c.y > 1) & (cls.c.z < 8)
        cls.zone3 = (cls.c.x < 3) & (cls.c.x > 2) & (cls.c.y < 5) & (cls.c.y > 1) & (cls.c.z < 8) & (cls.c.w > 2) & (cls.c.w < 8)

        cls.dss1 = DoubleSymbolicState(None, cls.zone1)
        cls.dss2 = DoubleSymbolicState(None, cls.zone2)
        cls.dss3 = DoubleSymbolicState(None, cls.zone3)

    def test_k_eqiavalens(self):
        x = self.c.items()[0]
        y = self.c.items()[1]
        z = self.c.items()[2]
        w = self.c.items()[3]
        self.assertTrue(self.dss1.k_equivalence(self.dss1, [x, y]))
        self.assertTrue(self.dss1.k_equivalence(self.dss2, [x, y]))
        self.assertFalse(self.dss1.k_equivalence(self.dss2, [x, y, z]))
        self.assertTrue(self.dss1.k_equivalence(self.dss3, [x, y]))
        self.assertFalse(self.dss1.k_equivalence(self.dss3, [x, y, z]))
        self.assertFalse(self.dss1.k_equivalence(self.dss2, [x, y, z, w]))
        self.assertTrue(self.dss2.k_equivalence(self.dss3, [x, y, z]))
        self.assertFalse(self.dss2.k_equivalence(self.dss3, [x, y, z, w]))


if __name__ == '__main__':
    unittest.main()
