import sys
sys.path.insert(0, '../test/')
import udbm

class TIOA:
    def __init__(self, locations, initial_location, clocks, edges, actions_input, actions_output, invariants):
        self.locations = locations
        self.initial_location = initial_location
        self.clocks = clocks  # clocks is a set of clocks
        self.edges = edges
        self.actions_input = actions_input
        self.actions_output = actions_output
        self.invariants = invariants

    def is_valid_edge(self, edge):
        return \
            edge.initial_location in self.locations \
            and (edge.action in self.actions_output or edge.action in self.actions_input) \
            and edge.reset <= self.clocks \
            and edge.target_location in self.locations


class Edge:
    def __init__(self, initial_location, action, guard, reset, target_location):
        self.initial_location = initial_location  # is the s in s -> s'
        self.action = action
        self.guard = guard
        self.reset = reset  # reset is a set of clocks that will be reset over the edge
        self.target_location = target_location  # is the s' in s -> s'

class Guard:
    """TIOA representation of a Guard, with TIOA specific functionality"""
    
    def __init__(self, *ops):
        """Initialises the Guard

        *ops --  a list of tuples of the form (clock, value, relation).
        """
        self.ops = ops

    @staticmethod
    def _tuple_to_federation(op):
        """Converts a single tuple to a federation.

        op -- a tuple of the form (clock, value, relation), where relation is a boolean
        """
        (clock, value, is_strict) = op
        if is_strict:
            return clock <= value
        else:
            return clock < value

    def to_federations(self):
        """Converts the clocks and values into a list of federations."""
        return map(Guard._tuple_to_federation, ops)
            
