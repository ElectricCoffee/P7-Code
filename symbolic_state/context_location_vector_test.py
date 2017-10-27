import unittest
from .context_location_vector import *
from tioa.tioa import TIOA
from tioa.automata_context import AutomataContext


class ContextLocationVectorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #  Automata -- Only locations and initial location are defined.
        cls.automaton0 = TIOA(['x', 'y'], 'x', None, None, None, None, None)
        cls.automaton1 = TIOA(['a', 'b'], 'a', None, None, None, None, None)
        cls.automaton2 = TIOA(['f', 'g'], 'f', None, None, None, None, None)

        #  Context for the context location vectors -- Includes all the automata
        context = AutomataContext([cls.automaton0, cls.automaton1, cls.automaton2])

        #  Context location vectors created with context
        cls.lv0 = context.ContextLocationVector(['x', 'a', 'g'])
        cls.lv1 = context.ContextLocationVector(['x', 'b', 'g'])

    def test_m_equivalence(self):
        #  Tests m_equivalence between lv0 and lv1, with all legal permutations of m.
        #  Asserts true iff automaton1 is not in m
        self.assertTrue(self.lv0.m_equivalence(self.lv1, {self.automaton0}))
        self.assertTrue(self.lv0.m_equivalence(self.lv1, {self.automaton2}))
        self.assertTrue(self.lv0.m_equivalence(self.lv1, {self.automaton0, self.automaton2}))

        self.assertFalse(self.lv0.m_equivalence(self.lv1, {self.automaton1}))
        self.assertFalse(self.lv0.m_equivalence(self.lv1, {self.automaton0, self.automaton1}))
        self.assertFalse(self.lv0.m_equivalence(self.lv1, {self.automaton1, self.automaton2}))
        self.assertFalse(self.lv0.m_equivalence(self.lv1, {self.automaton0, self.automaton1, self.automaton2}))

if __name__ == '__main__':
    unittest.main()
