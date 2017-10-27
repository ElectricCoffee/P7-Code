import unittest
from tioa.tioa import *
from test.udbm import Context

class GuardTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        c = Context(clock_names = ['x', 'y', 'z', 'w'], name = 'c')
        constraints = [(c.x, 2, '<' ), (c.y, 3, '>' ),
                       (c.z, 1, '<='), (c.x, 3, '>='),
                       (c.w, 8, '<' ), (c.y, 5, '<=')]

        cls.guard = Guard(*constraints)
        cls.context = c

    def test_max_clock_values(self):
        c = self.context
        table = self.guard.max_clock_values()
        self.assertTrue(table[c.x] == 3)
        self.assertTrue(table[c.y] == 5)
        self.assertTrue(table[c.z] == 1)
        self.assertTrue(table[c.w] == 8)

class TIOATest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        c = Context(clock_names = ['x', 'y', 'z', 'w'], name = 'c')
        
        locations = ['s', 'a', 'b']
        initial_location = 's'
        clocks = c.clocks
        edges = [Edge('s', 'q!', Guard((c.x, 2, '>'), (c.x, 5, '<')), [c.x], 'a'),
                 Edge('a', 'p?', Guard((c.y, 3, '<')), [], 'b')]
        input_actions = ['p?']
        output_actions = ['q!']
        invariants = [Guard((c.w, 1, '>')), Guard((c.z, 3, '>'))]

        cls.automaton = TIOA(locations, initial_location, clocks, edges, input_actions, output_actions, invariants)
        cls.context = c
        
    def test_max_clock_values(self):
        c = self.context
        table = self.automaton.max_clock_values()
        self.assertTrue(table[c.x] == 5)
        self.assertTrue(table[c.y] == 3)
        self.assertTrue(table[c.z] == 3)
        self.assertTrue(table[c.w] == 1)
