class TIOA:

    def is_valid_edge(self, edge):
        return \
            edge.initial_location in self.locations \
            and (edge.action in self.actions_output or edge.action in self.actions_input) \
            and edge.reset <= self.clocks \
            and edge.target_location in self.locations

    def __init__(self, locations, initial_location, clocks, edges, actions_input, actions_output, invariants):
        self.locations = locations
        self.initial_location = initial_location
        self.clocks = clocks
        self.edges = edges
        self.actions_input = actions_input
        self.actions_output = actions_output
        self.invariants = invariants


class Edge:

    def __init__(self, initial_location, action, guard, reset, target_location):
        self.initial_location = initial_location
        self.action = action
        self.guard = guard
        self.reset = reset
        self.target_location = target_location
