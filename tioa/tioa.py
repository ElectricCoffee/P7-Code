import sys
sys.path.insert(0, '../test/')
import udbm

from numbers import Number

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

        *ops -- a list of tuples of the form (clock, value, relation).
        """
        # assert that all the tuples in ops are valid
        assert(all(map(Guard.is_valid_op, ops)))
        
        self.ops = ops

    @staticmethod
    def is_valid_op(op):
        """Checks if an ops-triple is valid.

        op -- A triple of the form (clock, value, relation)
        """
        (clock, value, relation) = op
        
        return  isinstance(clock, Clock) \
            and isinstance(value, Number) \
            and isinstance(relation, bool)

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
            
    def to_federation(self):
        """Converts all the clocks and values into a single federation."""
        return reduce(lambda x, y: x & y, self.to_federations())

    def clocks(self):
        """Gets all the clocks in ops."""
        return map(lambda ops: ops[0], self.ops)

    def values(self):
        """Gets all the values in ops."""
        return map(lambda ops: ops[1], self.ops)

    def relations(self):
        """Gets all the relations in ops. 

        Relations are booleans, true if <=, and false if <.
        """
        return map(lambda ops: ops[2], self.ops)
