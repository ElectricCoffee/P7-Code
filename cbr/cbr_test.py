import unittest
from cbr import *
from dbm.udbm import *
from tioa.tioa import *
from symbolic_state.double_symbolic_state import *
from symbolic_state.location_vector import *
from tioa.automata_context import *

class double_symbolic_state_test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.c = Context(['x', 'y'], 'c')
        cls.t1 = TIOA(["a", "b", "c"], "a", ['x', 'y'],
                      [Edge("a", "g", None, [], "b"), Edge("b", "h", None, [], "c")], ["g"], ["h"], {})
        cls.t2 = TIOA(["d", "e", "f"], "d", ['x', 'y'],
                      [Edge("d", "g", None, [], "e"), Edge("e", "h", None, [], "f")], ["h"], ["g"], {})
        cls.t3 = TIOA(["l", "m", "n"], "l", ['x', 'y'],
                      [Edge("l", "r", None, [], "m"), Edge("m", "t", None, [], "n")], ["r"], ["t"], {})

        cls.t4 = TIOA(["a", "b", "c"], "a", ['x', 'y'],
                      [Edge("a", "g", Guard((cls.c['x'], 2, '>')), [], "b"), Edge("b", "h", None, [], "c")], ["g"], ["h"], {})
        cls.t5 = TIOA(["d", "e", "f"], "d", ['x', 'y'],
                      [Edge("d", "g", Guard((cls.c['x'], 2, '>')), [], "e"), Edge("e", "h", None, [], "f")], ["h"], ["g"], {})
        cls.t6 = TIOA(["l", "m", "n"], "l", ['x', 'y'],
                      [Edge("l", "g", Guard((cls.c['x'], 2, '<')), [], "m"), Edge("m", "h", None, [], "n")], ["h"], ["g"], {})

        cls.autocon12 = AutomataContext([cls.t1, cls.t2])

    def test_sym_pre(self):
        self.assertTrue(DoubleSymbolicState(self.autocon12.ContextLocationVector(["c", "f"]), self.c.getZeroFederation()).mk_predecessors([self.t1, self.t2], self.c.items()) == DoubleSymbolicState(self.autocon12.ContextLocationVector(["b", "e"]), self.c.getZeroFederation()))

    def tes_cbr_true_wu_zone(self):
        self.assertTrue(cbr(DoubleSymbolicState(LocationVector(["a", "d"]), self.c.getZeroFederation()),
                            DoubleSymbolicState(LocationVector(["c", "f"]), self.c.getZeroFederation()),
                            [self.t1, self.t2]), self.c.items())

    def tes_cbr_false_wu_zone(self):
        self.assertFalse(cbr(DoubleSymbolicState(LocationVector(["a", "l"]), self.c.getZeroFederation()),
                             DoubleSymbolicState(LocationVector(["c", "n"]), self.c.getZeroFederation()),
                             [self.t1, self.t3]), self.c.items())

    def tes_cbr_true_w_zone(self):
        self.assertTrue(cbr(DoubleSymbolicState(LocationVector(["a", "d"]), self.c.getZeroFederation()),
                            DoubleSymbolicState(LocationVector(["c", "f"]), self.c.getZeroFederation()),
                            [self.t4, self.t5]), self.c.items())

    def tes_cbr_false_w_zone(self):
        self.assertFalse(cbr(DoubleSymbolicState(LocationVector(["a", "l"]), self.c.getZeroFederation()),
                             DoubleSymbolicState(LocationVector(["c", "n"]), self.c.getZeroFederation()),
                             [self.t4, self.t6]), self.c.items())

if __name__ == '__main__':
            unittest.main()