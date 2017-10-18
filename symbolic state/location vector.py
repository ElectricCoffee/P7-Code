class LocationVector:
    def __init__(self, *locations):
        self.locations = locations

    def __eq__(self, other):
            return self.locations == other.locations

    def __ne__(self, other):
        return not self == other

    def __le__(self, other):
            for location, otherlocation in self.locations, other.locations:
                if otherlocation != '*' and location != otherlocation:
                    return False
            return True

    def __ge__(self, other):
        return other <= self

    def __lt__(self, other):
        return self <= other and self != other

    def __gt__(self, other):
        return other <= self and self != other