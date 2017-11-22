from itertools import groupby
from numbers import Number

from dbm.udbm import Clock


class TIOA:
    """TIOA: Timed Input/Output Automaton"""
    
    def __init__(self, locations, initial_location, clocks, edges, input_actions, output_actions, invariants):
        """Constructor for the Timed Input/Output Automaton

        Keyword Arguments:
        locations -- a set of location identifiers, descirbing nodes in the tioa
        initial_location -- a location in the set of locations
        clocks -- clocks is a set of clocks (constructed via Context)
        edges -- edges is a list of Edges
        input_actions -- set of input actions
        output_actions -- set of output actions
        invariants -- dictionaries with locations as keys, and guards as values
        """
        self.locations = locations
        self.initial_location = initial_location
        self.clocks = clocks
        self.edges = edges
        self.input_actions = input_actions
        self.output_actions = output_actions
        self.invariants = invariants
        self.preceeding_edges = {}
        self._generate_preceeding_edges()

    def _generate_preceeding_edges(self):
        self.preceeding_edges = groupby(sorted(self.edges, key=lambda edge: edge.target_location),
                                        key=lambda edge: edge.target_location)

    def is_valid_edge(self, edge):
        return \
            edge.initial_location in self.locations \
            and (edge.action in self.output_actions or edge.action in self.input_actions) \
            and edge.reset <= self.clocks \
            and edge.target_location in self.locations

    def max_clock_values(self):
        """Gets the maximum clock value for each clock, based on the maximum clock values in the edges and invariants"""
        clock_table = {k: [] for k in self.clocks} # initialise a dictionary using every clock as the keys
        guards = [edge.guard for edge in self.edges] + [guard for guard in self.invariants.values()]

        # transfer all the max-values of all the guards to the dict table
        for guard in guards:    # todo: find a nicer way to do this
            mcv = guard.max_clock_values()
            for clock, max_value in mcv.iteritems():
                clock_table[clock] = clock_table[clock].append(max_value)

        # destructively iterate over the dict table, and insert the maximum max_value
        for clock, max_values in clock_table.iteritems():
            clock_table[clock] = max(max_values)

        return clock_table

class Edge:
    def __init__(self, initial_location, action, guard, reset, target_location):
        self.initial_location = initial_location  # is the s in s -> s'
        self.action = action
        self.guard = guard
        self.reset = reset  # reset is a set of clocks that will be reset over the edge
        self.target_location = target_location  # is the s' in s -> s'

class Guard:
    """TIOA representation of a Guard, with TIOA specific functionality"""

    # tuple indices to avoid magic numbers
    _clock     = 0
    _value     = 1
    _relation  = 2
    # a list of legal relations
    _relations = ['<', '<=', '>', '>=']
    
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
            and isinstance(relation, str) \
            and relation in Guard._relations

    @staticmethod
    def _tuple_to_federation(op):
        """Converts a single tuple to a federation.

        op -- a tuple of the form (clock, value, relation), where relation in _relations
        """
        (clock, value, relation) = op
        
        if relation == '<':
            return clock < value
        elif relation == '<=':
            return clock <= value
        elif relation == '>':
            return clock > value
        elif relation == '>=':
            return clock >= value
        else:
            raise LookupError('The provided relation is not valid.')

    def to_federations(self):
        """Converts the clocks and values into a list of federations."""
        return map(Guard._tuple_to_federation, self.ops)
            
    def to_federation(self):
        """Converts all the clocks and values into a single federation."""
        return reduce(lambda x, y: x & y, self.to_federations())

    def clocks(self):
        """Gets all the clocks in ops."""
        return map(lambda op: op[self._clock], self.ops)

    def values(self):
        """Gets all the values in ops."""
        return map(lambda op: op[self._value], self.ops)

    def relations(self):
        """Gets all the relations in ops."""
        return map(lambda op: op[self._relation], self.ops)

    def max_clock_values(self):
        """Returns a table of the maximum value for each clock in the guard"""
        # ask sorted and groupby to only check the clock part of the triple
        clock      = lambda op: op[self._clock]
        # groupby doesn't work well on unsorted lists, this part is a must
        sorted_ops = sorted(self.ops, key = clock)
        max_clocks = {}

        for key, group in groupby(sorted_ops, key = clock):
            max_clocks[key] = max([op[self._value] for op in group])

        return max_clocks

    def k_sorted(self, k):
        return self.clocks() <= k
        
