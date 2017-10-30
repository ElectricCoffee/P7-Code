from .location_vector import LocationVector


class ContextLocationVector(LocationVector):
    def __init__(self, context, locations):
        self.context = context
        super(ContextLocationVector, self).__init__(locations)