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
        cls.e1 = Edge("b", "h", Guard(cls.c), set(), "c")
        cls.e2 = Edge("e", "h", Guard(cls.c), set(), "f")
        cls.t1 = TIOA(["a", "b", "c"], "a", set(cls.c.clocks),
                      [Edge("a", "g", Guard(cls.c), set(), "b"), cls.e1], {"g"}, {"h"}, {})
        cls.t2 = TIOA(["d", "e", "f"], "d", set(cls.c.clocks),
                      [Edge("d", "g", Guard(cls.c), set(), "e"), cls.e2], {"h"}, {"g"}, {})
        cls.t3 = TIOA(["l", "m", "n"], "l", set(cls.c.clocks),
                      [Edge("l", "h", Guard(cls.c), set(), "m"), Edge("m", "g", Guard(cls.c), set(), "n")], {"h"}, {"g"}, {})

        cls.t4 = TIOA(["a", "b", "c"], "a", set(cls.c.clocks),
                      [Edge("a", "g", Guard(cls.c, (cls.c['x'], 2, '>')), set(), "b"),
                       Edge("b", "h", Guard(cls.c), set(), "c")], {"g"}, {"h"}, {})
        cls.t5 = TIOA(["d", "e", "f"], "d", set(cls.c.clocks),
                      [Edge("d", "g", Guard(cls.c, (cls.c['x'], 2, '>')), set(), "e"),
                       Edge("e", "h", Guard(cls.c), set(), "f")], {"h"}, {"g"}, {})
        cls.t6 = TIOA(["l", "m", "n"], "l", set(cls.c.clocks),
                      [Edge("l", "g", Guard(cls.c, (cls.c['x'], 2, '<')), set(), "m"),
                       Edge("m", "h", Guard(cls.c), set(), "n")], {"h"}, {"g"}, {})

        cls.t7 = TIOA(["a", "b", "c"], "a", set(cls.c.clocks),
                      [Edge("a", "g", Guard(cls.c), set(), "b"),
                       Edge("b", "h", Guard(cls.c), set(), "c")], {"g"}, {"h"}, {})
        cls.t8 = TIOA(["d", "e", "f"], "d", set(cls.c.clocks),
                      [Edge("d", "g", Guard(cls.c), set(), "e"),
                       Edge("e", "h", Guard(cls.c), set(), "f")], {"h"}, {"g"}, {"e":(cls.c.x == 1)})
        cls.t9 = TIOA(["l", "m", "n"], "l", set(cls.c.clocks),
                      [Edge("l", "g", Guard(cls.c), set(cls.c['x']), "m"),
                       Edge("m", "h", Guard(cls.c), set(), "n")], {"h"}, {"g"}, {"m":(cls.c.x == 1)})

        cls.autocon12 = AutomataContext([cls.t1, cls.t2])
        cls.autocon13 = AutomataContext([cls.t1, cls.t3])
        cls.autocon45 = AutomataContext([cls.t4, cls.t5])
        cls.autocon46 = AutomataContext([cls.t4, cls.t6])
        cls.autocon78 = AutomataContext([cls.t7, cls.t8])
        cls.autocon79 = AutomataContext([cls.t7, cls.t9])


        cls.clocks = set()
        for clock_name, clock in cls.c.items():
            cls.clocks.add(clock)

    def test_generate_options(self):
        self.assertEqual(list(DoubleSymbolicState._generate_options({"a":[2,3], "b":[5,7]})),[{"a":2,"b":5}, {"a":2,"b":7}, {"a":3,"b":5}, {"a":3,"b":7}])

    def test_get_predecessor_options(self):
        self.dss1 = DoubleSymbolicState(self.autocon12.ContextLocationVector(["c", "f"]), self.c.getTautologyFederation())
        self.assertEqual(list(self.dss1._get_predecessor_options([self.t1, self.t2], self.clocks)), [{self.t1:self.e1, self.t2:self.e2}])

    def test_sym_pre(self):
        self.dss1 = DoubleSymbolicState(self.autocon12.ContextLocationVector(["c", "f"]), self.c.getTautologyFederation())
        self.dss2 = DoubleSymbolicState(self.autocon12.ContextLocationVector(["b", "e"]), self.c.getTautologyFederation())
        self.assertTrue(self.dss1.mk_predecessors([self.t1, self.t2], self.clocks) == [self.dss2])

    def test_cbr_true_wu_zone(self):
        self.dss1 = DoubleSymbolicState(self.autocon12.ContextLocationVector(["a", "d"]), self.c.getTautologyFederation())
        self.dss2 = DoubleSymbolicState(self.autocon12.ContextLocationVector(["c", "f"]), self.c.getTautologyFederation())
        self.assertTrue(cbr(self.dss1, self.dss2, [self.t1, self.t2], self.clocks))

    def test_cbr_false_wu_zone(self):
        self.dss1 = DoubleSymbolicState(self.autocon13.ContextLocationVector(["a", "l"]), self.c.getTautologyFederation())
        self.dss2 = DoubleSymbolicState(self.autocon13.ContextLocationVector(["c", "n"]), self.c.getTautologyFederation())
        self.assertFalse(cbr(self.dss1, self.dss2, [self.t1, self.t3], self.clocks))

    def test_cbr_true_w_zone(self):
        self.dss1 = DoubleSymbolicState(self.autocon45.ContextLocationVector(["a", "d"]), self.c.getTautologyFederation())
        self.dss2 = DoubleSymbolicState(self.autocon45.ContextLocationVector(["c", "f"]), self.c.getTautologyFederation())
        self.assertTrue(cbr(self.dss1, self.dss2, [self.t4, self.t5], self.clocks))

    def test_cbr_false_w_zone(self):
        self.dss1 = DoubleSymbolicState(self.autocon46.ContextLocationVector(["a", "l"]), self.c.getTautologyFederation())
        self.dss2 = DoubleSymbolicState(self.autocon46.ContextLocationVector(["c", "n"]), self.c.getTautologyFederation())
        self.assertFalse(cbr(self.dss1, self.dss2, [self.t4, self.t6], self.clocks))

    def test_cbr_true_w_invariants(self):
        self.dss1 = DoubleSymbolicState(self.autocon78.ContextLocationVector(["a", "d"]),
                                        self.c.getTautologyFederation())
        self.dss2 = DoubleSymbolicState(self.autocon78.ContextLocationVector(["c", "f"]),
                                        self.c.getTautologyFederation())
        self.assertTrue(cbr(self.dss1, self.dss2, [self.t7, self.t8], self.clocks))

    def test_cbr_false_w_invariants(self):
        self.dss1 = DoubleSymbolicState(self.autocon79.ContextLocationVector(["a", "l"]),
                                        self.c.getTautologyFederation())
        self.dss2 = DoubleSymbolicState(self.autocon79.ContextLocationVector(["c", "n"]),
                                        self.c.getTautologyFederation())
        self.assertFalse(cbr(self.dss1, self.dss2, [self.t7, self.t9], self.clocks))

if __name__ == '__main__':
            unittest.main()