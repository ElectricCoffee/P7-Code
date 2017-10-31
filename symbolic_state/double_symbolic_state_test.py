import unittest
from double_symbolic_state import *
import sys
sys.path.insert(0, '../dbm/')
from udbm import *

class double_symbolic_state_test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.c = Context(['x', 'y', 'z', 'w'], 'c')
        cls.zone1 = (cls.c.x < 3) & (cls.c.x > 2) & (cls.c.y < 5) & (cls.c.y > 1)
        cls.zone2 = (cls.c.x < 3) & (cls.c.x > 2) & (cls.c.y < 5) & (cls.c.y > 1) & (cls.c.z < 8)
        cls.zone3 = (cls.c.x < 3) & (cls.c.x > 2) & (cls.c.y < 5) & (cls.c.y > 1) & (cls.c.z < 8) & (cls.c.w > 2) & (cls.c.w < 8)
        cls.zone4 = (cls.c.x < 4) & (cls.c.x > 2) & (cls.c.y < 5) & (cls.c.y > 1)

        #  Automata -- Only locations and initial location are defined.
        cls.automaton0 = TIOA(['x', 'y'], 'x', None, None, None, None, None)
        cls.automaton1 = TIOA(['a', 'b'], 'a', None, None, None, None, None)
        cls.automaton2 = TIOA(['f', 'g'], 'f', None, None, None, None, None)

        #  Context for the context location vectors -- Includes all the automata
        context = AutomataContext([cls.automaton0, cls.automaton1, cls.automaton2])

        #  Context location vectors created with context
        lv0 = context.ContextLocationVector(['x', 'a', 'g'])
        lv1 = context.ContextLocationVector(['x', 'b', 'g'])

        cls.dss1 = DoubleSymbolicState(lv0, cls.zone1)
        cls.dss2 = DoubleSymbolicState(lv1, cls.zone2)
        cls.dss3 = DoubleSymbolicState(lv0, cls.zone3)
        cls.dss4 = DoubleSymbolicState(lv1, cls.zone4)

    def test_k_eqiavalens1_1(self):  # a double symbolic states needs to be k-equivalent with it self
        self.assertTrue(self.dss1.k_equivalence(self.dss1, ['x', 'y']))

    def test_k_eqiavalens1_2(self):  # without the dimension z dss1 and dss2 should be k-equivalent
        self.assertTrue(self.dss1.k_equivalence(self.dss2, ['x', 'y']))

    def test_k_eqiavalens1_2_z(self):  # with the dimension z dss1 and dss2 should not be k-equivalent
        self.assertFalse(self.dss1.k_equivalence(self.dss2, ['x', 'y', 'z']))

    def test_k_eqiavalens1_3(self):  # without the dimension z and w, dss1 and dss3 should be k-equivalent
        self.assertTrue(self.dss1.k_equivalence(self.dss3, ['x', 'y']))

    def test_k_eqiavalens1_3_z(self):  # with the dimension z, dss1 and dss3 should not be k-equilventent
        self.assertFalse(self.dss1.k_equivalence(self.dss3, ['x', 'y', 'z']))

    def test_k_eqiavalens1_2_z_w(self):  # with the exstra dimension w, which dss1 and dss2 do not have, then they are not k-equivalent
        self.assertFalse(self.dss1.k_equivalence(self.dss2, ['x', 'y', 'z', 'w']))

    def test_k_eqiavalens2_3(self):  # dss2 and dss3 should be k-equivalent without the dimension w
        self.assertTrue(self.dss2.k_equivalence(self.dss3, ['x', 'y', 'z']))

    def test_k_eqiavalens2_3_w(self):  # with the dimension w, dss2 and dss3 should not be k-equivalent
        self.assertFalse(self.dss2.k_equivalence(self.dss3, ['x', 'y', 'z', 'w']))

    def test_k_eqiavalens1_4(self):  # dss1 and dss4 should not be k-equivalent because they do not have the same contrains
        self.assertFalse(self.dss1.k_equivalence(self.dss4, ['x', 'y']))

    def test_k_eqiavalens1_1_z(self):  # this should not be k-equivalent because dss1 do not have the dimension z
        self.assertTrue(self.dss1.k_equivalence(self.dss1, ['x', 'y', 'z']))

    def testmk_equivalence(self):
        self.assertTrue(self.dss1.mk_equivalence(self.dss2, self.zone1, self.automaton0))
        self.assertTrue(self.dss1.mk_equivalence(self.dss2, self.zone1, self.automaton2))

        self.assertFalse(self.dss1.mk_equivalence(self.dss2, self.zone2, self.automaton0)) # k-equavalence should return false
        self.assertFalse(self.dss1.mk_equivalence(self.dss2, self.zone1, self.automaton1)) # m-equavalence should return false

if __name__ == '__main__':
    unittest.main()
