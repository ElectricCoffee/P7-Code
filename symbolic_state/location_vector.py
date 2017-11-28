class LocationVector(list):
    def __init__(self, locations):
        super(LocationVector, self).__init__(locations)

    def __le__(self, other):
        """Checks if self is included in other"""
        for location, otherlocation in zip(self, other):
            if otherlocation != '*' and location != otherlocation:
                return False
        return True

    def __ge__(self, other):
        """Checks if other is included in self"""
        return other <= self

    def __lt__(self, other):
        """Checks if self is strictly included in other"""
        return self <= other and self != other

    def __gt__(self, other):
        """Checks if other is strictly included in self"""
        return other <= self and self != other

    def __hash__(self):
        return hash(tuple(self))