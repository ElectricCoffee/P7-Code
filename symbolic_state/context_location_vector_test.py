import unittest
from symbolic_state.context_location_vector import *
from tioa.tioa import TIOA
from tioa.automata_context import AutomataContext


class ContextLocationVectorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.automaton0 = TIOA(['x', 'y'], 'x', None, None, None, None, None)
        cls.automaton1 = TIOA(['a', 'b'], 'a', None, None, None, None, None)
        cls.automaton2 = TIOA(['f', 'g'], 'f', None, None, None, None, None)

        context = AutomataContext([cls.automaton0, cls.automaton1, cls.automaton2])

        cls.lv0 = ContextLocationVector(context, ['x', 'a', 'g'])
        cls.lv1 = ContextLocationVector(context, ['x', 'b', 'g'])

    def test_m_equivalence(self):
        self.assertTrue(self.lv0.m_equivalence(self.lv1, {self.automaton0}))
        self.assertFalse(self.lv0.m_equivalence(self.lv1, {self.automaton1}))
        self.assertTrue(self.lv0.m_equivalence(self.lv1, {self.automaton2}))
        self.assertFalse(self.lv0.m_equivalence(self.lv1, {self.automaton0, self.automaton1}))
        self.assertTrue(self.lv0.m_equivalence(self.lv1, {self.automaton0, self.automaton2}))
        self.assertFalse(self.lv0.m_equivalence(self.lv1, {self.automaton1, self.automaton2}))
        self.assertFalse(self.lv0.m_equivalence(self.lv1, {self.automaton0, self.automaton1, self.automaton2}))

if __name__ == '__main__':
    unittest.main()